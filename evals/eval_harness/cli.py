"""CLI entry point for the eval harness.

Usage:
    python -m eval_harness --label v1-bm25
    python -m eval_harness --label v1-bm25 --limit 4 --types single_hop
    python -m eval_harness --label v1-bm25 --force

What it does, end to end:
    1. Load + validate the dataset.
    2. Build the agent_fn closure (wraps run_agent against the guidance index).
    3. Run the agent on each sample (cache_hit if previously cached).
    4. Score each (Sample, Result) pair with the type-appropriate scorer.
    5. Write JSON + Markdown reports under evals/reports/<label>/<ts>/.
    6. Print a one-page summary to stderr.

Design note:
    The agent wiring is done here and only here. The runner accepts a
    callable; the scorer accepts results. Only this file knows about
    `lib.expert_agent.run_agent`, `ExpertIndex`, KB_ROOT, etc.
    Tomorrow when we want to evaluate a vector-DB RAG, we replace
    THIS file (or add a sibling) and reuse everything else.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def _build_agent_fn(domain: str, kb_root: Path, verbose: bool):
    """Wire run_agent into the (question) -> (answer, trace) contract."""
    # Defer imports so the harness can be loaded for non-run commands
    # (e.g., schema validation) without requiring the agent's deps.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
    from expert_index import get_or_build_index
    from expert_agent import run_agent

    kb_dir = kb_root / domain
    index = get_or_build_index(kb_dir, domain)

    def agent_fn(question: str):
        return run_agent(
            question, index, domain=domain,
            verbose=verbose, return_trace=True,
        )

    return agent_fn


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="eval_harness",
        description="Run the agentic-rag-bm25 eval and produce reports.",
    )
    p.add_argument("--label", required=True,
                   help="Run label (e.g. 'v1-bm25-default'). Used for cache + report dirs.")
    p.add_argument("--dataset", default="evals/groundtruth.jsonl",
                   help="Path to groundtruth.jsonl (default: evals/groundtruth.jsonl)")
    p.add_argument("--domain", default="guidance",
                   help="Knowledge-base domain to evaluate (default: guidance)")
    p.add_argument("--kb-root",
                   default=os.environ.get("KB_ROOT", str(Path.home() / "knowledge-bases")),
                   help="Root directory of knowledge bases (default: $KB_ROOT or ~/knowledge-bases)")
    p.add_argument("--cache-root", default="evals/cache",
                   help="Cache root (default: evals/cache)")
    p.add_argument("--reports-root", default="evals/reports",
                   help="Reports root (default: evals/reports)")
    p.add_argument("--force", action="store_true",
                   help="Ignore cache, re-run the agent on every sample")
    p.add_argument("--limit", type=int, default=None,
                   help="Process only the first N samples (debug)")
    p.add_argument("--types", default=None,
                   help="Comma-separated question types to include "
                        "(e.g. 'single_hop,multi_hop'). Default: all.")
    p.add_argument("--verbose", action="store_true",
                   help="Print agent tool calls to stderr")
    args = p.parse_args(argv)

    # Imports deferred so --help doesn't require runtime deps
    from .dataset import load_dataset
    from .runner import run_all
    from .scorer import score_sample, JUDGE_MODEL
    from .report import generate

    # 1. Load + filter dataset
    samples = load_dataset(args.dataset)
    if args.types:
        wanted = set(args.types.split(","))
        samples = [s for s in samples if s.question_type in wanted]
    if args.limit is not None:
        samples = samples[:args.limit]
    if not samples:
        print("No samples selected after filtering.", file=sys.stderr)
        return 2

    print(f"\n→ Running {len(samples)} samples with label {args.label!r} "
          f"on domain {args.domain!r}", file=sys.stderr)
    if args.force:
        print("  [--force] cache will be ignored and overwritten", file=sys.stderr)
    print(file=sys.stderr)

    # 2. Build the agent function
    agent_fn = _build_agent_fn(args.domain, Path(args.kb_root), args.verbose)

    # 3. Run the agent
    cache_dir = Path(args.cache_root) / args.label
    results = run_all(samples, agent_fn, cache_dir, force=args.force, progress=True)

    # 4. Score
    print(f"\n→ Scoring with judge {JUDGE_MODEL!r}", file=sys.stderr)
    scores = []
    for i, (sample, result) in enumerate(zip(samples, results), start=1):
        print(f"  [{i:>2}/{len(samples)}] {sample.id}…", end="", flush=True, file=sys.stderr)
        s = score_sample(sample, result)
        marker = "PASS" if s.passed else "FAIL"
        print(f" {marker} (value={s.value:.2f})", file=sys.stderr)
        scores.append(s)

    # 5. Report
    out_dir = generate(
        samples, results, scores,
        label=args.label,
        dataset_path=args.dataset,
        agent_label="kimi-k2.5 + BM25 (lib/expert_agent.run_agent)",
        judge_model=JUDGE_MODEL,
        reports_root=Path(args.reports_root),
    )

    # 6. One-page summary
    passed = sum(1 for s in scores if s.passed)
    total = len(scores)
    print(f"\n===== Summary =====", file=sys.stderr)
    print(f"  Pass rate: {passed}/{total} ({passed/total*100:.1f}%)", file=sys.stderr)
    by_type: dict[str, list] = {}
    for s in scores:
        by_type.setdefault(s.question_type, []).append(s)
    for qtype, group in sorted(by_type.items()):
        p_n = sum(1 for s in group if s.passed)
        print(f"    {qtype:12} {p_n:>2}/{len(group):<2}  "
              f"(avg value {sum(s.value for s in group)/len(group):.2f})",
              file=sys.stderr)
    print(f"\n  Reports written to: {out_dir}", file=sys.stderr)
    print(f"    - {out_dir / 'report.md'}", file=sys.stderr)
    print(f"    - {out_dir / 'report.json'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
