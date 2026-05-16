# LinkedIn launch post

Paste this directly into LinkedIn the same day the Medium post goes live, ideally a couple of hours after. The first 130 characters are what shows above "see more" on the feed, so the hook is front-loaded.

---

I gave Claude my engineering books to read. Then I spent twice as long building the eval harness to check it wasn't lying to me.

I have a day job in autonomous drone systems and roughly zero hours to read textbooks the way I used to. So I started handing PDFs to Claude. That worked, then it stopped working, then I built an agentic RAG to do the retrieval, then I noticed the agent was sometimes confidently wrong and I had no way to tell.

The last problem is what most public RAG demos skip. How do you actually know it works.

Two months later, here is what I have:

- An open-source agentic RAG with BM25 retrieval. No vector DB, no LangChain, about 200 lines of agent code.
- A type-aware eval harness with an LLM judge I measured against my own hand-grades. 94% exact-match agreement on 18 calibration rows. The first version of the judge got 39%. The writeup explains the four rubric iterations it took to close that gap.
- Three corpora running through the same harness with no per-corpus tuning. Pass rates between 75% and 80%.
- One reversed result I am specifically proud of: a chunking technique that lifted one corpus by 33 points regressed another by 17. The harness caught it on the first run. Calibration writeup explains why.

I am actively looking for my next role. Applied AI engineering, AI infrastructure, evaluation, RAG, agent systems. Remote or relocation, both fine.

Repo, methodology, the full negative-result writeup: github.com/imkunal007219/agentic-rag-bm25
Full story on Medium: [PASTE MEDIUM URL HERE AFTER PUBLISHING]

If this is the kind of work you want done at your company, message me. If you are building production eval right now and want to compare notes on the calibration protocol, also message me.

#AppliedAI #LLMEvaluation #AgenticRAG
