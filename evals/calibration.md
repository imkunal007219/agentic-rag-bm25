# Judge calibration — v4-three-policies

The eval harness uses Claude Sonnet 4.6 as an LLM judge to score correctness, refusal, and clarification behaviour on a 30-row hand-validated dataset. Before trusting any score the judge produces, the judge itself has to be calibrated against human grading. This note documents the calibration pass.

## Method

- **Sample:** 10 rows, stratified random sample from v4-three-policies. Composition: 5 single_hop, 3 multi_hop, 1 no_answer, 1 ambiguous. Seed `42` for reproducibility.
- **Protocol:** blind hand-grading. The grader read each row (question, reference, agent answer) and assigned a score on the harness rubric WITHOUT seeing the judge's score. Scores were then compared.
- **Rubric:** four-bucket for single/multi-hop (`0.0 / 0.4 / 0.7 / 1.0`), three-bucket for no_answer/ambiguous (`0.0 / 0.5 / 1.0`).
- **Agreement metrics:** exact-match (same bucket) and within-one-bucket (adjacent bucket).
- **Pass criterion:** ≥80% within-one-bucket agreement.

Reproducible via `evals/calibration_worksheet.md`, `evals/calibration_key.md`, and `evals/calibration_agreement.py`.

## Result

| Metric | Score |
|---|---:|
| Exact-match agreement | **10/10 (100%)** |
| Within-one-bucket agreement | **10/10 (100%)** |
| Sample failures present | 1 (q002, both graded 0.0) |
| Sample passes present | 9 (all graded 1.0 by both) |

The judge passed the calibration bar cleanly on this sample.

## Honest caveats

This number measures the judge in the **easy regime**:
- Nine of the ten sampled rows were judge-passes — the natural composition of a 86.7%-pass-rate run reflects this. Stratified random sampling on a high-pass-rate dataset surfaces few edge cases.
- Zero rows in this sample received a partial-credit score (`0.4` or `0.7`). Judge calibration on partial-credit calls — the cases most prone to disagreement — is therefore **not measured by this pass**.
- A second, failure-weighted sample (drawing from v1/v2/v3 failures across all categories) is planned to stress-test the judge on borderline rows.

The number to quote when discussing this work: **100% on the easy regime; partial-credit calibration pending.**

## Substantive observations from the grading

**1. Judge-human alignment is in the lenient direction.**
On q001 the agent cited §6.1's definition of "guidance law" ("the algorithm by which the desired geometrical rule is implemented") instead of the reference's §1.1 phrasing ("algorithm that determines the required commanded missile acceleration"). Both definitions are correct. Both grader and judge awarded `1.0`. This implies the system rewards semantic correctness over phrasing-match — a deliberate choice, but one consumers of the score should know about.

**2. The judge correctly identifies the one true failure.**
q002 ("first missile to use parallel navigation, and year") was the only failing row in the sample. The agent refused; the answer (Lark missile, 1950) is in §1.2 of the corpus. Judge scored `0.0`. Hand-grade `0.0`. The judge did not soften the score because the agent's refusal language was polite — it scored on outcome.

**3. The judge's `correctness` signal can be trusted as the primary pass gate.**
This calibration was conducted after the scorer was changed from `passed = recall>=1.0 AND correctness>=0.7` to `passed = correctness>=0.7` (for single_hop). The calibration validates that decision: the judge's correctness call is reliable enough to be the pass gate when retrieval recall and judged correctness disagree (the q006-style case where the agent finds an equivalent-but-different chunk).

## What this calibration does NOT establish

- Reliability on `0.4` / `0.7` partial-credit calls
- Reliability on the no_answer rubric's `0.5` (partial refusal) bucket
- Reliability on the ambiguous rubric's `0.5` (commits-while-noting-alternatives) bucket
- Inter-grader reliability (only one human grader was used)

A follow-up calibration round will sample explicitly from failing rows and partial-credit rows across the run history to address these gaps.

## Citation

If you reproduce this calibration, cite the methodology as: blind hand-grading on a stratified random sample, with agreement measured by within-one-bucket overlap on a discrete rubric. This is the pattern advocated by Hamel Husain ("Creating an LLM-as-a-Judge that drives business results") and is the standard pre-flight check before relying on LLM judges in any iterative evaluation loop.
