# Eval Report — ml-v6-subsection

- **Generated:** 20260515T090911Z
- **Dataset:** `evals/groundtruth-ml.jsonl` (15 rows)
- **Agent:** `kimi-k2.5 + BM25 (lib/expert_agent.run_agent)`
- **Judge model:** `claude-sonnet-4-6`

## Headline

- **Overall pass rate:** 80.0%  (12 / 15)
- **Overall avg value:** 0.85

## Per-category metrics

| Type | Count | Pass rate | Avg value | Avg recall | Avg correctness | Refusal | Clarification |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ambiguous` | 2 | 50.0% | 0.50 | — | — | — | 0.50 |
| `multi_hop` | 3 | 33.3% | 0.58 | 0.83 | 0.33 | — | — |
| `no_answer` | 2 | 100.0% | 1.00 | — | — | 1.00 | — |
| `single_hop` | 8 | 100.0% | 1.00 | 1.00 | 1.00 | — | — |

## Trace statistics

| Type | Avg tool calls | Max tool calls | Avg turns | Total tokens (in / out) |
|---|---:|---:|---:|---:|
| `ambiguous` | 4.50 | 6 | 4.00 | 46,575 / 2,460 |
| `multi_hop` | 6.67 | 14 | 5.00 | 195,145 / 2,430 |
| `no_answer` | 6.00 | 7 | 5.50 | 55,010 / 2,267 |
| `single_hop` | 2.75 | 5 | 3.50 | 100,478 / 7,169 |

## Failures (3)

### `m009` — `multi_hop` — value 0.50

**Question:** Compare batch gradient descent and stochastic gradient descent.

**Judge rationale:** recall=1.00 of 1 chunks, correctness=0.00: The system answer is an API error message and contains no information about batch gradient descent or stochastic gradient descent.

**Agent answer (preview):** [Kimi API rate-limited after 4 retries. Error: Error code: 429 - {'error': {'message': 'The engine is currently overloaded, please try again later', 'type': 'engine_overloaded_error'}}]

**Tool calls (1):** `search_kb`

### `m010` — `multi_hop` — value 0.50

**Question:** Compare K-Means and DBSCAN clustering.

**Judge rationale:** recall=1.00 of 1 chunks, correctness=0.00: The system produced no answer at all (agent exceeded maximum turns), so none of the reference content was conveyed.

**Agent answer (preview):** [Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Tool calls (14):** `search_kb`, `search_kb`, `search_kb`, `search_kb`, `read_section`, `search_kb`, `search_kb`, `search_kb` …

### `m015` — `ambiguous` — value 0.00

**Question:** What does 'training' mean here?

**Judge rationale:** The system silently commits to a single interpretation of 'training' (supervised model fitting from Chapter 4) without acknowledging that the question is ambiguous or that 'training' could refer to multiple distinct concepts such as deep neural network training (Ch11), the training set as a data partition (Ch1/2), or reinforcement learning training.

**Agent answer (preview):** Based on the **Hands-On Machine Learning** textbook, here is what **training** means in the context of machine learning:

## Definition of Training

According to **Chapter 4: Training Models**, **training** is the process of **finding model parameters that best fit the model to the training set**—specifically, the parameters that **minimize the cost function over the training set** (Section "CHAPT…

**Tool calls (6):** `search_kb`, `read_section`, `read_section`, `search_kb`, `read_section`, `read_section`
