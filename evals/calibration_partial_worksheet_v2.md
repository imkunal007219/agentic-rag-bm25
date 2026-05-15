# Hand-grade worksheet — judge-v2 rubric re-anchor

The original `calibration_partial_worksheet.md` was authored under v1's
rubric, where "thin or imprecise but not wrong" = 0.7. Judge-v2 explicitly
says **"answer contains the reference meaning (extra prose is not a defect)"
→ 1.0**, with **0.9** carved out for "right answer, wrong chunk" and
**0.4** reserved for answers that miss a *central* reference claim.

This file re-anchors the same 18 v5 hand-graded rows under the v2 rubric,
so judge-v2 agreement numbers can be computed apples-to-apples instead
of against a frozen v1 reference.

## Rubric reminder (judge-v2)

- **1.0** — answer contains reference meaning (paraphrase / extra context OK) AND retrieval pulled the expected chunk
- **0.9** — answer contains reference meaning BUT retrieval missed the expected chunk; right answer, wrong source
- **0.4** — incomplete: misses a claim central to the reference
- **0.0** — wrong / fabricated / hallucinated
- Ambiguous rubric (unchanged from v1): 1.0 / 0.5 / 0.0

## Re-graded scores

| row | type | recall | hand v1 | **hand v2** | change | reason |
|---|---|---|---:|---:|---|---|
| q003 | single_hop | 0.0 | 1.0 | **0.9** | -0.1 | answer right (boost/midcourse/homing) — chunk missed |
| q004 | single_hop | 1.0 | 0.7 | **1.0** | +0.3 | thinness no longer penalised; rendezvous-vs-intercept meaning captured |
| q007 | single_hop | 1.0 | 0.7 | **1.0** | +0.3 | collision-triangle definition captured (M, T, LOS, intercept trajectory) |
| q009 | single_hop | 1.0 | 0.7 | **1.0** | +0.3 | both PN-optimal assumptions and N=3 covered |
| q016 | multi_hop | 1.0 | 0.4 | **0.4** | same | genuine partial — agent refused on "first missile" half (which IS in corpus) |
| q018 | multi_hop | 0.5 | 1.0 | **1.0** | same | covers analytical-expressions reasoning; multi_hop chunks_hit at recall ≥ 0.5 |
| q020 | multi_hop | 0.0 | 0.4 | **0.4** | same | real mischaracterization (called Ch2 "inverse optimal control"); central claim wrong |
| q022 | multi_hop | 0.5 | 1.0 | **1.0** | same | covers Kappa + SM2; multi_hop chunks_hit |
| q029 | ambiguous | — | 0.5 | **0.5** | same | partial — surfaces some senses (PN/Lyapunov) but not all |
| q034 | single_hop | 1.0 | 1.0 | **1.0** | same | radome-refraction mechanism + high-altitude effect both captured |
| q035 | multi_hop | 1.0 | 0.0 | **0.0** | same | "exceeded maximum turns" — no answer |
| q036 | multi_hop | 0.5 | 1.0 | **1.0** | same | covers peak-miss for deterministic weave; multi_hop chunks_hit |
| q050 | single_hop | 0.0 | 0.7 | **0.9** | +0.2 | gives an equivalent BIBO condition (algebraic form), expected chunk missed |
| q051 | single_hop | 0.0 | 0.7 | **0.9** | +0.2 | miss-step-response defined + analogy to step response covered, chunk missed |
| q052 | multi_hop | 1.0 | 1.0 | **1.0** | same | inertialess-PN baseline → realistic time-constant extension both covered |
| q053 | multi_hop | 1.0 | 1.0 | **1.0** | same | Lyapunov vs Bellman framings both covered |
| q056 | multi_hop | 1.0 | 0.0 | **0.0** | same | "exceeded maximum turns" — no answer |
| q060 | ambiguous | — | 0.5 | **0.5** | same | acknowledges ambiguity but doesn't enumerate the distinct time-constant senses |

## What changed and why

**6 rows shifted, 12 stayed.**

- 4 single_hop rows lifted from 0.7 → 1.0 (q004, q007, q009): the v1 hand-grade
  docked them for prose verbosity even though they captured the reference
  meaning. Under v2 that's not a defect.
- 2 single_hop rows shifted 0.7 → 0.9 (q050, q051): same lift as above, but
  recall=0 so v2 routes them through the "right answer, wrong chunk" bucket.
- 1 single_hop row shifted 1.0 → 0.9 (q003): the answer is right but recall=0,
  so v2 surfaces the source mismatch.

**No row shifted in the wrong direction.** No clean answers got penalised; no
real failures got inflated. The shifts are exactly what v2's rubric was
designed to produce — credit-for-meaning + signal-for-chunk-correctness.

## Agreement results (apples-to-apples)

Each judge re-evaluated on its own scoring run, compared against the
re-anchored hand-grades in the table above (5-bucket snap: 0/0.4/0.5/0.9/1.0).

| Judge | Exact-match | Within-1-bucket |
|---|---:|---:|
| judge-v1 (legacy 0.7-bucket rubric) | **7/18 (39%)** | 11/18 (61%) |
| judge-v2 (option B — collapsed 0.7, added 0.9) | **17/18 (94%)** | 18/18 (100%) |

The single judge-v2 miss is q009 (judge 0.9 vs hand 1.0) — the judge was
slightly conservative on a row where recall=1.0 was reported.

### What this says

Under the v1-rubric anchor (original `calibration_partial_worksheet.md`),
judge-v1 looked fine (67% exact, 100% within-1) and judge-v2 looked like
a marginal regression (72% exact). That comparison was apples-to-oranges:
the v1 hand-grades baked in a "thin answers should be 0.7" rule that
judge-v2 explicitly rejects.

Under the matched-rubric anchor, judge-v2 jumps from 72% to **94%**
exact-match and judge-v1 falls from 67% to **39%**. The right judge was
ahead by a lot all along; the previous calibration just couldn't see it
because the reference was using the wrong rubric.

### Caveat

Hand-grades are mine, single grader. Inter-grader reliability is not
established. Re-grading the same rows in a week would likely flip 1-2
rows on its own, so 94% should be read as "near the ceiling of what
single-grader agreement can yield," not as a hard score.

Reproducible: the per-row data (question, reference, agent answer, recall)
was extracted from `evals/reports/v5-evidence-gated-refusal/20260514T102955Z/report.json`,
and agreement was computed against `evals/reports/v5-judgev2-optionB/20260515T043853Z/report.json`.

Reproducible: the per-row data (question, reference, agent answer, recall)
was extracted from `evals/reports/v5-evidence-gated-refusal/20260514T102955Z/report.json`.
