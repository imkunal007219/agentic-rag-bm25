Agentic RAG BM25
================

Terminal-native RAG for technical textbooks. BM25 keyword search + LLM tool-calling. No vector database, no embeddings, no LangChain—just ~200 lines of Python.

Query engineering knowledge bases from the CLI using an agentic loop that searches, reads, and synthesizes until it finds the answer. Works with any OpenAI-compatible API (Kimi, DeepSeek, Ollama).

Quick Start
-----------

```bash
# 1. Clone and install deps
git clone https://github.com/imkunal007219/agentic-rag-bm25.git
cd agentic-rag-bm25
./setup.sh

# 2. Configure API (Kimi, DeepSeek, or Ollama)
export WORKER_API_KEY="your-api-key"
export WORKER_BASE_URL="https://api.moonshot.ai/v1"  # or DeepSeek/Ollama
export WORKER_MODEL="kimi-k2.5"                      # or "deepseek-chat"

# 3. Add textbooks
export KB_ROOT="$HOME/knowledge-bases"
mkdir -p $KB_ROOT/control-systems
cp textbook-chapter.md $KB_ROOT/control-systems/

# 4. Ask questions
ask-expert -q "How do I tune a PID controller?" --domain control-systems --verbose
```

How It Works
------------

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   User      │────▶│  LLM Agent   │────▶│  Tool Call  │
│  Question   │     │ (Kimi/etc)   │     │             │
└─────────────┘     └──────────────┘     └──────┬──────┘
       ▲                                         │
       │                              ┌─────────▼──────────┐
       │                              │  BM25Okapi Index   │
       │                              │  (keyword search)  │
       │                              └─────────┬──────────┘
       │                                         │
       │     ┌──────────────┐     ┌─────────────▼──────┐
       └─────│   Final      │◀────│  Search Results    │
             │   Answer     │     │  (text chunks)     │
             └──────────────┘     └────────────────────┘
```

1. Agent receives question + tool definitions (search_all, search_domain, read_section)
2. LLM decides to search across books or dive deep into one
3. BM25 index returns ranked text chunks
4. Agent reads full sections if needed
5. Loop continues until LLM synthesizes final answer

Usage Examples
--------------

Single-domain (one book):
```bash
ask-expert -q "What is the guidance gain matrix?" --domain guidance-systems
```

Multi-domain (search all books, auto-select):
```bash
ask-expert -q "Compare optimal control vs PID" --verbose
```

Force index rebuild:
```bash
ask-expert -q "Question?" --domain physics --rebuild-index
```

List available domains:
```bash
ask-expert --list-domains
```

Add Your Own Books
------------------

Drop markdown files into `$KB_ROOT/<domain-name>/`. The indexer chunks on `##` headings.

```
$KB_ROOT/
├── aerodynamics/
│   ├── lift-theory.md      # Chapters with ## Section headings
│   └── drag-models.md
└── propulsion/
    ├── rocket-engines.md
    └── turbofans.md
```

Files are automatically indexed on first query (cached as `.pkl`).

Architecture
------------

**expert_index.py** (~80 lines)
- Recursive markdown chunking on `##` headings
- BM25Okapi indexing with pickle caching
- Search across all domains or filter by domain

**expert_agent.py** (~120 lines)
- Tool definitions for `search_all`, `search_domain`, `read_section`
- Agent loop with retry logic for rate limits
- Supports both single-domain and multi-domain modes

**ask-expert** (~30 lines)
- CLI argument parsing
- Domain auto-discovery
- Index lifecycle management

Why BM25 (Not Vectors)?
-----------------------

- **Deterministic**: Same query = same results every time
- **Zero embedding cost**: No API calls to embed documents
- **Fast**: Local index loads in milliseconds
- **Precise**: Technical terms (e.g., "Lyapunov stability", "Ziegler-Nichols") match exactly
- **Simple**: No vector DB to configure, no dimensionality to tune

For engineering textbooks with exact terminology, BM25 often outperforms semantic search.

Provider Examples
-----------------

**Kimi K2.5** (Moonshot)
```bash
export WORKER_API_KEY="sk-..."
export WORKER_BASE_URL="https://api.moonshot.ai/v1"
export WORKER_MODEL="kimi-k2.5"
```

**DeepSeek**
```bash
export WORKER_API_KEY="sk-..."
export WORKER_BASE_URL="https://api.deepseek.com/v1"
export WORKER_MODEL="deepseek-chat"
```

**Ollama (Local)**
```bash
export WORKER_API_KEY="ollama"
export WORKER_BASE_URL="http://localhost:11434/v1"
export WORKER_MODEL="llama3.1:70b"
```

Performance
-----------

Tested on aerospace and control theory textbooks:
- **Typical tool calls**: 2-4 per question
- **Latency**: 5-15 seconds (depending on provider)
- **Cost**: ~$0.02-0.05 per query (Kimi K2.5)

Author
------

**Kunal Bhardwaj** — Systems engineer working on autonomous drones and AI-powered developer tools. Building at the intersection of embedded systems and LLM workflows.

- [Medium](https://medium.com/@kunalbhardwaj598/i-was-burning-through-claude-codes-weekly-limit-in-3-days-here-s-how-i-fixed-it-0344c555abda)
- [LinkedIn](https://www.linkedin.com/in/kunal-bhardwaj-61433818b)
- [Claude Coworker Model](https://github.com/imkunal007219/claude-coworker-model) — The worker-model toolkit this project builds on

License
-------

MIT