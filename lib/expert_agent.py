"""Agentic RAG loop for ask-expert.

Supports two modes:
  - Single-domain: agent searches one book (old behavior)
  - Multi-domain (auto): agent searches across ALL books, then dives deep

Multi-domain tools:
  1. search_all(query, top_k) — BM25 search across ALL books
  2. search_domain(domain, query, top_k) — Deep search within one specific book
  3. read_section(domain, file, heading) — Read full text of a specific section

Single-domain tools (backward compatible):
  1. search_kb(query, top_k) — BM25 search in the selected book
  2. read_section(file, heading) — Read full text of a section
"""

import os
import sys
import json
import time
from pathlib import Path
from openai import OpenAI

# Local imports
sys.path.insert(0, str(Path(__file__).parent))
from expert_index import (
    get_or_build_index, get_or_build_global_index,
    search, search_by_domain, discover_domains, Chunk,
)

KB_ROOT = Path(os.environ.get("KB_ROOT", str(Path.home() / "knowledge-bases")))


# ══════════════════════════════════════════════════════════════════
# MULTI-DOMAIN TOOLS (auto mode)
# ══════════════════════════════════════════════════════════════════

def _build_multi_tools(domains: dict[str, Path]) -> list[dict]:
    """Build tool definitions for multi-domain mode."""
    domain_list = ", ".join(f'"{name}"' for name in sorted(domains.keys()))

    return [
        {
            "type": "function",
            "function": {
                "name": "search_all",
                "description": (
                    "Search across ALL books in the knowledge base. Returns short previews "
                    "from any book, with domain tags. Use this FIRST to discover which "
                    "books are relevant, then use search_domain or read_section to go deeper."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query — use precise technical terms"
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "Number of results (default 8, max 15)",
                            "default": 8
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_domain",
                "description": (
                    "Deep search within ONE specific book/domain. Use after search_all "
                    "when you want more results from a particular book. "
                    f"Available domains: {domain_list}"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": f"Domain name. One of: {domain_list}"
                        },
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "Number of results (default 5, max 10)",
                            "default": 5
                        }
                    },
                    "required": ["domain", "query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_section",
                "description": (
                    "Read the full text of a specific section. Use after searching "
                    "when you need the complete content, not just the preview."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "Domain name from search results"
                        },
                        "file": {
                            "type": "string",
                            "description": "Filename from search results"
                        },
                        "heading": {
                            "type": "string",
                            "description": "Section heading from search results"
                        }
                    },
                    "required": ["file", "heading"]
                }
            }
        }
    ]


# ══════════════════════════════════════════════════════════════════
# SINGLE-DOMAIN TOOLS (legacy mode)
# ══════════════════════════════════════════════════════════════════

SINGLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_kb",
            "description": (
                "Search the knowledge base for sections relevant to a query. "
                "Returns ranked results with chapter, heading, and text preview. "
                "Use specific technical terms for best results (BM25 keyword matching)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query — use precise technical terms"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return (default 5, max 10)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_section",
            "description": (
                "Read the full text of a specific section from the knowledge base. "
                "Use this after search_kb when you need the complete content of a "
                "section, not just the preview."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": "Filename from search results"
                    },
                    "heading": {
                        "type": "string",
                        "description": "Section heading from search results"
                    }
                },
                "required": ["file", "heading"]
            }
        }
    }
]


# ══════════════════════════════════════════════════════════════════
# TOOL EXECUTORS
# ══════════════════════════════════════════════════════════════════

def _format_results(results: list[dict], show_domain: bool = False,
                     preview_len: int = 500) -> str:
    """Format search results for the agent."""
    if not results:
        return "No results found. Try different keywords."

    output = []
    for r in results:
        preview = r['text'][:preview_len]
        if len(r['text']) > preview_len:
            preview += '...'

        domain_tag = f" [{r['domain']}]" if show_domain else ""
        output.append(
            f"[{r['rank']}] score={r['score']}{domain_tag} | {r['file']} → {r['heading']}\n"
            f"Chapter: {r['chapter']}\n"
            f"Text:\n{preview}"
        )
    return "\n\n---\n\n".join(output)


def exec_search_all(index, args: dict) -> str:
    """Search across all domains. Shorter previews to save tokens."""
    query = args["query"]
    top_k = min(args.get("top_k", 8), 15)
    results = search(index, query, top_k=top_k)
    # Short previews (200 chars) — search_all is for scanning, not reading
    return _format_results(results, show_domain=True, preview_len=200)


def exec_search_domain(index, args: dict) -> str:
    """Search within one specific domain."""
    domain = args["domain"]
    query = args["query"]
    top_k = min(args.get("top_k", 5), 10)
    results = search_by_domain(index, query, domain, top_k=top_k)
    if not results:
        # Check if domain exists at all
        known = set(c.domain for c in index.chunks)
        if domain not in known:
            return f"Unknown domain: '{domain}'. Available: {', '.join(sorted(known))}"
    return _format_results(results, show_domain=True)


def exec_search_kb(index, args: dict) -> str:
    """Single-domain search (legacy)."""
    query = args["query"]
    top_k = min(args.get("top_k", 5), 10)
    results = search(index, query, top_k=top_k)
    return _format_results(results, show_domain=False)


def exec_read_section(index, args: dict) -> str:
    """Read full text of a specific chunk."""
    target_file = args["file"]
    target_heading = args["heading"]
    target_domain = args.get("domain")  # optional in single-domain mode

    # Exact match
    for chunk in index.chunks:
        if chunk.file == target_file and chunk.heading == target_heading:
            if target_domain and chunk.domain != target_domain:
                continue
            return (
                f"Domain: {chunk.domain}\n"
                f"File: {chunk.file}\n"
                f"Chapter: {chunk.chapter}\n"
                f"Section: {chunk.heading}\n\n"
                f"{chunk.text}"
            )

    # Fuzzy match on heading
    for chunk in index.chunks:
        if chunk.file == target_file and target_heading.lower() in chunk.heading.lower():
            if target_domain and chunk.domain != target_domain:
                continue
            return (
                f"Domain: {chunk.domain}\n"
                f"File: {chunk.file}\n"
                f"Chapter: {chunk.chapter}\n"
                f"Section: {chunk.heading}\n\n"
                f"{chunk.text}"
            )

    return f"Section not found: {target_file} → {target_heading}. Use search to find valid sections."


# ══════════════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ══════════════════════════════════════════════════════════════════

def _multi_system_prompt(domains: dict[str, Path]) -> str:
    domain_list = "\n".join(f"  - {name}" for name in sorted(domains.keys()))
    return f"""You are a technical expert with access to multiple textbook knowledge bases:

{domain_list}

WORKFLOW:
1. Use search_all FIRST to find relevant sections across ALL books
2. Look at which books (domains) have the best results
3. Use search_domain to go deeper into the most relevant book(s)
4. Use read_section if you need full text of a specific section
5. Synthesize your answer combining knowledge from all relevant books

RULES:
- Base your answer strictly on the knowledge base content — do not hallucinate
- When citing, include both the book domain and section (e.g., "According to guidance/Section 2.2...")
- If multiple books cover the topic, compare and combine their perspectives
- If the knowledge base doesn't cover the topic, say so honestly
- Keep answers focused and technical — the user is an engineer
- Be efficient: 1-2 search_all calls, then 1-2 search_domain calls if needed
- After gathering enough context, STOP searching and synthesize your answer"""


def _single_system_prompt(domain: str) -> str:
    return f"""You are an expert in {domain}. You have access to a comprehensive textbook knowledge base.

WORKFLOW:
1. When asked a question, ALWAYS use search_kb first to find relevant sections
2. Read the search results carefully
3. If you need more detail, use read_section to get the full text
4. If initial results don't cover the question well, search again with different keywords
5. Synthesize your answer from the retrieved content

REFUSAL POLICY (critical — read carefully):
After 2-3 search attempts, evaluate whether any retrieved chunk DIRECTLY addresses
the user's question. "Directly addresses" means the chunk contains an explicit
statement, definition, or explanation of the specific thing being asked about —
not merely chunks that mention related concepts or share vocabulary.

If NO retrieved chunk directly addresses the question, you MUST refuse rather
than weave an answer from tangentially related content. Use this format:

    "The knowledge base does not specifically cover [the exact topic asked].
    Related material I found discusses [brief mention of what was found], but
    this does not substantively answer your question."

DO NOT:
- Weave an authoritative-sounding answer by combining unrelated chunks
- Extrapolate from related-but-not-answering content
- Hedge by saying "the corpus may not cover this" while still providing
  a full structured answer — that's the same failure as not refusing
- Treat "I found related content" as license to answer the original question

Refusal is the CORRECT behavior for out-of-corpus queries. A short, honest
refusal is much better than a confident-sounding fabrication.

RULES:
- Base your answer strictly on the knowledge base content — do not hallucinate
- Reference specific chapters and sections (e.g., "According to Section 2.2...")
- Include key equations by describing them (the text references equation images)
- Keep answers focused and technical — the user is an engineer
- Search efficiently: 1-2 search calls suffice when content is present;
  if your first 2-3 searches return only tangential material, that is itself
  the signal to refuse, not the signal to search more aggressively
- After gathering enough context (or confirming absence), STOP searching"""


# ══════════════════════════════════════════════════════════════════
# AGENT LOOP
# ══════════════════════════════════════════════════════════════════

MULTI_EXECUTORS = {
    "search_all": exec_search_all,
    "search_domain": exec_search_domain,
    "read_section": exec_read_section,
}

SINGLE_EXECUTORS = {
    "search_kb": exec_search_kb,
    "read_section": exec_read_section,
}


def run_agent(question: str, index, domain: str,
              max_tokens: int = 8192, max_turns: int = 10,
              verbose: bool = False, multi_domain: bool = False,
              return_trace: bool = False):
    """Run the agentic RAG loop.

    Args:
        question: User's question
        index: ExpertIndex (single-domain or global index)
        domain: Domain name (or "auto" for multi-domain)
        max_tokens: Token budget for Kimi (reasoning + answer)
        max_turns: Max agent loop iterations (safety limit)
        verbose: Print tool calls to stderr
        multi_domain: If True, use search_all + search_domain tools
        return_trace: If True, return (answer, trace_dict) instead of
            just the answer. Trace contains tool_calls list, turn count,
            and token usage. Used by the eval harness.

    Returns:
        If return_trace is False (default), the agent's final answer as
        a string. If True, a tuple (answer_str, trace_dict).
    """
    client = OpenAI(
        api_key=os.environ.get("WORKER_API_KEY", os.environ.get("MOONSHOT_API_KEY", "")),
        base_url=os.environ.get("WORKER_BASE_URL", "https://api.moonshot.ai/v1"),
    )

    # Pick tools and system prompt based on mode
    if multi_domain:
        domains = discover_domains(KB_ROOT)
        tools = _build_multi_tools(domains)
        system_prompt = _multi_system_prompt(domains)
        executors = MULTI_EXECUTORS
    else:
        tools = SINGLE_TOOLS
        system_prompt = _single_system_prompt(domain)
        executors = SINGLE_EXECUTORS

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    total_in = 0
    total_out = 0
    tool_call_count = 0
    trace_calls: list[dict] = []     # for return_trace
    last_cached = 0                  # updated each turn from usage

    def _ret(answer: str, turn_idx: int):
        if not return_trace:
            return answer
        trace = {
            "tool_calls": trace_calls,
            "turns": turn_idx + 1,
            "tokens_in": total_in,
            "tokens_out": total_out,
            "cached_tokens": last_cached,
        }
        return (answer, trace)

    for turn in range(max_turns):
        # Retry with backoff on 429 / overloaded errors
        for attempt in range(4):
            try:
                resp = client.chat.completions.create(
                    model=os.environ.get("WORKER_MODEL", "kimi-k2.5"),
                    messages=messages,
                    tools=tools,
                    max_tokens=max_tokens,
                )
                break
            except Exception as e:
                err_str = str(e)
                err_type = type(e).__name__
                if "429" in err_str or "overloaded" in err_str.lower():
                    wait = (attempt + 1) * 5  # 5s, 10s, 15s, 20s
                    if attempt == 0 and verbose:
                        print(f"  [DEBUG] {err_type}: {err_str[:300]}", file=sys.stderr)
                        print(f"  [DEBUG] turn={turn+1}, messages={len(messages)}, "
                              f"approx chars={sum(len(str(m)) for m in messages)}",
                              file=sys.stderr)
                    print(f"  [retry {attempt+1}/4] Kimi rate-limited, waiting {wait}s...",
                          file=sys.stderr)
                    time.sleep(wait)
                    if attempt == 3:
                        return _ret(
                            f"[Kimi API rate-limited after 4 retries. Error: {err_str[:200]}]",
                            turn,
                        )
                else:
                    raise

        msg = resp.choices[0].message
        total_in += resp.usage.prompt_tokens
        total_out += resp.usage.completion_tokens
        last_cached = (
            getattr(getattr(resp.usage, 'prompt_tokens_details', None), 'cached_tokens', 0) or 0
        )

        # If the model wants to call tools
        if resp.choices[0].finish_reason == "tool_calls" and msg.tool_calls:
            messages.append(msg)

            for tc in msg.tool_calls:
                tool_call_count += 1
                fn_name = tc.function.name
                fn_args = json.loads(tc.function.arguments)

                if verbose:
                    print(f"  [tool {tool_call_count}] {fn_name}({json.dumps(fn_args)})",
                          file=sys.stderr)

                if fn_name in executors:
                    result = executors[fn_name](index, fn_args)
                else:
                    result = f"Unknown tool: {fn_name}"

                # Record this tool call for the trace (truncate result preview)
                trace_calls.append({
                    "name": fn_name,
                    "args": fn_args,
                    "result_preview": (result[:300] if isinstance(result, str) else str(result)[:300]),
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

            continue

        # Model is done
        answer = msg.content
        if not answer:
            answer = "[Agent produced no answer — likely ran out of tokens during reasoning. Try a simpler question.]"

        mode_tag = "multi" if multi_domain else domain
        print(f"\n[expert-agent ({mode_tag}): {total_in} in ({last_cached} cached) / {total_out} out | "
              f"{tool_call_count} tool calls | {turn + 1} turns]",
              file=sys.stderr)

        return _ret(answer, turn)

    return _ret(
        "[Agent exceeded maximum turns without producing an answer. Try a more specific question.]",
        max_turns - 1,
    )
