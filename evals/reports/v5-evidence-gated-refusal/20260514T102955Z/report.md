# Eval Report — v5-evidence-gated-refusal

- **Generated:** 20260514T102955Z
- **Dataset:** `evals/groundtruth.jsonl` (60 rows)
- **Agent:** `kimi-k2.5 + BM25 (lib/expert_agent.run_agent)`
- **Judge model:** `claude-sonnet-4-6`

## Headline

- **Overall pass rate:** 85.0%  (51 / 60)
- **Overall avg value:** 0.83

## Per-category metrics

| Type | Count | Pass rate | Avg value | Avg recall | Avg correctness | Refusal | Clarification |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ambiguous` | 5 | 20.0% | 0.40 | — | — | — | 0.40 |
| `multi_hop` | 16 | 81.2% | 0.80 | 0.84 | 0.76 | — | — |
| `no_answer` | 9 | 100.0% | 1.00 | — | — | 1.00 | — |
| `single_hop` | 30 | 93.3% | 0.86 | 0.90 | 0.86 | — | — |

## Trace statistics

| Type | Avg tool calls | Max tool calls | Avg turns | Total tokens (in / out) |
|---|---:|---:|---:|---:|
| `ambiguous` | 6.20 | 10 | 6.40 | 165,484 / 8,916 |
| `multi_hop` | 7.44 | 16 | 6.06 | 683,652 / 24,624 |
| `no_answer` | 10.22 | 16 | 7.22 | 516,560 / 12,691 |
| `single_hop` | 4.23 | 10 | 4.60 | 586,545 / 29,737 |

## Failures (9)

### `q002` — `single_hop` — value 0.00

**Question:** What is the first missile system to use the parallel navigation principle, and in what year?

**Judge rationale:** correctness=0.00 (recall=1.00): The system answer fails to provide the correct answer (the Lark missile, 1950) and instead claims the information is not in the knowledge base, constituting a failure to answer the question.

**Agent answer (preview):** The knowledge base does not specifically cover which missile system was the first to use the parallel navigation principle or the year it was introduced.

I read:
- **Section 2.1 (Parallel Navigation)** and **Section 2.2 (Proportional Navigation. Planar Engagement)** from Chapter 2 — These sections explain that proportional navigation (PN) is the guidance law that implements parallel navigation (t…

**Tool calls (8):** `search_kb`, `read_section`, `read_section`, `search_kb`, `search_kb`, `search_kb`, `read_section`, `search_kb`

### `q020` — `multi_hop` — value 0.20

**Question:** The book derives the proportional-navigation law as the solution to a control problem in Chapter 2 and revisits it via a Lyapunov approach in Chapter 5 — what does the Lyapunov treatment add beyond the Chapter 2 derivation?

**Judge rationale:** recall=0.00 of 2 chunks, correctness=0.40: The system answer correctly identifies that Chapter 5 adds a comparison criterion via the Lyapunov function derivative module and a design methodology for creating new guidance laws, but it mischaracterizes Chapter 2 as an inverse optimal control derivation (minimizing a quadratic cost) rather than a control-problem formulation using LOS angle/derivative as state variables, and critically omits the reference's key point that the Lyapunov treatment extends naturally to maneuvering targets, enabling augmented PN and other modifications to be derived as stability solutions rather than ad-hoc extensions.

**Agent answer (preview):** Based on my reading of the full sections, I can now synthesize the answer.

## What the Lyapunov Treatment Adds (Chapter 5 vs. Chapter 2)

**Chapter 2's Optimal Control Approach (Section 2.7)** treats the PN law as the solution to an **inverse optimal control problem**. Under near-collision course assumptions (constant closing velocity, ignoring missile dynamics), it minimizes the quadratic perfor…

**Tool calls (6):** `search_kb`, `search_kb`, `read_section`, `read_section`, `read_section`, `search_kb`

### `q029` — `ambiguous` — value 0.50

**Question:** What is the optimal guidance law?

**Judge rationale:** The response correctly surfaces multiple senses of 'optimal' (PN with N=3, Kappa guidance, and general optimal control) and avoids silently committing to one, but it misses several interpretations described in the expected behavior — specifically Lyapunov-based guidance (Ch5 §5.3), neoclassical guidance and its counterintuitive failure mode (Ch6 §6.2), and integrated guidance-and-control design (Ch9 §9.3) as distinct senses of optimality.

**Agent answer (preview):** Based on the textbook's full coverage of optimal guidance theory, I can now synthesize an answer. There is **no single universal "optimal guidance law"** — optimality depends entirely on the performance index chosen for the specific engagement requirements.

## 1. PN as Optimal Under Quadratic Performance Index

According to **Section 2.7**, Proportional Navigation (PN) is optimal when:

- The sys…

**Tool calls (5):** `search_kb`, `read_section`, `read_section`, `search_kb`, `read_section`

### `q030` — `ambiguous` — value 0.00

**Question:** What is the miss distance for my missile guidance system?

**Judge rationale:** The system response is a technical error message (API rate limiting) that provides no answer whatsoever — it neither recognizes the ambiguity nor surfaces any interpretations, effectively a complete failure to handle the question.

**Agent answer (preview):** [Kimi API rate-limited after 4 retries. Error: Error code: 429 - {'error': {'message': 'The engine is currently overloaded, please try again later', 'type': 'engine_overloaded_error'}}]

**Tool calls (4):** `search_kb`, `read_section`, `read_section`, `read_section`

### `q033` — `single_hop` — value 0.00

**Question:** Why do Kalman filters struggle with glint noise in radar seekers?

**Judge rationale:** correctness=0.00 (recall=1.00): The system failed to produce any answer, returning only an error message about exceeding maximum turns.

**Agent answer (preview):** [Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Tool calls (10):** `search_kb`, `read_section`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `read_section`, `search_kb` …

### `q035` — `multi_hop` — value 0.50

**Question:** How does adding a cubic term to the Lyapunov guidance law compare to using it in the pseudoclassical method? Do they achieve the same thing?

**Judge rationale:** recall=1.00 of 2 chunks, correctness=0.00: The system failed to produce any answer, returning only an error message about exceeding maximum turns, so no relevant information was conveyed.

**Agent answer (preview):** [Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Tool calls (16):** `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `read_section` …

### `q040` — `ambiguous` — value 0.00

**Question:** What does the shaping term do in missile guidance?

**Judge rationale:** The system failed to produce any answer at all, let alone recognize the ambiguity or surface multiple interpretations, which is a complete failure to meet the expected behavior.

**Agent answer (preview):** [Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Tool calls (10):** `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `search_kb`, `read_section` …

### `q056` — `multi_hop` — value 0.50

**Question:** How do the line-of-sight angles defined in Chapter 1 relate to the seeker gimbal angles in the Chapter 8 seeker model?

**Judge rationale:** recall=1.00 of 2 chunks, correctness=0.00: The system produced no answer at all (agent timeout), so it fails to address any aspect of the question.

**Agent answer (preview):** [Agent exceeded maximum turns without producing an answer. Try a more specific question.]

**Tool calls (13):** `search_kb`, `search_kb`, `search_kb`, `read_section`, `read_section`, `read_section`, `search_kb`, `search_kb` …

### `q060` — `ambiguous` — value 0.50

**Question:** What time constant should I use in my guidance model?

**Judge rationale:** The system does ask for clarification and surfaces some ambiguity around the flight-control time constant τ, but it silently commits to the Ch3-4 first-order guidance/flight-control time constant without acknowledging the other distinct senses described in the expected behavior: the autopilot lag time constant, the seeker time constant, and the actuator time constant from Ch8 models.

**Agent answer (preview):** Based on my reading of the relevant sections, your question requires clarification because the appropriate time constant depends on several system parameters.

## Clarification Needed

The knowledge base shows that the flight control system time constant **τ** is highly dependent on:

1. **Airframe zero frequency (ω_z)**: At high altitudes where ω_z is low (e.g., 5 rad/s), decreasing τ can actuall…

**Tool calls (3):** `search_kb`, `read_section`, `read_section`
