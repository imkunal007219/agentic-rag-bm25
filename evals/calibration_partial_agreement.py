"""Partial-credit judge calibration — agreement analysis.

Compares blind hand-grades in `calibration_partial_worksheet.md` against the
LLM-judge scores in the v4 and v5 eval reports, restricted to the
partial-credit regime (rows the judge scored strictly between 0 and 1).

This is the follow-up to `calibration_agreement.py` (the Day-1 easy-regime
pass). The easy-regime pass measured the judge on rows that were almost all
clean 1.0s; this pass measures it where disagreement actually lives —
0.4 / 0.7 buckets for single/multi-hop, 0.5 for ambiguous.

The grader was primed on a subset of rows (had seen the judge score earlier
in the working session). Those rows are tagged PRIMED; CLEAN rows are the
honest blind sample and are reported as the headline.

Compared quantity:
  single_hop / multi_hop -> judge `components.correctness`
  ambiguous              -> judge `score.value`
(The grader's worksheet buckets are the correctness rubric, not the
multi-hop blended value.)

Usage:  python evals/calibration_partial_agreement.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
REPORTS = {
    "v4": ROOT / "reports/v4-three-policies-60row/20260514T053149Z/report.json",
    "v5": ROOT / "reports/v5-evidence-gated-refusal/20260514T102955Z/report.json",
}
WORKSHEET = ROOT / "calibration_partial_worksheet.md"

PRIMED = {"q002", "q005", "q018", "q020", "q029", "q030",
          "q034", "q035", "q040", "q054", "q056", "q060"}

B4 = [0.0, 0.4, 0.7, 1.0]   # single_hop, multi_hop  (correctness rubric)
B3 = [0.0, 0.5, 1.0]        # no_answer, ambiguous


def snap(v: float, buckets: list[float]) -> int:
    return min(range(len(buckets)), key=lambda i: abs(buckets[i] - v))


def load_rows(path: Path) -> dict:
    return {r["sample_id"]: r for r in json.load(open(path))["rows"]}


def judge_score(r: dict) -> float:
    qt = r["question_type"]
    comp = r["score"].get("components", {})
    if qt in ("single_hop", "multi_hop"):
        return comp.get("correctness", r["score"]["value"])
    return r["score"]["value"]


def parse_worksheet(text: str) -> list[tuple[str, str, float | None]]:
    """Returns [(sample_id, run, your_score|None)] in worksheet order."""
    out = []
    # split only on worksheet row headers ("## 12. `q022` ..."), NOT on the
    # agent answers' own markdown headers ("## 1. Launch Phase")
    blocks = re.split(r"^## \d+\.\s+(?=`q\d+`)", text, flags=re.M)[1:]
    for blk in blocks:
        m = re.match(r"`(q\d+)`\s+—\s+`([a-z_]+)`\s+—\s+run:(v\d)", blk)
        if not m:
            continue
        sid, run = m.group(1), m.group(3)
        sm = re.search(r"\*\*Your score:\*\*\s*([0-9]*\.?[0-9]+)", blk)
        score = float(sm.group(1)) if sm else None
        out.append((sid, run, score))
    return out


def main() -> None:
    runs = {k: load_rows(v) for k, v in REPORTS.items()}
    graded = parse_worksheet(WORKSHEET.read_text())

    rows = []
    for sid, run, mine in graded:
        if mine is None:
            print(f"{sid}/{run}: no hand grade — fill the worksheet first.")
            sys.exit(1)
        r = runs[run][sid]
        qt = r["question_type"]
        js = judge_score(r)
        buckets = B3 if qt in ("no_answer", "ambiguous") else B4
        delta = abs(snap(mine, buckets) - snap(js, buckets))
        rows.append(dict(sid=sid, run=run, qt=qt, primed=sid in PRIMED,
                         mine=mine, judge=js, delta=delta))

    print(f"{'row':<10}{'type':<11}{'mine':>6}{'judge':>7}{'d':>3}  {'match':<16}{'tag'}")
    print("-" * 56)
    for x in rows:
        mark = "EXACT" if x["delta"] == 0 else ("CLOSE" if x["delta"] == 1 else "** DIVERGENT **")
        tag = "PRIMED" if x["primed"] else "clean"
        print(f"{x['sid'] + '/' + x['run']:<10}{x['qt']:<11}"
              f"{x['mine']:>6.2f}{x['judge']:>7.2f}{x['delta']:>3}  {mark:<16}{tag}")

    def agree(sub):
        if not sub:
            return 0, 0, 0
        return (sum(1 for x in sub if x["delta"] == 0),
                sum(1 for x in sub if x["delta"] <= 1),
                len(sub))

    clean = [x for x in rows if not x["primed"]]
    primed = [x for x in rows if x["primed"]]
    print("-" * 56)
    for label, sub in [("CLEAN (headline)", clean), ("PRIMED", primed), ("ALL", rows)]:
        ex, wi, n = agree(sub)
        print(f"{label:<18} exact {ex}/{n} ({100 * ex / n:.0f}%)   "
              f"within-1 {wi}/{n} ({100 * wi / n:.0f}%)")

    # direction of disagreement — the signal that matters
    disagree = [x for x in rows if x["delta"] >= 1]
    judge_lower = sum(1 for x in disagree if x["judge"] < x["mine"])
    judge_higher = sum(1 for x in disagree if x["judge"] > x["mine"])
    print()
    print(f"Disagreements: {len(disagree)}  "
          f"(judge lower than grader: {judge_lower}, judge higher: {judge_higher})")
    div = [x for x in rows if x["delta"] >= 2]
    print(f"Divergent (d>=2): {len(div)}")
    if div:
        for x in div:
            print(f"  {x['sid']}/{x['run']}: mine={x['mine']} judge={x['judge']}")

    ex, wi, n = agree(clean)
    print()
    print("PASS" if wi / n >= 0.8 else "FAIL",
          "— within-one-bucket >= 80% on the clean sample"
          if wi / n >= 0.8 else "— within-one-bucket below 80%")


if __name__ == "__main__":
    main()
