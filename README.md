# agentic-rag-bm25

A working agentic RAG system, plus the eval harness that proves it works.

No vector database. No LangChain. About 200 lines of retrieval code, a small tool-calling agent, and an eval harness with an LLM judge measured against human grades. Three knowledge bases shipped: a missile-guidance textbook, the Géron Hands-On ML book, and Marcus Aurelius's *Meditations*.

## The three numbers

- **94%** — exact-match agreement between the LLM judge and human hand-grades on 18 rows, under a matched rubric. See [`evals/calibration.md`](evals/calibration.md).
- **75–80%** — agent pass rate across three corpora (technical, semi-technical, classical), same prompt, same judge, no per-corpus tuning.
- **One reversed result** — the chunking technique that lifted the ML eval by 33 points regressed Meditations by 17. The harness caught it on the first run. [`evals/notes-meditations-chunking.md`](evals/notes-meditations-chunking.md) explains why.

That third number is the one I'd actually defend in an interview. A uniformly rising chart is suspicious. An A/B with one direction reversed, and a mechanical explanation for the reversal, is not.

## What this is for

If you are building RAG in a regulated, air-gapped, or cost-sensitive environment (legal, healthcare, defense, internal engineering knowledge), the usual stack of LangChain plus a hosted vector DB plus uncalibrated LLM scoring is overkill and hides what is actually happening. This project is the opposite:

- BM25 retrieval. Interpretable, free, runs on a laptop, no embeddings API
- A small tool-calling agent that decides when to search, when to refuse, when to clarify
- An eval harness that scores every change against a frozen gold set
- A judge whose rubric was iterated four times, whose agreement with a human grader is actually measured

It is not a production drop-in. It is what someone building under those constraints would assemble if they had a week. Most of the value is in the eval and calibration story, not in the agent itself.

## Quickstart

You need:

- Python 3.10+
- An OpenAI-compatible LLM API for the agent (Moonshot's Kimi K2.5, DeepSeek, or local Ollama all work)
- An Anthropic API key for the judge (Claude Sonnet 4.6)
- About $0.30 in API credits for a full 12-row run, or free if you only want the agent

```bash
git clone https://github.com/imkunal007219/agentic-rag-bm25.git
cd agentic-rag-bm25
./setup.sh

export WORKER_API_KEY="sk-..."                         # your agent provider
export WORKER_BASE_URL="https://api.moonshot.ai/v1"
export WORKER_MODEL="kimi-k2.5"
export ANTHROPIC_API_KEY="sk-ant-..."                  # the judge
export KB_ROOT="$HOME/knowledge-bases"                 # where corpora live

# Ask the agent a question over the guidance corpus
ask-expert --domain guidance -q "What is the proportional navigation law?"

# Run the full eval (12 rows, ~12 minutes first time, ~30s cached)
./evals/run.sh --label my-first-run --domain guidance
```

The report lands in `evals/reports/my-first-run/<timestamp>/report.md` with per-row scores, judge rationales, recall, and trace data.

## Adding your own corpus

Drop a PDF, text, or pre-chunked markdown file in:

```bash
python -m lib.ingestion --input ~/Downloads/my-book.pdf --corpus my-corpus
```

That converts the file to chunked markdown, builds the BM25 index, and registers a new domain you can query. For aphoristic numbered texts where small paragraph chunks hurt retrieval (legal codes, sutras, *Meditations*), pass `--no-paragraph-split`. The reason this flag exists is itself an eval finding, written up in `evals/notes-meditations-chunking.md`.

For very old OCR-scanned PDFs where pypdf garbles word spacing, pre-convert with `pdftotext yourbook.pdf yourbook.txt` and feed the `.txt`. Automatic fallback is on the roadmap.

## How the eval works

Every question in the gold set carries a type tag. The scorer picks a different rule per type:

| Type | What it measures | Scoring |
|---|---|---|
| `single_hop` | Retrieve, then answer from one chunk | Recall + LLM-judge correctness |
| `multi_hop` | Synthesize from multiple chunks | Recall@k + correctness |
| `no_answer` | Out-of-corpus question | Refusal detection. The agent should decline, not fabricate. |
| `ambiguous` | Vague or overloaded question | Did the agent clarify, or silently commit to one reading? |

The judge is Claude Sonnet 4.6, a different model family than the agent (Kimi K2.5), so it is not grading its own output. The rubric uses four discrete buckets, and the one I'd point at as the rubric's main contribution is **0.9 — "right answer, wrong chunk"**. Without that bucket, a row where retrieval misses the canonical source but the agent answered correctly from an equivalent passage becomes either a false positive or a false negative. The 0.9 bucket keeps retrieval correctness and answer correctness observable as separate signals.

Read [`evals/calibration.md`](evals/calibration.md) before trusting any pass rate this thing produces. The 94% number is on 18 rows, single grader, one corpus. Read the caveats.

## Why no vector DB

Three reasons, and they compound.

One: for textual corpora where users use the document's own vocabulary, BM25 is competitive with or better than dense retrieval. The semantic-search lift mostly shows up when query vocabulary diverges from document vocabulary (paraphrase, multi-language, retail search). In legal, medical, and technical writing, vocabulary is the point.

Two: BM25 is interpretable. I can point at the exact term that scored a chunk. In compliance settings that property is the difference between "we can use this" and "we cannot."

Three: a 10-million-document BM25 index is a 200 MB pickle file. The same index in Pinecone is a recurring bill.

If you have a use case where embeddings clearly win (retail product search, cross-lingual retrieval, semantic deduplication), use embeddings. This project is for the other use cases, where people reach for vectors by reflex.

## What's in the repo

```
agentic-rag-bm25/
├── lib/
│   ├── expert_index.py        # BM25 indexer
│   ├── expert_agent.py        # Tool-calling agent (search_kb, read_section)
│   └── ingestion.py           # PDF/TXT → chunked markdown + BM25 index
├── ask-expert                 # CLI wrapper for the agent
├── evals/
│   ├── groundtruth.jsonl              # Guidance corpus gold set, 30 rows
│   ├── groundtruth-ml.jsonl           # Géron ML corpus gold set, 15 rows
│   ├── groundtruth-meditations.jsonl  # Meditations gold set, 12 rows
│   ├── calibration.md                 # Judge calibration writeup. Read this first.
│   ├── notes-meditations-chunking.md  # The negative result
│   ├── eval_harness/                  # Dataset loader, runner, scorer, report
│   └── run.sh                         # Convenience wrapper
├── setup.sh
└── requirements.txt
```

## Project status

Working:

- BM25 retrieval, agent loop, ingestion CLI, eval harness, calibrated judge
- Three corpora running with measured pass rates
- Reproducible reports per run

Pending:

- Live demo (Hugging Face Spaces)
- Adversarial calibration slice (edge-case rows for the judge)
- Inter-grader reliability pass (second human, kappa score)
- pypdf → pdftotext automatic fallback for old OCR'd PDFs
- OCR support for scanned PDFs (via ocrmypdf)
- Test suite

If you find a real-world corpus where this approach fails in an interesting way, open an issue.

## Related work worth reading

- Hailey Schoelkopf, *lm-evaluation-harness design notes*. The canonical reference for LLM eval rigor.
- Hamel Husain, *Your AI product needs evals* and *Creating an LLM-as-a-Judge* at hamel.dev. The practitioner's guide to production eval that this project's calibration protocol leans on.
- JJ Allaire's Inspect framework (UK AISI). Production eval framework whose Task / Solver / Scorer abstractions inspired this harness's structure.
- Anthropic's *Building effective agents*. The agent loop here is closer to that essay's "augmented LLM" pattern than to a LangChain-style chain.

## Author

Kunal Bhardwaj. Embedded systems engineer (autonomous drones) moving into applied AI. This repo is part of a 10-day public sprint to ship a portfolio piece I would actually use to argue for a role.

- LinkedIn: [linkedin.com/in/kunal-bhardwaj-61433818b](https://www.linkedin.com/in/kunal-bhardwaj-61433818b)
- Email: kunalbhardwaj598@gmail.com

If you're hiring for an applied AI or AI infrastructure role and this is the kind of work you want done, please reach out.

## License

MIT. See [LICENSE](LICENSE).
