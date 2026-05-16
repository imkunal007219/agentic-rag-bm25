# Eval Report — v5-judgev2-optionB

- **Generated:** 20260515T043853Z
- **Dataset:** `evals/groundtruth.jsonl` (60 rows)
- **Agent:** `kimi-k2.5 + BM25 (lib/expert_agent.run_agent)`
- **Judge model:** `claude-sonnet-4-6`

## Headline

- **Overall pass rate:** 83.3%  (50 / 60)
- **Overall avg value:** 0.86

## Per-category metrics

| Type | Count | Pass rate | Avg value | Avg recall | Avg correctness | Refusal | Clarification |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ambiguous` | 5 | 20.0% | 0.40 | — | — | — | 0.40 |
| `multi_hop` | 16 | 75.0% | 0.82 | 0.84 | 0.80 | — | — |
| `no_answer` | 9 | 100.0% | 1.00 | — | — | 1.00 | — |
| `single_hop` | 30 | 93.3% | 0.92 | 0.90 | 0.92 | — | — |

## Trace statistics

| Type | Avg tool calls | Max tool calls | Avg turns | Total tokens (in / out) |
|---|---:|---:|---:|---:|
| `ambiguous` | 6.20 | 10 | 6.40 | 165,484 / 8,916 |
| `multi_hop` | 7.44 | 16 | 6.06 | 683,652 / 24,624 |
| `no_answer` | 10.22 | 16 | 7.22 | 516,560 / 12,691 |
| `single_hop` | 4.23 | 10 | 4.60 | 586,545 / 29,737 |

## Failures (10)

### `q002` — `single_hop` — value 0.00

**Question:** What is the first missile system to use the parallel navigation principle, and in what year?

**Judge rationale:** correctness=0.00 (recall=1.00): The system answer fails to provide the correct answer (Lark missile, 1950) and instead claims the information is not in the knowledge base, despite retrieval being marked as correct.

**Agent answer (preview):** The knowledge base does not specifically cover which missile system was the first to use the parallel navigation principle or the year it was introduced.

I read:
- **Section 2.1 (Parallel Navigation)** and **Section 2.2 (Proportional Navigation. Planar Engagement)** from Chapter 2 — These sections explain that proportional navigation (PN) is the guidance law that implements parallel navigation (t…

**Tool calls (8):** `search_kb`, `read_section`, `read_section`, `search_kb`, `search_kb`, `search_kb`, `read_section`, `search_kb`

### `q016` — `multi_hop` — value 0.70

**Question:** How does proportional navigation implement the parallel-navigation principle, and when was it first used in a real missile system?

**Judge rationale:** recall=1.00 of 2 chunks, correctness=0.40: The system answer correctly explains how proportional navigation implements the parallel-navigation principle, but explicitly states it cannot find when PN was first used in a real missile system (the Lark missile in 1950), which is a central claim in the reference answer.

**Agent answer (preview):** Based on my reading of the full sections, I can answer the first part of your question. The knowledge base does not contain specific information about when proportional navigation was first used in a real missile system.

---

## How Proportional Navigation Implements Parallel Navigation

According to **Section 2.2** and **Section 2.5** of the Parallel Navigation chapter, proportional navigation (…

**Tool calls (11):** `search_kb`, `search_kb`, `read_section`, `read_section`, `read_section`, `search_kb`, `search_kb`, `search_kb` …

### `q020` — `multi_hop` — value 0.20

**Question:** The book derives the proportional-navigation law as the solution to a control problem in Chapter 2 and revisits it via a Lyapunov approach in Chapter 5 — what does the Lyapunov treatment add beyond the Chapter 2 derivation?

**Judge rationale:** recall=0.00 of 2 chunks, correctness=0.40: The system answer captures point (1) about the Lyapunov function derivative as a performance index for comparing and creating guidance laws, but misses the central point (2) about extension to maneuvering targets — that augmented PN and other modifications are obtained as solutions of a stability problem rather than ad-hoc extensions — and also mischaracterizes Chapter 2 as an optimal control/quadratic cost derivation rather than a control-problem formulation using LOS angle and its derivative as state variables; additionally retrieval was incorrect.

**Agent answer (preview):** Based on my reading of the full sections, I can now synthesize the answer.

## What the Lyapunov Treatment Adds (Chapter 5 vs. Chapter 2)

**Chapter 2's Optimal Control Approach (Section 2.7)** treats the PN law as the solution to an **inverse optimal control problem**. Under near-collision course assumptions (constant closing velocity, ignoring missile dynamics), it minimizes the quadratic perfor…

**Tool calls (6):** `search_kb`, `search_kb`, `read_section`, `read_section`, `read_section`, `search_kb`

### `q029` — `ambiguous` — value 0.50

**Question:** What is the optimal guidance law?

**Judge rationale:** The response correctly surfaces multiple interpretations of 'optimal' (PN with N=3, Kappa guidance, general optimal control) and explicitly states there is no single universal answer, but it misses at least two senses described in the expected behavior — Lyapunov-based guidance laws (Ch5 §5.3) and neoclassical guidance (Ch6 §6.2) — making it only a partial match.

**Agent answer (preview):** Based on the textbook's full coverage of optimal guidance theory, I can now synthesize an answer. There is **no single universal "optimal guidance law"** — optimality depends entirely on the performance index chosen for the specific engagement requirements.

## 1. PN as Optimal Under Quadratic Performance Index

According to **Section 2.7**, Proportional Navigation (PN) is optimal when:

- The sys…

**Tool calls (5):** `search_kb`, `read_section`, `read_section`, `search_kb`, `read_section`

### `q030` — `ambiguous` — value 0.00

**Question:** What is the miss distance for my missile guidance system?

**Judge rationale:** The system response is a technical error message (API rate limit), not an answer at all — it neither recognizes the ambiguity nor provides any useful response, so it fails to meet the expected behavior.

**Agent answer (preview):** [Kimi API rate-limited after 4 retries. Error: Error code: 429 - {'error': {'message': 'The engine is currently overloaded, please try again later', 'type': 'engine_overloaded_error'}}]

**Tool calls (4):** `search_kb`, `read_section`, `read_section`, `read_section`

### `q033` — `single_hop` — value 0.00

**Question:** Why do Kalman filters struggle with glint noise in radar seekers?

**Judge rationale:** correctness=0.00 (recall=1.00): The system failed to produce any answer, returning only an error message about exceeding maximum turns.

**Agent answer (preview):** [Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Tool calls (10):** `search_kb`, `read_section`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `read_section`, `search_kb` …

### `q035` — `multi_hop` — value 0.50

**Question:** How does adding a cubic term to the Lyapunov guidance law compare to using it in the pseudoclassical method? Do they achieve the same thing?

**Judge rationale:** recall=1.00 of 2 chunks, correctness=0.00: The system produced no answer at all (agent timeout), so none of the reference content is conveyed.

**Agent answer (preview):** [Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Tool calls (16):** `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `read_section` …

### `q040` — `ambiguous` — value 0.00

**Question:** What does the shaping term do in missile guidance?

**Judge rationale:** The system failed to produce any answer at all due to exceeding maximum turns, which means it neither recognized the ambiguity nor surfaced multiple interpretations, representing a complete failure to handle the question.

**Agent answer (preview):** [Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Tool calls (10):** `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `read_section` …

### `q056` — `multi_hop` — value 0.50

**Question:** How do the line-of-sight angles defined in Chapter 1 relate to the seeker gimbal angles in the Chapter 8 seeker model?

**Judge rationale:** recall=1.00 of 2 chunks, correctness=0.00: The system answer is a failure message indicating the agent exceeded maximum turns and produced no answer, so it conveys none of the reference content.

**Agent answer (preview):** [Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Tool calls (13):** `search_kb`, `search_kb`, `search_kb`, `read_section`, `read_section`, `read_section`, `search_kb`, `search_kb` …

### `q060` — `ambiguous` — value 0.50

**Question:** What time constant should I use in my guidance model?

**Judge rationale:** The system does ask for clarification and acknowledges that the time constant depends on scenario parameters, but it silently commits to only the flight-control/guidance time constant τ from Ch3-4 and never surfaces the other distinct senses (autopilot lag time constant, seeker time constant, actuator time constant from Ch8) that the expected behavior requires to be identified as separate interpretations.

**Agent answer (preview):** Based on my reading of the relevant sections, your question requires clarification because the appropriate time constant depends on several system parameters.

## Clarification Needed

The knowledge base shows that the flight control system time constant **τ** is highly dependent on:

1. **Airframe zero frequency (ω_z)**: At high altitudes where ω_z is low (e.g., 5 rad/s), decreasing τ can actuall…

**Tool calls (3):** `search_kb`, `read_section`, `read_section`
