"""Aggregate Scores into a report. Writes JSON and Markdown side-by-side
under evals/reports/<label>/<timestamp>/.

Design:
  - No LLM calls. Pure aggregation over the in-memory list of
    (Sample, Result, Score) triples.
  - JSON is the canonical machine-readable artifact; downstream tooling
    (charts, comparison scripts, regressions in CI) reads this.
  - Markdown is for humans — PR reviews, blog posts, the README. It
    contains the same numbers as the JSON, formatted as tables and
    headed sections so it renders cleanly on GitHub.
  - Each run is preserved under its own timestamped subdirectory so
    that comparing runs is as simple as diffing two folders.
"""

from __future__ import annotations

import json
import statistics
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .dataset import Sample
from .runner import Result
from .scorer import Score


# ── Aggregation ──────────────────────────────────────────────────────

def _aggregate(scores: list[Score], results: list[Result]) -> dict:
    """Compute headline + per-category + trace metrics."""
    by_type: dict[str, list[Score]] = {}
    for s in scores:
        by_type.setdefault(s.question_type, []).append(s)

    # Build a sample_id -> Result lookup for trace metrics
    results_by_id = {r.sample_id: r for r in results}

    def _pass_rate(group: list[Score]) -> float:
        return sum(1 for s in group if s.passed) / len(group) if group else 0.0

    def _avg_value(group: list[Score]) -> float:
        return statistics.fmean(s.value for s in group) if group else 0.0

    def _component_avg(group: list[Score], comp: str) -> float | None:
        vals = [s.components[comp] for s in group if comp in s.components]
        return statistics.fmean(vals) if vals else None

    def _trace_stats(group: list[Score]) -> dict:
        traces = [results_by_id[s.sample_id].trace for s in group if s.sample_id in results_by_id]
        if not traces:
            return {}
        tool_counts = [len(t.tool_calls) for t in traces]
        return {
            "avg_tool_calls": statistics.fmean(tool_counts),
            "max_tool_calls": max(tool_counts),
            "avg_turns": statistics.fmean(t.turns for t in traces),
            "total_tokens_in": sum(t.tokens_in for t in traces),
            "total_tokens_out": sum(t.tokens_out for t in traces),
        }

    overall = {
        "total": len(scores),
        "pass_rate": _pass_rate(scores),
        "avg_value": _avg_value(scores),
    }

    per_type = {}
    for qtype, group in sorted(by_type.items()):
        per_type[qtype] = {
            "count": len(group),
            "pass_rate": _pass_rate(group),
            "avg_value": _avg_value(group),
            "components": {
                "retrieval_recall": _component_avg(group, "retrieval_recall"),
                "correctness":      _component_avg(group, "correctness"),
                "refusal":          _component_avg(group, "refusal"),
                "clarification":    _component_avg(group, "clarification"),
            },
            "trace": _trace_stats(group),
        }
        # Drop None components for cleanliness
        per_type[qtype]["components"] = {
            k: v for k, v in per_type[qtype]["components"].items() if v is not None
        }

    return {"overall": overall, "per_type": per_type}


# ── Output writers ───────────────────────────────────────────────────

def _write_json(path: Path, samples: list[Sample], results: list[Result],
                scores: list[Score], metrics: dict, metadata: dict) -> None:
    payload = {
        "metadata": metadata,
        "metrics": metrics,
        "rows": [
            {
                "sample_id": s.id,
                "question_type": s.question_type,
                "question": s.question,
                "expected_answer": s.expected_answer,
                "expected_chunks": list(s.expected_chunks),
                "agent_answer": r.answer,
                "score": {
                    "passed": sc.passed,
                    "value": sc.value,
                    "rationale": sc.rationale,
                    "components": sc.components,
                },
                "trace": {
                    "turns": r.trace.turns,
                    "tool_calls": [asdict(tc) for tc in r.trace.tool_calls],
                    "tokens_in": r.trace.tokens_in,
                    "tokens_out": r.trace.tokens_out,
                    "cached_tokens": r.trace.cached_tokens,
                },
                "cache_hit": r.cache_hit,
                "elapsed_seconds": r.elapsed_seconds,
            }
            for s, r, sc in zip(samples, results, scores)
        ],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _md_pct(x: float) -> str:
    return f"{x*100:.1f}%"


def _md_num(x: float | int | None, fmt: str = "{:.2f}") -> str:
    return "—" if x is None else fmt.format(x)


def _write_markdown(path: Path, samples: list[Sample], results: list[Result],
                    scores: list[Score], metrics: dict, metadata: dict) -> None:
    lines: list[str] = []
    lines.append(f"# Eval Report — {metadata['label']}")
    lines.append("")
    lines.append(f"- **Generated:** {metadata['timestamp']}")
    lines.append(f"- **Dataset:** `{metadata['dataset_path']}` ({metrics['overall']['total']} rows)")
    lines.append(f"- **Agent:** `{metadata['agent_label']}`")
    lines.append(f"- **Judge model:** `{metadata['judge_model']}`")
    lines.append("")

    # Headline
    overall = metrics["overall"]
    lines.append("## Headline")
    lines.append("")
    lines.append(f"- **Overall pass rate:** {_md_pct(overall['pass_rate'])}  "
                 f"({sum(1 for s in scores if s.passed)} / {overall['total']})")
    lines.append(f"- **Overall avg value:** {_md_num(overall['avg_value'])}")
    lines.append("")

    # Per-type table
    lines.append("## Per-category metrics")
    lines.append("")
    lines.append("| Type | Count | Pass rate | Avg value | Avg recall | Avg correctness | Refusal | Clarification |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for qtype, m in metrics["per_type"].items():
        comps = m.get("components", {})
        lines.append(
            f"| `{qtype}` | {m['count']} | {_md_pct(m['pass_rate'])} | {_md_num(m['avg_value'])} | "
            f"{_md_num(comps.get('retrieval_recall'))} | {_md_num(comps.get('correctness'))} | "
            f"{_md_num(comps.get('refusal'))} | {_md_num(comps.get('clarification'))} |"
        )
    lines.append("")

    # Trace stats
    lines.append("## Trace statistics")
    lines.append("")
    lines.append("| Type | Avg tool calls | Max tool calls | Avg turns | Total tokens (in / out) |")
    lines.append("|---|---:|---:|---:|---:|")
    for qtype, m in metrics["per_type"].items():
        t = m.get("trace", {})
        if not t:
            continue
        lines.append(
            f"| `{qtype}` | {_md_num(t.get('avg_tool_calls'))} | {t.get('max_tool_calls', 0)} | "
            f"{_md_num(t.get('avg_turns'))} | {t.get('total_tokens_in', 0):,} / {t.get('total_tokens_out', 0):,} |"
        )
    lines.append("")

    # Failures
    failures = [(s, r, sc) for s, r, sc in zip(samples, results, scores) if not sc.passed]
    lines.append(f"## Failures ({len(failures)})")
    lines.append("")
    if not failures:
        lines.append("_All rows passed._")
    else:
        for sample, result, score in failures:
            lines.append(f"### `{sample.id}` — `{sample.question_type}` — value {score.value:.2f}")
            lines.append("")
            lines.append(f"**Question:** {sample.question}")
            lines.append("")
            lines.append(f"**Judge rationale:** {score.rationale}")
            lines.append("")
            lines.append(f"**Agent answer (preview):** {result.answer[:400].strip()}{'…' if len(result.answer) > 400 else ''}")
            lines.append("")
            tools_used = ", ".join(f"`{tc.name}`" for tc in result.trace.tool_calls[:8])
            lines.append(f"**Tool calls ({len(result.trace.tool_calls)}):** {tools_used}{' …' if len(result.trace.tool_calls) > 8 else ''}")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


# ── Public API ───────────────────────────────────────────────────────

def generate(
    samples: list[Sample],
    results: list[Result],
    scores: list[Score],
    *,
    label: str,
    dataset_path: str,
    agent_label: str,
    judge_model: str,
    reports_root: Path,
) -> Path:
    """Generate both JSON and Markdown reports under reports_root/<label>/<timestamp>/.

    Returns the directory where the reports were written.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = reports_root / label / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    metrics = _aggregate(scores, results)
    metadata = {
        "label": label,
        "timestamp": timestamp,
        "dataset_path": dataset_path,
        "agent_label": agent_label,
        "judge_model": judge_model,
    }

    _write_json(out_dir / "report.json", samples, results, scores, metrics, metadata)
    _write_markdown(out_dir / "report.md", samples, results, scores, metrics, metadata)
    return out_dir
