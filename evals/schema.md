# Ground-Truth Dataset Schema

Each line in `groundtruth.jsonl` is a single JSON object with the following fields.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `id` | string | yes | Stable identifier, e.g. `q001`. Lets us reference specific questions in failure analysis without quoting the question text. |
| `question` | string | yes | The user input given to the RAG system. Written as a real user would ask it. |
| `expected_answer` | string \| null | yes | Reference answer for correctness scoring. `null` only for `no_answer` questions (the system should refuse). |
| `expected_chunks` | string[] | yes | List of chunk identifiers in the form `"<file>#<heading>"`, matching the `(file, heading)` pair returned by `ExpertIndex.search()`. Empty array for `no_answer`. Used to score *retrieval* independently of *generation*. Section-level granularity (not file-level) — preserves the ability to distinguish "right chapter, wrong section" from "right section". |
| `question_type` | enum | yes | One of: `single_hop`, `multi_hop`, `no_answer`, `ambiguous`. Lets us slice results by category. |
| `notes` | string | no | Free-form authoring notes. Why the question was included, edge cases, hints for future-you. |

## `question_type` definitions

- **`single_hop`** — answerable from one chunk. Tests baseline retrieve-then-answer.
- **`multi_hop`** — requires information from two or more chunks. Tests composition.
- **`no_answer`** — the corpus does not cover this topic. The system should refuse or say so. `expected_answer` is `null`. Tests hallucination resistance.
- **`ambiguous`** — under-specified question (missing context, vague pronoun, multiple valid interpretations). Tests whether the system clarifies vs. silently committing.

## Example rows

```json
{"id":"q001","question":"What is a guidance law?","expected_answer":"A guidance law is an algorithm that determines the required commanded missile acceleration.","expected_chunks":["01-Chapter-1---Basics-of-Missile-Guidance.md#1.1 INTRODUCTION"],"question_type":"single_hop","notes":"Definition from §1.1"}
{"id":"q017","question":"What does this book say about quantum guidance?","expected_answer":null,"expected_chunks":[],"question_type":"no_answer","notes":"Topic not covered; system should refuse rather than fabricate"}
```

## Validation rules

A row is invalid if:
- `expected_answer` is non-null and `question_type` is `no_answer`
- `expected_chunks` is empty and `question_type` is not `no_answer`
- `id` is not unique within the file
- Any required field is missing
