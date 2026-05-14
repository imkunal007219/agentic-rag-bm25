"""Judge-v2 validation against frozen human grades.

After drafting a new judge prompt (judge-v2) to address the central-tendency
bias found in `calibration_partial.md`, we re-scored v5's cached agent
answers with judge-v2 and compared agreement against the SAME blind
hand-grades in `calibration_partial_worksheet.md`. The hand-grades are the
fixed reference; the judge is what's on trial.

This script reports, on the 18 v5 rows the grader hand-graded:
  - judge-v1 agreement (exact + within-one-bucket)
  - judge-v2 agreement (exact + within-one-bucket)
  - direction of disagreement under each judge
  - which rows changed v1 -> v2 and whether the change moved toward or
    away from the human grade

A judge "fix" succeeds only if exact-match agreement goes UP and the
systematic direction of the old disagreements (everything collapsing
toward 0.7) weakens.

Usage:  python evals/calibration_judgev2_check.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
JUDGE_V1 = ROOT / "reports/v5-evidence-gated-refusal/20260514T102955Z/report.json"
JUDGE_V2 = ROOT / "reports/v5-judgev2/20260514T112655Z/report.json"
WORKSHEET = ROOT / "calibration_partial_worksheet.md"

PRIMED = {"q002", "q005", "q018", "q020", "q029", "q030",
          "q034", "q035", "q040", "q054", "q056", "q060"}
B4 = [0.0, 0.4, 0.7, 1.0]
B3 = [0.0, 0.5, 1.0]


def snap(v: float, buckets: list[float]) -> int:
    return min(range(len(buckets)), key=lambda i: abs(buckets[i] - v))


def load(p: Path) -> dict:
    return {r["sample_id"]: r for r in json.load(open(p))["rows"]}


def jscore(r: dict) -> float:
    qt = r["question_type"]
    comp = r["score"].get("components", {})
    if qt in ("single_hop", "multi_hop"):
        return comp.get("correctness", r["score"]["value"])
    return r["score"]["value"]


def parse_hand_grades(text: str) -> dict[str, tuple[str, float]]:
    """Returns {sid: (question_type, hand_grade)} for v5 rows only."""
    out = {}
    blocks = re.split(r"^## \d+\.\s+(?=`q\d+`)", text, flags=re.M)[1:]
    for blk in blocks:
        m = re.match(r"`(q\d+)`\s+—\s+`([a-z_]+)`\s+—\s+run:(v\d)", blk)
        if not m:
            continue
        sid, qt, run = m.group(1), m.group(2), m.group(3)
        sm = re.search(r"\*\*Your score:\*\*\s*([0-9]*\.?[0-9]+)", blk)
        if run == "v5" and sm:
            out[sid] = (qt, float(sm.group(1)))
    return out


def main() -> None:
    v1 = load(JUDGE_V1)
    v2 = load(JUDGE_V2)
    hand = parse_hand_grades(WORKSHEET.read_text())

    print(f"v5 rows hand-graded: {len(hand)}")
    print(f"{'row':<8}{'type':<11}{'mine':>5}{'j1':>6}{'j2':>6}  "
          f"{'j1 match':<10}{'j2 match':<10}{'tag'}")
    print("-" * 64)

    rows = []
    for sid, (qt, mine) in sorted(hand.items()):
        buckets = B3 if qt in ("no_answer", "ambiguous") else B4
        j1 = jscore(v1[sid])
        j2 = jscore(v2[sid])
        d1 = abs(snap(mine, buckets) - snap(j1, buckets))
        d2 = abs(snap(mine, buckets) - snap(j2, buckets))
        m1 = "EXACT" if d1 == 0 else ("CLOSE" if d1 == 1 else "DIVERGENT")
        m2 = "EXACT" if d2 == 0 else ("CLOSE" if d2 == 1 else "DIVERGENT")
        tag = "PRIMED" if sid in PRIMED else "clean"
        rows.append(dict(sid=sid, qt=qt, mine=mine, j1=j1, j2=j2, d1=d1, d2=d2))
        print(f"{sid:<8}{qt:<11}{mine:>5.2f}{j1:>6.2f}{j2:>6.2f}  "
              f"{m1:<10}{m2:<10}{tag}")

    def stats(rs, key):
        return (sum(1 for r in rs if r[key] == 0),
                sum(1 for r in rs if r[key] <= 1),
                len(rs))

    print("-" * 64)
    e1, w1, n = stats(rows, "d1")
    e2, w2, _ = stats(rows, "d2")
    print(f"judge-v1 vs hand-grades:  exact {e1}/{n} ({100*e1/n:.0f}%)   "
          f"within-1 {w1}/{n} ({100*w1/n:.0f}%)")
    print(f"judge-v2 vs hand-grades:  exact {e2}/{n} ({100*e2/n:.0f}%)   "
          f"within-1 {w2}/{n} ({100*w2/n:.0f}%)")
    print()

    def direction(rs, jkey):
        return (sum(1 for r in rs if r[jkey] < r["mine"]),
                sum(1 for r in rs if r[jkey] > r["mine"]))

    l1, h1 = direction(rows, "j1")
    l2, h2 = direction(rows, "j2")
    print(f"judge-v1 disagreement direction:  {l1} judge-lower / {h1} judge-higher")
    print(f"judge-v2 disagreement direction:  {l2} judge-lower / {h2} judge-higher")
    print()

    changed = [r for r in rows if r["j1"] != r["j2"]]
    print(f"Rows where judge-v2 differs from judge-v1: {len(changed)}")
    toward = away = same = 0
    for r in changed:
        d_to_mine_v1 = abs(r["j1"] - r["mine"])
        d_to_mine_v2 = abs(r["j2"] - r["mine"])
        if d_to_mine_v2 < d_to_mine_v1:
            label = "TOWARD mine"
            toward += 1
        elif d_to_mine_v2 > d_to_mine_v1:
            label = "AWAY from mine"
            away += 1
        else:
            label = "same dist"
            same += 1
        print(f"  {r['sid']} ({r['qt']}): j1={r['j1']:.2f} -> j2={r['j2']:.2f}  "
              f"| mine={r['mine']:.2f}  [{label}]")
    print()
    print(f"  changes toward hand-grade: {toward}")
    print(f"  changes away from hand-grade: {away}")
    print(f"  unchanged distance: {same}")
    print()

    verdict = "WIN" if e2 > e1 else ("REGRESSION" if e2 < e1 else "NEUTRAL")
    print(f"Verdict: judge-v2 exact-match agreement vs judge-v1 -> {verdict}")
    if e2 <= e1:
        print("  -> do not ship judge-v2 as-is; iterate to judge-v3")


if __name__ == "__main__":
    main()
