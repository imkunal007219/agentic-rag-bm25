# Agentic RAG over Technical Textbooks — and a Rigorous Eval of It

Terminal-native agentic RAG using BM25 keyword retrieval and LLM tool-calling, plus a hand-built evaluation harness that scores it across four failure-mode categories and tracks iteration impact across measured runs.

No vector database, no embeddings, no LangChain — just ~200 lines of retrieval code plus a small eval framework that turns "did it work?" into measurable numbers.

---

## Headline result — three iterations, measured

Evaluated on a hand-curated 30-question dataset over a missile-guidance textbook corpus. Each iteration was a single, named change. Each run was scored by an LLM-judge (Claude Sonnet 4.6) against rule-based retrieval-recall.

| Run | Overall | Single-hop | Multi-hop | No-answer | Ambiguous |
|---|---:|---:|---:|---:|---:|
| `v1-bm25-default` (baseline) | 76.7% | 86.7% | 87.5% | 75.0% | 0.0% |
| `v2-chunking-fix` | 66.7% | 73.3% | **100%** | 25.0% | 0.0% |
| `v3-refusal-prompt` | 76.7% | 73.3% | 87.5% | **100%** | **33.3%** |

The full headline doesn't tell the story by itself — the categories do.

**Three substantive findings** the eval surfaced (not vibes — diffable across runs):

1. **The agent ranked back-of-book index pages above real content for definitional queries** because single-letter index pages have 3× the keyword density of real sections. Tagging chunks by content type (`body`, `appendix`, `reference`, `index`, `front_matter`, …) and weighting them at search time moved multi-hop synthesis from 87.5% to **100%** and cut single-hop tokens 34%.

2. **Cleaner retrieval degraded refusal behavior** (75% → 25%). With back-of-book noise removed, out-of-corpus queries returned plausible-but-tangential body chunks, and the agent wove confident answers instead of refusing. The bad chunks had been acting as an implicit hallucination guard. This cross-axis effect doesn't show up in simple evals.

3. **Strengthening the refusal policy in the system prompt recovered no-answer to 100%** and unexpectedly improved ambiguity-handling from 0% to 33% — one prompt change addressed two failure modes via instinct transfer. The change broke one multi-hop row (the more cautious agent over-validates and hits its turn budget), measured and logged.

Each iteration's full report (per-row scores, judge rationales, trace data) is reproducible — see [Reproducibility](#reproducibility).

---

## What's in this repo

```
agentic-rag-bm25/
├── lib/                       # The RAG system
│   ├── expert_index.py        # BM25 indexer + content-type weighting
│   └── expert_agent.py        # Agentic tool-calling loop (Kimi K2.5)
├── ask-expert                 # CLI for the RAG
├── evals/                     # The evaluation harness
│   ├── groundtruth.jsonl      # 30 hand-validated questions, 4 categories
│   ├── schema.md              # Dataset schema + validation rules
│   ├── README.md              # Dataset documentation
│   ├── eval_harness/          # ~600 lines: dataset loader, runner, scorer, report
│   │   ├── dataset.py         # Typed loader + schema validation
│   │   ├── runner.py          # Agent invocation + trace capture + file cache
│   │   ├── scorer.py          # Four type-aware scorers (rule-based + LLM-judge)
│   │   ├── report.py          # JSON + Markdown reports
│   │   └── cli.py             # python -m eval_harness entry point
│   ├── run.sh                 # Convenience wrapper
│   └── reports/               # Per-run scored reports (created on run)
└── requirements.txt
```

---

## The evaluation methodology

### Dataset — 30 questions across four failure modes

Hand-validated by a domain-knowledgeable author (one row at a time, source-checked against the textbook). Each row carries a question, a reference answer, the expected source chunks, and a `question_type` tag determining which scorer is used.

| Type | Count | What it measures |
|---|---:|---|
| `single_hop` | 15 | Retrieval-then-synthesis from one chunk. Tests the baseline RAG loop. |
| `multi_hop` | 8 | Cross-chunk synthesis. Tests whether the agent decomposes and iterates. |
| `no_answer` | 4 | Out-of-corpus queries (near-miss traps that share vocabulary with the corpus). Tests hallucination resistance. |
| `ambiguous` | 3 | Pronoun/term-overload/scope ambiguity. Tests whether the system clarifies or silently commits. |

See [`evals/schema.md`](evals/schema.md) and [`evals/README.md`](evals/README.md) for the full schema, validation rules, and curation methodology.

### Scorers — type-appropriate, hybrid rule + LLM-judge

Different question types need different scoring. A single scorer would either be too strict (penalizes paraphrase on single-hop) or too lenient (can't detect silent commitment on ambiguous).

| Question type | Scoring |
|---|---|
| `single_hop` | Rule-based retrieval recall AND LLM-judge correctness against reference |
| `multi_hop` | Rule-based recall@k over multiple chunks AND LLM-judge correctness |
| `no_answer` | LLM-judge refusal detection (the system should decline, not fabricate) |
| `ambiguous` | LLM-judge against an `expected_behavior` description (does the response surface the ambiguity?) |

Judge model is **Claude Sonnet 4.6**, deliberately a different model family than the agent under test (Kimi K2.5) to avoid self-evaluation bias. Judge prompts are rubric-style with discrete score levels (0.0 / 0.4 / 0.7 / 1.0) for reproducibility, and demand structured JSON output. Per-row judge rationale is captured in every report.

### Trace capture

Every agent invocation is recorded with its tool-call sequence, turn count, and token usage. This is what surfaced the back-of-book-index finding — naive answer-checking would have missed it because the agent eventually produced the right answer (after burning 5 tool calls). Trace data turns "did it work?" into "*how* did it work, and at what cost?"

### Caching and reproducibility

Agent results are cached per run-label by `(sample_id, sha256(question)[:12])`. Re-running the same eval after fixing a scorer is instant; iterating on the agent itself requires `--force` or selectively deleting cache entries. Each run writes a timestamped report under `evals/reports/<label>/<timestamp>/` so old runs are never overwritten.

---

## Reproducibility

```bash
# 1. Clone and install
git clone https://github.com/imkunal007219/agentic-rag-bm25.git
cd agentic-rag-bm25
./setup.sh

# 2. Configure the agent (Kimi K2.5 here; any OpenAI-compatible API works)
export WORKER_API_KEY="sk-..."
export WORKER_BASE_URL="https://api.moonshot.ai/v1"
export WORKER_MODEL="kimi-k2.5"

# 3. Configure the judge for the eval harness
export ANTHROPIC_API_KEY="sk-ant-..."

# 4. Point at a knowledge base (markdown files chunked on ## headings)
export KB_ROOT="$HOME/knowledge-bases"

# 5. Run the eval
./evals/run.sh --label my-run

# Faster iteration: re-run only a subset of question types
./evals/run.sh --label my-run --types ambiguous --force
```

A full 30-question run costs ~$0.30 in API tokens and ~12 minutes the first time. Subsequent runs with the same label hit the cache and complete in ~30 seconds.

The report lands at `evals/reports/<label>/<timestamp>/report.md` (human-readable) and `report.json` (machine-readable / diffable).

---

## Using the RAG by itself

The agent is usable independent of the harness, via the CLI:

```bash
# Single-domain
ask-expert -q "What is the proportional navigation law?" --domain guidance

# Multi-domain (search all books, agent auto-selects)
ask-expert -q "Compare optimal control vs PID" --verbose

# List available domains
ask-expert --list-domains
```

### How the agent works

1. Receives question + tool definitions (`search_all`, `search_domain`, `read_section`)
2. Decides whether to broad-search across books or dive deep into one
3. BM25 index returns ranked text chunks (now weighted by content type)
4. Agent reads full sections if needed
5. Loop continues until the LLM synthesizes a final answer — or refuses for an out-of-corpus query

### Why BM25 (not vectors)?

For technical-textbook retrieval where exact terminology matters ("Lyapunov stability", "Ziegler-Nichols", "Lark missile 1950"), BM25 often outperforms semantic search. It's also deterministic, free to run, and ships with zero vector-DB dependencies. A planned follow-up study evaluates BM25 against vector and hybrid retrieval using this same harness.

---

## Adding your own knowledge base

Drop markdown files into `$KB_ROOT/<domain-name>/`. The indexer chunks on `##` headings.

```
$KB_ROOT/
├── control-theory/
│   ├── chapter-1.md
│   └── chapter-2.md
└── propulsion/
    ├── rocket-engines.md
    └── turbofans.md
```

Files are auto-indexed on first query and cached. The `CHUNKER_VERSION` constant in `lib/expert_index.py` auto-invalidates cached indexes when chunking semantics change.

---

## Performance

Tested on the missile-guidance corpus (10 chapters, 74 indexed chunks after content-type filtering):

- **Typical tool calls per query**: 2–5 (lower with the v3 refusal-policy prompt)
- **Per-query latency**: 5–20 seconds (depends on agent provider)
- **Per-query token cost**: ~$0.01–$0.05 (Kimi K2.5)
- **Eval run cost**: ~$0.30 for the full 30-row dataset including Sonnet judging

---

## Worth reading next

If you found this useful you might also find these interesting:

- Hailey Schoelkopf — "EleutherAI's lm-evaluation-harness, design notes" — the canonical reference for LLM eval rigor.
- Hamel Husain — "Your AI product needs evals" and "Creating a LLM-as-a-Judge" at hamel.dev — the practitioner's guide to production eval.
- JJ Allaire — Inspect framework from UK AISI — production-grade eval framework whose Task / Solver / Scorer abstractions inspired this harness's structure.

---

## Author

**Kunal Bhardwaj** — Systems engineer working on autonomous drones and AI-powered developer tools. Building at the intersection of embedded systems and LLM workflows.

- [Medium](https://medium.com/@kunalbhardwaj598/i-was-burning-through-claude-codes-weekly-limit-in-3-days-here-s-how-i-fixed-it-0344c555abda)
- [LinkedIn](https://www.linkedin.com/in/kunal-bhardwaj-61433818b)
- [Claude Coworker Model](https://github.com/imkunal007219/claude-coworker-model) — The worker-model toolkit this project builds on

---

## License

MIT
