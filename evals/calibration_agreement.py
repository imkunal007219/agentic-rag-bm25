"""Compare hand-grades from calibration_worksheet.md against the LLM-judge
scores in calibration_key.md. Prints per-row comparison and overall
agreement rates (exact-match + within-one-bucket).

Usage:  python evals/calibration_agreement.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


BUCKETS_4 = [0.0, 0.4, 0.7, 1.0]   # single_hop, multi_hop
BUCKETS_3 = [0.0, 0.5, 1.0]        # no_answer, ambiguous


def bucket_index(score: float, buckets: list[float]) -> int:
    # snap to nearest legal bucket
    return min(range(len(buckets)), key=lambda i: abs(buckets[i] - score))


def parse_worksheet(text: str) -> list[tuple[str, str, float | None]]:
    """Returns list of (sample_id, question_type, your_score | None)."""
    rows = []
    blocks = re.split(r"^## \d+\.\s+", text, flags=re.M)[1:]
    for blk in blocks:
        m = re.match(r"`(q\d+)`\s+—\s+`([a-z_]+)`", blk)
        if not m:
            continue
        sid, qtype = m.group(1), m.group(2)
        sm = re.search(r"\*\*Your score:\*\*[\s_]*([0-9]+(?:\.[0-9]+)?)", blk)
        score = float(sm.group(1)) if sm else None
        rows.append((sid, qtype, score))
    return rows


def parse_key(text: str) -> dict[str, float]:
    out = {}
    blocks = re.split(r"^## \d+\.\s+", text, flags=re.M)[1:]
    for blk in blocks:
        m = re.match(r"`(q\d+)`", blk)
        if not m:
            continue
        sm = re.search(r"Judge score:\s+\*\*([0-9.]+)\*\*", blk)
        if sm:
            out[m.group(1)] = float(sm.group(1))
    return out


def main():
    root = Path(__file__).parent
    worksheet = parse_worksheet((root / "calibration_worksheet.md").read_text())
    key = parse_key((root / "calibration_key.md").read_text())

    print(f"{'id':<6} {'type':<11} {'you':>5}  {'judge':>5}  {'Δbuckets':>9}  match")
    print("-" * 60)

    exact = 0
    within = 0
    graded = 0
    for sid, qtype, you in worksheet:
        judge = key.get(sid)
        if you is None or judge is None:
            print(f"{sid:<6} {qtype:<11} {'-':>5}  {judge if judge is not None else '-':>5}  {'-':>9}  (skipped — no hand grade)")
            continue
        graded += 1
        buckets = BUCKETS_3 if qtype in ("no_answer", "ambiguous") else BUCKETS_4
        bi_you = bucket_index(you, buckets)
        bi_jud = bucket_index(judge, buckets)
        delta = abs(bi_you - bi_jud)
        mark = "EXACT" if delta == 0 else ("CLOSE" if delta == 1 else "DIVERGENT")
        if delta == 0:
            exact += 1
        if delta <= 1:
            within += 1
        print(f"{sid:<6} {qtype:<11} {you:>5.2f}  {judge:>5.2f}  {delta:>9d}  {mark}")

    print("-" * 60)
    if graded == 0:
        print("No hand grades found. Fill in **Your score:** values in calibration_worksheet.md.")
        sys.exit(1)
    print(f"Graded:           {graded}/10")
    print(f"Exact match:      {exact}/{graded}  ({100*exact/graded:.0f}%)")
    print(f"Within 1 bucket:  {within}/{graded}  ({100*within/graded:.0f}%)")
    print()
    if graded == 10 and within / graded >= 0.8:
        print("PASS — judge is calibrated (≥80% within-one-bucket).")
    elif graded == 10:
        print("FAIL — judge agreement below 80%. Inspect divergent rows and tighten the rubric.")


if __name__ == "__main__":
    main()
