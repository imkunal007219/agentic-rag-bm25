# RAG Evaluation Dataset

Ground-truth dataset for evaluating `agentic-rag-bm25` against a missile-guidance textbook corpus.

## Source corpus

**Domain:** `guidance` — a missile guidance textbook converted to chapter-level Markdown.

**Location:** `memory/knowledge-bases/guidance/` in the MC07/MC08 project. The corpus is organised as one Markdown file per chapter/section, e.g. `01-Chapter-1---Basics-of-Missile-Guidance.md`.

**Chapters covered in dataset:** TBD — will be filled in once questions are written.

## Dataset composition (target)

| Question type | Target count | Tests |
|---|---|---|
| `single_hop` | 15 | Retrieval + synthesis from one chunk |
| `multi_hop` | 8 | Composition across multiple chunks |
| `no_answer` | 4 | Hallucination resistance on out-of-domain queries |
| `ambiguous` | 3 | Behaviour on under-specified queries |
| **Total** | **30** | |

Actual counts will be updated as rows are added.

## How questions were created

Manual curation by a domain-knowledgeable author (control / guidance background). Process:

1. **Single-hop bootstrap:** read one chapter at a time, write 5-7 factual questions per chapter, record the source chunk.
2. **Run against the system:** each draft question goes through `ask-expert` against the guidance domain. Both correct and incorrect responses are kept — incorrect ones are the most valuable rows because they expose real failure modes.
3. **Multi-hop:** identify pairs of chapters that relate (e.g. proportional navigation in Ch3 + guidance-law design in Ch5), write questions that require both.
4. **No-answer:** deliberately pick topics outside the book's scope (e.g. quantum guidance, satellite formation flying).
5. **Ambiguous:** vague pronouns, missing referents, multi-interpretation queries.
6. **Validation:** every row is spot-checked against the source text before being committed. `expected_answer` is verified to actually appear in `expected_chunks`.

## Schema

See [`schema.md`](./schema.md) for the field-by-field specification.

## Limitations

Stated up front so they cannot be hidden later:

- **Single corpus** — one textbook. Results do not generalise to other domains without re-curation.
- **English only.**
- **Author bias** — questions reflect what the author finds interesting / important. Coverage is not uniform across chapters.
- **No numerical / equation-heavy questions in v1** — eval of formulae requires a different scoring approach (symbolic comparison, not string match). Deferred to v2.
- **Hand-curated, not LLM-generated** — by design (LLM generation inherits the generator's biases and risks circular evaluation). LLM augmentation is a v2 step once a hand-validated baseline exists.

## Versioning

- `v0.1` — initial 30-question dataset, hand-curated, guidance corpus only.

## Reproducibility notes

- Each row carries enough information (`question` + `expected_chunks`) that an external reviewer can verify correctness by reading the source chunks directly.
- The dataset file is checked into version control. Any update to a row is a real commit with a real diff — the eval is reproducible across time.
