# Meditations: when sub-section chunking hurts

A note for the calibration writeup. Captured during Day 3 of the
agentic-rag-bm25 sprint, after running paragraph-level chunking on the
Marcus Aurelius corpus and watching the eval regress.

## The finding

The same ingestion technique that lifted the Géron ML eval by +33pp
(47% → 80%) regressed the Meditations eval by -17pp (75% → 58%).

| Corpus | Strategy | Chunks | Pass rate |
|---|---|---|---:|
| Géron ML | chapter-only | 9 | 47% |
| Géron ML | + sub-section split (page-header signal) | 136 | 80% |
| Meditations | chapter-only | 13 | **75%** |
| Meditations | + paragraph split (numbered-marker signal) | 202 | 58% |

The chapter-level chunking is what we ship for Meditations.

## Why the same technique flipped

Two preconditions for sub-section chunking to help:

1. **The heading must carry query-matching vocabulary.** Géron has
   sub-section titles like "Bagging and Pasting" or "Gradient Descent" —
   the heading itself is what a user would type. Meditations paragraph
   chunks are headed "BOOK IV.5", "BOOK IV.6". The heading carries no
   semantic content, so BM25 cannot use the heading as a discriminator.
2. **Chunks must stay substantial.** Géron sub-section chunks are
   500-2000 words. Meditations paragraph chunks are 50-500 words. With
   200 small chunks of similar thematic vocabulary, IDF helps less and
   BM25 picks the wrong chunk for thematic queries ("death", "nature",
   "virtue" appear across many books).

## Operational implication

`lib/ingestion.py` keeps the paragraph-split code (the right tool for
the right corpus — e.g. it would likely help on a numbered legal code
or RFC) but exposes `--no-paragraph-split` for corpora where the two
preconditions don't hold.

## Why this is portfolio-worthy, not embarrassing

A uniform "everything got better" story is weaker than an A/B with one
direction reversed. The negative result demonstrates: (a) the eval
harness detects regressions you would otherwise miss, (b) chunking is
empirical not dogmatic, (c) BM25's behavior is mechanically explainable
which is why we can reason about *why* it reversed. Most RAG demos in
the wild have neither the eval to detect this nor the explanation when
it happens.

## Reproducibility

- Chapter-only Meditations baseline: `evals/reports/medit-v1/20260515T103135Z/`
- Paragraph-split regression: `evals/reports/medit-paragraph/20260515T120038Z/`
- Eval set: `evals/groundtruth-meditations.jsonl` (12 rows: 6 single_hop,
  2 multi_hop, 2 no_answer, 2 ambiguous)
- Reproduce: `./evals/run.sh --label medit-v1 --dataset evals/groundtruth-meditations.jsonl --domain meditations`
