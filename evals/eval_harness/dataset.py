"""Dataset loader and validator for the eval harness.

Reads `evals/groundtruth.jsonl` into a list of typed Sample objects,
enforcing the schema contract documented in `evals/schema.md`.

Why a typed loader and not just `json.load`?
    - Catches schema violations at load time instead of at scoring time.
      A missing field at scoring time is a 30-row run that fails on
      row 27 with a cryptic KeyError. Validation at load time fails
      immediately with a clear message.
    - Gives downstream code (runner, scorer) a typed contract — IDE
      autocomplete, type checking, and self-documenting signatures.
    - `Sample` is the canonical name in eval frameworks (Inspect,
      lm-evaluation-harness). Using the standard term lowers cognitive
      load when reading this code alongside those libraries.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Literal


QuestionType = Literal["single_hop", "multi_hop", "no_answer", "ambiguous"]
VALID_TYPES: set[str] = {"single_hop", "multi_hop", "no_answer", "ambiguous"}


@dataclass(frozen=True)
class Sample:
    """One row of the ground-truth dataset.

    `frozen=True` makes samples immutable — the dataset is read-only
    once loaded, so mutating a Sample anywhere downstream is a bug.
    Freezing surfaces such bugs as AttributeError instead of letting
    them silently corrupt a run.
    """
    id: str
    question: str
    expected_answer: str | None
    expected_chunks: tuple[str, ...]   # tuple, not list — hashable + immutable
    question_type: QuestionType
    notes: str = ""


def validate_sample(s: Sample) -> list[str]:
    """Return a list of validation error messages for `s`.

    Empty list means the sample is valid. The rules mirror the
    "Validation rules" section of evals/schema.md verbatim — if you
    change one here, change it there.
    """
    errs: list[str] = []

    if s.question_type not in VALID_TYPES:
        errs.append(f"{s.id}: question_type {s.question_type!r} not in {VALID_TYPES}")

    # Rule: no_answer rows must have null expected_answer
    if s.question_type == "no_answer" and s.expected_answer is not None:
        errs.append(f"{s.id}: no_answer rows must have expected_answer=null")

    # Rule: ambiguous rows must describe expected meta-behaviour
    if s.question_type == "ambiguous" and s.expected_answer is None:
        errs.append(f"{s.id}: ambiguous rows must have a non-null expected_answer "
                    f"(describing the expected meta-behaviour)")

    # Rule: expected_chunks must be empty for no_answer / ambiguous, non-empty otherwise
    if s.question_type in {"no_answer", "ambiguous"}:
        if s.expected_chunks:
            errs.append(f"{s.id}: {s.question_type} rows must have empty expected_chunks")
    else:
        if not s.expected_chunks:
            errs.append(f"{s.id}: {s.question_type} rows must have non-empty expected_chunks")

    return errs


def load_dataset(path: str | Path) -> list[Sample]:
    """Load and validate the JSONL dataset.

    Raises ValueError on any schema violation — fail-fast at load time
    rather than surfacing a broken row mid-eval.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    samples: list[Sample] = []
    seen_ids: set[str] = set()
    all_errs: list[str] = []

    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                all_errs.append(f"line {lineno}: JSON parse error — {e}")
                continue

            try:
                sample = Sample(
                    id=obj["id"],
                    question=obj["question"],
                    expected_answer=obj.get("expected_answer"),
                    expected_chunks=tuple(obj.get("expected_chunks", [])),
                    question_type=obj["question_type"],
                    notes=obj.get("notes", ""),
                )
            except KeyError as e:
                all_errs.append(f"line {lineno}: missing required field {e}")
                continue

            if sample.id in seen_ids:
                all_errs.append(f"line {lineno}: duplicate id {sample.id!r}")
                continue
            seen_ids.add(sample.id)

            all_errs.extend(validate_sample(sample))
            samples.append(sample)

    if all_errs:
        joined = "\n  ".join(all_errs)
        raise ValueError(f"Dataset has {len(all_errs)} validation error(s):\n  {joined}")

    return samples


def filter_by_type(samples: Iterable[Sample], qtype: QuestionType) -> list[Sample]:
    """Return only samples of the given question_type."""
    return [s for s in samples if s.question_type == qtype]


def summary(samples: list[Sample]) -> dict:
    """Aggregate counts for a quick sanity-check after loading."""
    by_type: dict[str, int] = {}
    by_chunks: dict[int, int] = {}
    for s in samples:
        by_type[s.question_type] = by_type.get(s.question_type, 0) + 1
        k = len(s.expected_chunks)
        by_chunks[k] = by_chunks.get(k, 0) + 1
    return {
        "total": len(samples),
        "by_type": dict(sorted(by_type.items())),
        "by_chunk_count": dict(sorted(by_chunks.items())),
    }


# ── Script entry point: `python -m eval_harness.dataset` ─────────────

def _main() -> None:
    import argparse, sys
    p = argparse.ArgumentParser(description="Load + validate the eval dataset")
    p.add_argument("--path", default="evals/groundtruth.jsonl",
                   help="Path to groundtruth.jsonl")
    args = p.parse_args()

    try:
        samples = load_dataset(args.path)
    except (FileNotFoundError, ValueError) as e:
        print(f"FAILED: {e}", file=sys.stderr)
        sys.exit(1)

    stats = summary(samples)
    print(f"Loaded {stats['total']} samples from {args.path}")
    print(f"By type: {stats['by_type']}")
    print(f"By expected_chunks count: {stats['by_chunk_count']}")
    print("All rows pass schema validation.")


if __name__ == "__main__":
    _main()
