# Judge calibration

The eval harness scores agent answers with an LLM judge (Claude Sonnet 4.6). Before any pass rate quoted from that judge is worth reading, the judge itself has to be measured against something. This note is that measurement. How the current judge (v2) was built, how it was checked against hand-grades, what the agreement numbers do and don't prove.

The headline: **judge-v2 hits 17 out of 18 exact bucket matches against re-anchored hand-grades (94%). The previous judge (v1) gets 7 out of 18 (39%) on the same comparison.** Both passes used the same 18 rows, the same scoring code, the same hand-grader's calls. Only the rubric changed.

## Why calibrate

An LLM judge giving an LLM agent a passing grade is suspect by default. Three failure modes show up in practice:

- **Central-tendency bias.** Judges trained on instruction-tuning data tend to collapse partial credit toward a middle bucket. A four-bucket rubric (0 / 0.4 / 0.7 / 1.0) collects most of its mass at 0.7 regardless of answer quality.
- **Rubric ambiguity.** "Partially correct" means three different things across three reasonable readers: missing a claim, including a wrong claim, or being phrased poorly. If the rubric doesn't pin the cases, the judge picks a different one each time.
- **Author-time / annotation-time drift.** A reference answer written before the agent existed can disagree with the agent's correct-but-differently-phrased answer. Without a calibration pass you have no way to know whether the score reflects the agent or the reference.

Calibration is the fix: write the rubric, hand-grade a slice, compare. Report the agreement number, and let readers decide whether to trust the rest.

## The rubric, and how it got there

The current judge prompt uses a four-bucket scale for retrieval-grounded questions:

| Score | Meaning |
|------:|---|
| **1.0** | Answer contains the reference meaning, and retrieval surfaced the expected chunk. Extra prose is not a defect. |
| **0.9** | Answer contains the reference meaning, but retrieval missed the expected chunk. Right answer, wrong source. |
| **0.4** | Answer is incomplete: misses a claim central to the reference. |
| **0.0** | Answer is wrong, fabricated, or absent. |

Ambiguous-type questions keep a three-bucket scale (1.0 / 0.5 / 0.0); refusal questions are binary on the correctness axis.

This rubric is the fourth attempt, and the first one that worked. The earlier iterations and what each one taught:

- **v1 (four buckets, 0.7 = "thin or imprecise but not wrong").** Easy to write, hard to apply. The judge collapsed everything borderline into 0.7. Worse, a hand-grader applying the same rubric also collapsed into 0.7, which made the judge look fine in easy-regime calibration and hid the real disagreement.
- **v1.1 (drafted, never shipped).** Tried to tighten the 0.7 language without removing the bucket. Same central-tendency problem in dry runs. Deleted.
- **v2-draft, v3-draft.** Attempts to split the 0.7 bucket along axes like "missing-claim vs sloppy-phrasing." Didn't help. The rubric got longer without removing the ambiguity.
- **v2 (shipped).** Collapse the muddled middle bucket entirely. Add a separate 0.9 bucket for "right answer, wrong chunk" so retrieval correctness and answer correctness stay observable as independent signals. Treat extra prose as not-a-defect. If the reference meaning is in the answer, score it 1.0.

The design move that mattered was **separating chunk-correctness from answer-correctness**. Before v2, a row where retrieval missed the canonical chunk but the agent answered from an equivalent passage was either a false positive (1.0 papering over a retrieval miss) or a false negative (0.4 punishing a correct answer). The 0.9 bucket makes that case explicit, counts it as a pass, and still flags the retrieval signal in the trace.

## Protocol

- **Sample:** 18 rows from the v5-evidence-gated-refusal run on the guidance corpus. Composition: 8 single_hop, 6 multi_hop, 2 ambiguous, 2 no_answer.
- **Hand-grading:** single grader, blind to the judge's score at grading time. Each row scored on the judge-v2 rubric, including the 0.9 "right answer, wrong chunk" call.
- **Re-anchoring:** the original hand-grades were authored under v1's rubric. To compare judge-v2 against them apples-to-apples, the same 18 rows were re-graded under the v2 rubric. Six rows shifted, twelve stayed. The re-anchored grades are what the judge is measured against here. The re-anchoring worksheet (`calibration_partial_worksheet_v2.md`) shows every shift with a one-line justification.
- **Comparison:** both judge-v1 and judge-v2 were re-scored against the same agent answers from the v5 run, with their respective rubrics. The judge outputs are bucket-snapped (0 / 0.4 / 0.5 / 0.9 / 1.0) before comparison.

## Result

| Judge | Exact-match | Within-1-bucket |
|---|---:|---:|
| judge-v1 (legacy 0.7-bucket rubric) | **7/18 (39%)** | 11/18 (61%) |
| judge-v2 (collapsed 0.7, added 0.9) | **17/18 (94%)** | 18/18 (100%) |

The single judge-v2 miss is q009: the judge scored 0.9 where the hand-grade said 1.0. Retrieval was recall=1.0 on that row, so the judge was slightly conservative on a borderline call. It's a within-1-bucket miss, not a substantive disagreement.

The framing matters. Under the original v1-anchor (the worksheet as first written), judge-v1 looked decent (67% exact-match) and judge-v2 looked like a marginal regression (72% exact-match). That comparison was apples-to-oranges. The v1 hand-grades baked in a "thin answers are 0.7" rule that judge-v2 explicitly rejects. Under the matched rubric, judge-v2 is ahead by 55 points, not behind by five. **The previous calibration just couldn't see it because the reference was using a different rubric than the judge under test.** This is the kind of methodological hole that quietly invalidates most LLM-judge comparisons in the wild.

## Cross-corpus evidence

The same judge-v2 was used to score three different corpora. The pass rates and the chunking decision each one required:

| Corpus | Domain | Pass rate | Best chunking |
|---|---|---:|---|
| Missile guidance | technical, equation-heavy | 76% | chapter + sub-section split |
| Géron Hands-On ML | semi-technical textbook | 80% | chapter + sub-section split (+33pp lift vs chapter-only) |
| Marcus Aurelius — Meditations | classical philosophy | 75% | **chapter only** (paragraph-level split regressed by 17pp) |

Three things to pull out of that table.

One: the same agent prompt (v6) and the same judge (v2) generalize across three very different domains without per-corpus tuning. That's the cross-domain proof for the system overall.

Two: the chunking decision is not universal. Paragraph-level chunking lifted Géron by 33 points and hurt Meditations by 17. The mechanical explanation, that sub-section headings carry query-matching vocabulary in textbooks but numbered paragraph IDs in Meditations don't, is in `notes-meditations-chunking.md`. The point for calibration: **the harness detected this regression on the first run.** Without the eval, the regression ships.

Three: the Meditations result is the strongest portfolio claim, not the weakest. A uniformly-rising chart on three corpora invites "did you tune to your eval set?" An A/B with one direction reversed and a mechanical explanation does not.

## Honest caveats

What the 94% number is, and isn't:

- **Single grader.** Inter-grader reliability is not established. Re-grading the same 18 rows next week would likely flip one or two on its own. Read 94% as "near the ceiling of what single-grader agreement can produce," not as a hard score.
- **Single corpus for the calibration sample.** The hand-grades are all from the guidance corpus. Judge behavior on the ML or Meditations corpora has been spot-checked but not hand-validated to the same depth.
- **No adversarial slice.** The 18 rows are representative of the natural run distribution, not selected to stress edge cases. Calibration on deliberately hard rows (heavy paraphrase, hedged answers, correct-plus-wrong-claim) is the next round of work.
- **Small N on the 0.9 bucket.** Two of the 18 rows actually exercise it. The bucket is well-defined and the judge applies it correctly on those two. Two is still a small N for any claim about the bucket itself.

The number to quote in interviews and writeups: **94% under matched-rubric calibration on 18 rows, single grader, guidance corpus only. Partial-credit and cross-corpus calibration pending.**

## What's next

- **Inter-grader pass.** Recruit a second grader, re-score the same 18 rows, report kappa.
- **Adversarial slice.** Hand-author a 10-row eval where the agent answers are deliberately edge-case (heavy paraphrase, hedged answers, correct-plus-wrong-claim) and measure judge-v2 on it specifically.
- **Cross-corpus calibration.** Repeat the protocol on 10 rows each from the ML and Meditations runs.
- **Judge versioning.** Calibration is bound to a specific judge model and rubric. When either changes, the pass rate is not comparable until a new calibration is run. Versioning the judge prompt and tracking which calibration each report cites is the operational requirement.

## Reproducibility

- Rubric source: `lib/expert_agent.py` (agent prompt v6), `evals/eval_harness/scorer.py` (judge prompt v2, `_CORRECTNESS_PROMPT`).
- Hand-grade worksheet: `evals/calibration_partial_worksheet_v2.md` (18 rows, per-row shifts and justifications).
- Agreement comparison: `evals/calibration_partial_agreement.py` against the v5 run reports under `evals/reports/v5-evidence-gated-refusal/` and `evals/reports/v5-judgev2-optionB/`.
- Cross-corpus reports: `evals/reports/medit-v1/`, `evals/reports/ml-v6-subsection/`, `evals/reports/v5-judgev2-optionB/`.
- Negative-result note (Meditations chunking): `evals/notes-meditations-chunking.md`.

## History

A previous version of this document reported 100% within-one-bucket agreement on a 10-row easy-regime sample, scored under v1's rubric. That number was technically correct and operationally misleading. The sample contained no partial-credit rows and used the same rubric that was producing the central-tendency bias being measured. The matched-rubric, judge-v2 result reported here supersedes it.
