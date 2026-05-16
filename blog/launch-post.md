# I gave Claude full engineering books to read. Then I built the eval harness to check it wasn't lying to me.

*A story about Claude Code token bleed, an agentic RAG with BM25 (no vector DB, no LangChain), and the LLM-judge that ended up 94% in agreement with a human grader. Open-source repo linked at the end.*

---

I have a confession that probably won't surprise anyone who works full-time and tries to learn alongside their job. I do not have time to read engineering textbooks the way I used to in college. I want to. I buy them. I open them. I get four pages in and then a Slack notification, a flight log to extract, a child of someone in my family asking what plants eat for breakfast, and three days later the bookmark hasn't moved.

So like a lot of people in 2026, I started giving the books to Claude.

The early version was stupid. I would paste a chapter into Claude Code and ask it to explain a concept. Sometimes that worked. Often I would realize halfway through Claude's answer that it was answering the question I asked, not the question I should have asked, and I had no way to tell whether what it said was actually in the chapter or whether it was extrapolating from priors. I was trusting the output by vibe.

The next version was less stupid. I started feeding entire PDFs in, and that worked better when I converted them to markdown and dropped them in an Obsidian vault. Markdown is the format Claude is most fluent in, and Obsidian gave me a way to organize the files without thinking about it. Now I could ask Claude things like "explain proportional navigation, then quote the section it came from" and get something I could trust enough to use.

There was a new problem.

## The token bleed

I am cheap. I am especially cheap about my Claude Code budget because I learned the hard way how fast you can burn through the weekly limit. (I wrote that one up [here](https://medium.com/@kunalbhardwaj598/i-was-burning-through-claude-codes-weekly-limit-in-3-days-here-s-how-i-fixed-it-0344c555abda) if you have not read it. Short version: I built a cheaper worker model to take the boring parts off Claude so the expensive model could think.)

So every time I asked Claude "go look at chapter 4 of this book and tell me about the Lyapunov stability proof," it would re-read the whole book to find the answer. Tens of thousands of tokens per question. Sometimes I would ask three follow-ups and watch my weekly limit visibly shrink.

The fix was the same shape as last time. Put a cheaper agent in front. Have it do the retrieval. Let the expensive model see only the relevant chunks. Let Claude reason, not search.

That is what RAG is. Retrieval-augmented generation. I had been about to build a RAG without knowing the acronym.

## A career pivot, in parallel

Around this time I also started doing something I had been putting off for a year. I started actually moving my career toward applied AI engineering.

I spent five years building autonomous drones for a small startup. Embedded systems, sensor fusion, MAVLink, flight controllers. It is work I am still close to. The field I want to be in next, though, is applied AI: building systems that wrap LLMs, measure them, ship them. So in parallel with this token-saving project I started studying RAG, evaluation, and agent design.

The two threads merged. The token-saving project was a RAG. I might as well build it well. And the more I read about RAG, the more I noticed that almost every public RAG demo was missing the part I cared about most: how do you know it works.

## Why BM25, and why no vector DB

The default 2026 RAG tutorial goes: chunk your documents, embed with OpenAI or whatever, put the vectors in Pinecone or Chroma or Weaviate, retrieve top-K with cosine similarity, feed to LLM.

I did not do this.

I picked BM25 instead. BM25 is a 1994 retrieval algorithm that ranks documents by keyword frequency, with two corrections: rarer words count more (IDF), and longer documents get penalized so they do not always win. No embeddings. No vector index. Just keyword matching with two well-tuned knobs.

The hipster choice, I know. People who have built RAG for a living will roll their eyes. But hear me out.

For most textual corpora where users actually use the document's own vocabulary, BM25 is competitive with or better than dense retrieval. The big embedding lift mostly shows up when the user's vocabulary diverges from the document. Paraphrase, multi-language, retail product search. In legal, medical, defense, technical writing, vocabulary is the point. A lawyer searching "Section 230" does not want a vector neighbor of "Section 230." They want Section 230.

BM25 is also interpretable. I can point at the exact word that scored a chunk highest. For a hiring manager evaluating whether your RAG can ship in a regulated environment, that property is the difference between "yes" and "no."

And selfishly: a 10-million-document BM25 index is a 200 MB pickle file. The same thing in Pinecone is a recurring bill I would have to explain to nobody but myself, and I would still resent it.

If you have a use case where embeddings clearly win, use embeddings. I am not religious about this. But every time I have tested BM25 on a technical corpus, it has either matched or beaten dense retrieval, and it has done so on a laptop with no cloud account.

## Building the agent

The agent is small. About 200 lines of Python. It exposes three tools to the LLM:

- `search_kb` — BM25 over a chosen corpus, returns ranked snippets
- `read_section` — fetch a full section by heading
- `search_all` — BM25 over every loaded corpus, when the user has not picked one

The LLM (Kimi K2.5, because it is cheap and good enough for the agent role) decides on each turn whether to search, read, search again, or commit to an answer. The system prompt has policies for three failure modes. Refuse if the answer is not in the corpus. Clarify if the question is ambiguous. Synthesize if you have enough material, even if it took two rounds of searching.

This works. I run it daily over five corpora in my Obsidian vault, mostly on textbooks I keep meaning to read.

But after a few weeks, two things started happening.

The first was that the agent was sometimes giving me incomplete answers. Things like "Marcus Aurelius wrote about death in Book IX section 3" when the canonical passage was actually in Book IV section 5. The retrieval was missing the right chunk, the agent was answering from whatever it did get, and the answer looked confident enough that I could not tell.

The second was token usage creeping up as my questions got more complex. Multi-hop questions, comparison questions, "tell me about X and how it relates to Y" questions. The agent would thrash, search five times, read three sections, hit its turn budget. Sometimes give up. Sometimes hallucinate something plausible.

I had two options. I could keep guessing about the agent's behavior and tweak the prompt every time something looked off. Or I could measure it.

## The thing that took longer than the agent: the eval harness

I built a tiny evaluation harness. It is in the repo. The structure is unfashionable: just a dataset loader, an agent runner, a scorer, and a reporter. No fancy framework.

The dataset is a JSONL file. Each row is a question, a reference answer, the chunks where the answer should live, and a question type tag. Four types: single_hop (answer is in one chunk), multi_hop (you need to synthesize from multiple chunks), no_answer (out of corpus, the agent should refuse), and ambiguous (the agent should clarify or surface multiple readings).

The scorer is type-aware. Different question types deserve different rules. Single_hop scores both retrieval recall (did we get the expected chunk) and answer correctness (did we say the right thing). Multi_hop does recall@k. No_answer rewards refusal. Ambiguous rewards clarification behavior.

Then the question that every public RAG demo I have read seems to skip: who decides whether the answer was correct?

I am using an LLM judge. Claude Sonnet 4.6. Different model family from the agent (Kimi) so the judge is not grading its own output. Discrete-bucket rubric. Per-row rationale captured.

This was where most of my work actually happened.

## The judge does not work until you measure it

If you have ever built an LLM judge, you know the first version always looks great. Your numbers go up. Your prompt change "works." Confidence is high.

Then you hand-grade a few rows and find that your judge is collapsing everything borderline into the middle bucket regardless of actual quality. The technical term for this is central-tendency bias. The practical term is that your eval is a vibe check with extra steps.

My first rubric had four buckets: 0.0 (wrong), 0.4 (incomplete), 0.7 (thin or imprecise), 1.0 (correct). On hand-grading, my human grader (me, blind, on a different day) also collapsed into 0.7 for anything borderline. The judge agreed with the human at a respectable-looking rate. It was a respectable-looking lie. We were both reaching for the same wrong bucket.

I went through four rubric revisions trying to fix the 0.7 bucket. None of them worked.

The version that finally did something different was a complete redesign. I collapsed the muddled middle bucket. Then I added a separate bucket at 0.9 for one specific case: **right answer, wrong chunk.** This is the case where retrieval missed the canonical source, but the agent answered correctly from an equivalent passage. Before that bucket, this case was either a false positive (you scored it 1.0 and papered over a retrieval miss) or a false negative (you scored it 0.4 and punished a correct answer).

That single split — keeping retrieval correctness and answer correctness as observable signals — was the move that fixed the rubric.

## The headline number

I hand-graded 18 rows under the new rubric. I re-scored them with both judges (old and new) and compared.

| Judge | Exact-match agreement with human |
|---|---:|
| Old judge (v1, four-bucket with 0.7) | 7/18 (39%) |
| New judge (v2, with the 0.9 split) | **17/18 (94%)** |

The single miss is a row where the judge said 0.9 and the human said 1.0. Within one bucket. I am calling that the noise floor of single-grader self-consistency.

Here is the part that took me longer to understand than I want to admit. The first time I ran this comparison, I anchored both judges against the original hand-grades that had been written under the old rubric. Under that anchor, the new judge looked like a marginal regression. I almost shipped that conclusion.

What I missed was that I was scoring the new judge against grades that baked in the old rubric's "thin answers are 0.7" rule, which the new judge explicitly rejected. Apples-to-oranges. I re-anchored the hand-grades under the new rubric, re-ran the comparison, and the 39%-vs-94% gap appeared.

This is the kind of methodological hole that quietly invalidates most LLM-judge comparisons I see in public repos. If your judge and your human grader are using different rubrics, the agreement number you compute is measuring rubric drift, not judge quality. The full writeup, with the per-row table of which grades shifted and which stayed, is in [evals/calibration.md](https://github.com/imkunal007219/agentic-rag-bm25/blob/master/evals/calibration.md).

## Three corpora, three pass rates, one reversed result

To make sure the harness was not over-fit to a single corpus, I ran the same agent and judge against three very different ones.

| Corpus | Domain | Pass rate |
|---|---|---:|
| Missile guidance textbook | Technical, equation-heavy | 76% |
| Géron, *Hands-On Machine Learning* | Semi-technical | 80% |
| Marcus Aurelius, *Meditations* | Classical philosophy | 75% |

Same agent prompt. Same judge. No per-corpus tuning. The fact that the agent generalizes across a missile guidance book, an ML textbook, and a 2nd-century Stoic philosopher with no domain-specific changes is the cross-domain proof for the system. That is the number I would put in the executive summary.

The number I would actually defend in an interview is a different one.

## The negative result I am proud of

When I added a sub-section chunking technique to ingestion (splitting chapter chunks on detected sub-headings), the ML eval jumped from 47% to 80%. Big win, easy story.

I applied the same technique to Meditations. Pass rate dropped from 75% to 58%.

Same code. Same agent. Same judge. Opposite effect on different corpora.

Géron's chapters have sub-section headings like "Bagging and Pasting." That heading carries query-matching vocabulary; when someone asks about bagging, the heading itself is part of why BM25 ranks the right chunk first. Meditations does not have semantic sub-headings. The sub-sections are numbered paragraphs. When BM25 ranks 200 small chunks of similar thematic vocabulary against a query like "what does Marcus say about death," it picks wrong, because none of the small chunks dominate on the term "death" and the agent ends up reading the wrong one.

Chunking is not universal. The optimal granularity is a property of the corpus, not of the technique.

I reverted Meditations to chapter-level chunking, kept the sub-section code in the ingestion module behind a flag, and wrote up the finding. That writeup is at [evals/notes-meditations-chunking.md](https://github.com/imkunal007219/agentic-rag-bm25/blob/master/evals/notes-meditations-chunking.md).

A uniformly rising chart on three corpora invites the obvious question: did you tune to your eval set. An A/B where one corpus moves the wrong way, with a mechanical explanation for why, is harder to dismiss. The negative result was the harness flagging something the agent's outputs alone could not have told me.

## What I learned

Two things, and neither came from a tutorial.

The first is that the eval is where the engineering is. I spent roughly twice as long on the harness and the calibration as I did on the agent itself, and I would do it that way again the next time. The agent is the thing you demo. The harness is the thing that lets you keep changing the agent without making it worse.

The second is that negative results are more credible than positive ones. Every portfolio piece I have seen presents a smooth chart going up and to the right. Mine has a place where the chart goes the wrong way, and the only thing that recovered from that was the harness telling me. If you are an engineer trying to distinguish your work from the hundreds of LangChain wrappers on GitHub, find the place where your version failed in an interesting way. Write that part up specifically.

## What this is, what it is not

It is an open-source agentic RAG with a calibrated eval harness. Three corpora. 94% judge-human agreement on the calibration set. Cross-domain pass rate of 75 to 80 percent. MIT-licensed. Runs on a laptop. No vector database. No LangChain.

It is not a production drop-in for your company's RAG. The code is small and the test coverage is honestly weak. I have a roadmap with the gaps called out.

If you are building RAG in a regulated, air-gapped, or cost-sensitive environment, this is the reference design I wish I had had two months ago. Clone it, read the calibration writeup, ignore my prose, and steal the methodology.

If you are hiring for applied AI or AI infrastructure roles where the work is closer to "make this measurably good" than "ship the next demo," I am open to roles. Information at the bottom.

## Links

- The repo: [github.com/imkunal007219/agentic-rag-bm25](https://github.com/imkunal007219/agentic-rag-bm25)
- Judge calibration writeup: [evals/calibration.md](https://github.com/imkunal007219/agentic-rag-bm25/blob/master/evals/calibration.md)
- The negative result: [evals/notes-meditations-chunking.md](https://github.com/imkunal007219/agentic-rag-bm25/blob/master/evals/notes-meditations-chunking.md)
- The previous Medium post about Claude Code token bleed: [I was burning through Claude Code's weekly limit in 3 days. Here's how I fixed it.](https://medium.com/@kunalbhardwaj598/i-was-burning-through-claude-codes-weekly-limit-in-3-days-here-s-how-i-fixed-it-0344c555abda)

## Related work that shaped this

I would not have known how to calibrate the judge without [Hamel Husain](https://hamel.dev)'s writing on LLM evals, particularly his "Creating an LLM-as-a-Judge that drives business results" piece. The structural choices in the harness (typed dataset, type-aware scorers, separation of agent run from scoring) are loosely shaped by [Inspect AI](https://inspect.ai-safety-institute.org.uk/) from the UK AI Safety Institute. Hailey Schoelkopf's notes on `lm-evaluation-harness` are the canonical reference for what an eval framework should look like at scale. I am standing on their work.

## Find me

- LinkedIn: [linkedin.com/in/kunal-bhardwaj-61433818b](https://www.linkedin.com/in/kunal-bhardwaj-61433818b)
- Email: kunalbhardwaj598@gmail.com

If you read this far and have a critique of the calibration methodology, the chunking choices, or the agent loop, I want to hear it. Pull requests, issues, or a DM all work. If you found a real-world corpus where this approach fails in an interesting way, that is the most useful feedback I can get.
