# Judge calibration — partial-credit regime

The Day-1 calibration (`calibration.md`) measured the LLM judge on the
**easy regime**: a stratified random sample that was almost all clean 1.0s.
It passed 10/10 but explicitly left a gap — *"partial-credit calibration
pending"*. This note closes that gap.

## Method

- **Sample:** every row the judge scored strictly between 0 and 1 across the
  v4 (60-row) and v5 (60-row) eval runs — **35 rows**. This is the regime
  where judge disagreement actually lives: the `0.4` / `0.7` buckets for
  single/multi-hop and `0.5` for ambiguous.
- **Protocol:** blind hand-grading. The grader scored each row from the
  question, reference answer, and agent answer **without** seeing the judge
  score, then scores were compared.
- **Compared quantity:** the judge's `components.correctness` for
  single/multi-hop (the worksheet buckets are the correctness rubric, not
  the multi-hop blended value); `score.value` for ambiguous.
- **Contamination control:** the grader had already seen the judge score
  for 15 of the 35 rows earlier in the working session. Those are tagged
  `PRIMED`; the 20 `CLEAN` rows are the honest blind sample and are the
  headline. A calibration that hides its own contamination is worse than
  none.
- **Pass criterion:** >= 80% within-one-bucket agreement on the clean
  sample (same bar as Day 1).

Reproducible via `calibration_partial_worksheet.md`,
`calibration_partial_key.md`, and `calibration_partial_agreement.py`.

## Result

| Sample | Exact-match | Within-one-bucket |
|---|---:|---:|
| **CLEAN (headline, n=20)** | 50% | **100%** |
| PRIMED (n=15) | 73% | 100% |
| ALL (n=35) | 60% | 100% |

Divergent rows (delta >= 2 buckets): **0**.

**The judge passes the calibration bar** — 100% within-one-bucket on the
clean sample, well above 80%. Partial-credit scores are usable.

## The finding — central-tendency bias

Exact-match is only 50% on the clean sample, and the misses are **not
random**. Of 14 disagreements across all 35 rows, **11 are the judge
scoring lower than the grader, 3 higher, 0 divergent** — and every single
one moves *toward 0.7*:

- 10x the grader said `1.0`, the judge said `0.7` (q003 x2, q020, q034,
  q036, q046, q052 x2, q053, q055)
- 3x the grader said `0.4`, the judge said `0.7` (q016 x2, q056)
- 1x the grader said `1.0`, the judge said `0.5` (q060 — ambiguous)

The judge **compresses toward the middle**. It under-credits excellent
answers (parks clean 1.0s at 0.7) and over-credits weak multi-hop answers
(lifts genuine 0.4s — half the question answered, half refused — to 0.7).
It never scored *more* extreme than the grader. This is textbook
LLM-as-judge central-tendency bias.

## What this means for the eval

1. **single_hop pass/fail is trustworthy.** The dominant error is `1.0 ->
   0.7` compression, and `0.7` still passes the `correctness >= 0.7` gate.
   Pass/fail is not flipped; only the avg-value metric is depressed.
2. **multi_hop pass rate is mildly inflated.** The judge lifts some true
   `0.4` multi-hop answers to `0.7`, which is a false pass (q016: the agent
   answered one hop and refused the other — a genuine partial — and the
   judge passed it).
3. **ambiguous scores are unreliable at the high end.** q060/v4 is a clean
   case: the agent recognized the ambiguity, surfaced the alternatives, and
   asked for clarification — the exact expected meta-behaviour — and the
   judge scored it `0.5` (fail). Graded `1.0` blind. **The low ambiguous
   pass rate is partly a judge artifact, not purely an agent weakness.**
4. **Avg-value metrics are systematically depressed.** Do not over-read
   them; the central-tendency bias pulls them down.

## Actionable

- **v6 should not primarily target the CLARIFICATION policy.** The agent
  handles ambiguous better than the score shows; the bottleneck there is
  partly the judge. v6 stays focused on the Cluster-B escape valve.
- **The judge rubric needs a refinement pass** — sharper `1.0` vs `0.7`
  criteria, and ideally a few-shot anchor per bucket — to pull it off the
  0.7 attractor. Tracked as a separate iteration, not folded into v6.
- When quoting eval numbers: **pass rates for single_hop are solid;
  multi_hop is mildly optimistic; ambiguous is judge-limited; avg-value is
  conservative across the board.**

## What this does NOT establish

- Inter-grader reliability (one human grader).
- Whether the central-tendency bias is stable across corpora / domains.
- The judge's behaviour on a *failure-weighted* sample drawn deliberately
  from the hardest rows (the clean sample here is the natural
  partial-credit distribution, not an adversarial one).
