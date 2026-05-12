"""Runner: invokes an agent on each Sample, captures answer + trace,
with file-based caching.

Design notes:
  - The runner does NOT know about run_agent() directly. It accepts a
    plain callable `agent_fn(question: str) -> (answer: str, trace: dict)`.
    This decouples the harness from any specific RAG implementation —
    tomorrow you can pass a different agent_fn (vector retrieval, hybrid,
    a different LLM) and reuse everything else. This is the same
    abstraction Inspect calls a "Solver".

  - Caching is keyed by (run_label, sample_id, question_hash). The
    run_label is an explicit string the caller chooses (e.g. "v1-bm25",
    "v2-no-efficiency-prompt"). Bumping the run_label = new experiment.
    Embedding the question hash means edits to groundtruth.jsonl
    auto-invalidate stale cache entries instead of silently returning
    cached answers to questions that have since changed.

  - Cache files are JSON; one file per sample. Easy to inspect, edit,
    or delete. No SQLite, no pickle — debuggability over performance.
    The harness runs at minute-scale, not millisecond-scale.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Iterable

from .dataset import Sample


# ── Typed result structures ──────────────────────────────────────────

@dataclass(frozen=True)
class ToolCall:
    name: str
    args: dict
    result_preview: str


@dataclass(frozen=True)
class Trace:
    """Structured agent trace. Captures what the agent did, not just
    what it said. Critical for process eval — e.g. 'did the agent issue
    a second retrieval on this multi-hop question?'"""
    tool_calls: tuple[ToolCall, ...]
    turns: int
    tokens_in: int
    tokens_out: int
    cached_tokens: int


@dataclass(frozen=True)
class Result:
    """One sample's run. The scorer consumes this."""
    sample_id: str
    question: str
    answer: str
    trace: Trace
    cache_hit: bool
    elapsed_seconds: float


# ── Cache helpers ────────────────────────────────────────────────────

def _question_hash(question: str) -> str:
    return hashlib.sha256(question.encode("utf-8")).hexdigest()[:12]


def _cache_path(cache_dir: Path, sample: Sample) -> Path:
    return cache_dir / f"{sample.id}_{_question_hash(sample.question)}.json"


def _load_cached(path: Path) -> Result | None:
    if not path.exists():
        return None
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None  # corrupt cache → treat as miss
    return Result(
        sample_id=obj["sample_id"],
        question=obj["question"],
        answer=obj["answer"],
        trace=Trace(
            tool_calls=tuple(ToolCall(**tc) for tc in obj["trace"]["tool_calls"]),
            turns=obj["trace"]["turns"],
            tokens_in=obj["trace"]["tokens_in"],
            tokens_out=obj["trace"]["tokens_out"],
            cached_tokens=obj["trace"]["cached_tokens"],
        ),
        cache_hit=True,
        elapsed_seconds=obj.get("elapsed_seconds", 0.0),
    )


def _save_cached(path: Path, result: Result) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "sample_id": result.sample_id,
        "question": result.question,
        "answer": result.answer,
        "trace": {
            "tool_calls": [asdict(tc) for tc in result.trace.tool_calls],
            "turns": result.trace.turns,
            "tokens_in": result.trace.tokens_in,
            "tokens_out": result.trace.tokens_out,
            "cached_tokens": result.trace.cached_tokens,
        },
        "elapsed_seconds": result.elapsed_seconds,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


# ── Public runner API ────────────────────────────────────────────────

AgentFn = Callable[[str], tuple[str, dict]]


def run_one(
    sample: Sample,
    agent_fn: AgentFn,
    cache_dir: Path,
    force: bool = False,
) -> Result:
    """Run the agent on one sample.

    Args:
        sample:    The Sample to run.
        agent_fn:  A function that takes a question and returns
                   (answer_str, trace_dict). The trace_dict must have
                   keys: tool_calls, turns, tokens_in, tokens_out,
                   cached_tokens. Matches the contract of run_agent
                   when return_trace=True.
        cache_dir: Directory for per-sample JSON cache files. Created
                   if missing.
        force:     If True, ignore any cached result and re-run.
    """
    path = _cache_path(cache_dir, sample)

    if not force:
        cached = _load_cached(path)
        if cached is not None:
            return cached

    t0 = time.time()
    answer, raw_trace = agent_fn(sample.question)
    elapsed = time.time() - t0

    trace = Trace(
        tool_calls=tuple(
            ToolCall(
                name=tc["name"],
                args=tc.get("args", {}),
                result_preview=tc.get("result_preview", ""),
            )
            for tc in raw_trace.get("tool_calls", [])
        ),
        turns=raw_trace.get("turns", 0),
        tokens_in=raw_trace.get("tokens_in", 0),
        tokens_out=raw_trace.get("tokens_out", 0),
        cached_tokens=raw_trace.get("cached_tokens", 0),
    )

    result = Result(
        sample_id=sample.id,
        question=sample.question,
        answer=answer,
        trace=trace,
        cache_hit=False,
        elapsed_seconds=elapsed,
    )
    _save_cached(path, result)
    return result


def run_all(
    samples: Iterable[Sample],
    agent_fn: AgentFn,
    cache_dir: Path,
    force: bool = False,
    progress: bool = True,
) -> list[Result]:
    """Run the agent on every sample. Returns results in input order."""
    import sys
    results: list[Result] = []
    samples = list(samples)
    total = len(samples)
    for i, sample in enumerate(samples, start=1):
        if progress:
            tag = sample.question_type[:4]
            print(f"  [{i:>2}/{total}] {sample.id} ({tag})…", end="", flush=True, file=sys.stderr)
        r = run_one(sample, agent_fn, cache_dir, force=force)
        if progress:
            marker = "cache" if r.cache_hit else f"{r.elapsed_seconds:.1f}s"
            tools = len(r.trace.tool_calls)
            print(f" {marker}, {tools} tool calls", file=sys.stderr)
        results.append(r)
    return results
