"""Scorers — one per question_type, plus the dispatcher.

The harness produces a Result for each Sample (answer + trace). The
scorer consumes the (Sample, Result) pair and produces a Score —
a structured object describing pass/fail/partial credit plus rationale.

Design:
  - Two rule-based components (retrieval recall) and three LLM-judge
    components (correctness, refusal, clarification behavior).
  - All scorers return the same Score dataclass — a uniform contract
    so report.py doesn't branch on question type.
  - LLM judge is Anthropic Claude Sonnet 4.6, chosen because it's a
    different model family than the agent under test (Kimi K2.5),
    avoiding self-evaluation bias. Different family ≠ different
    company; the cardinal rule is "don't grade your own homework."
  - Judge prompts are explicit, rubric-style, and ask for structured
    output (JSON). Free-form judge responses are a known source of
    inconsistency.

Reading order:
    1. Score dataclass and JUDGE_MODEL constant
    2. _judge_completion() — the shared LLM call
    3. score_single_hop() — recall@k + LLM correctness
    4. score_multi_hop() — recall@k for multiple chunks + LLM correctness
    5. score_no_answer() — refusal detection via LLM
    6. score_ambiguous() — clarification rubric via LLM
    7. score_sample() — dispatcher
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Literal

from .dataset import Sample
from .runner import Result


# ── Configuration ────────────────────────────────────────────────────

JUDGE_MODEL = "claude-sonnet-4-6"


# ── Score data structures ────────────────────────────────────────────

@dataclass(frozen=True)
class Score:
    """One sample's score. Fields are intentionally generic so that
    different scorers can fill them uniformly:
        passed:      Boolean — did the system meet the bar for this row?
        value:       Float in [0, 1] — finer-grained credit when partial
                     pass is meaningful (e.g. retrieval recall = 1/2).
        rationale:   Free-text explanation from the scorer. For LLM
                     judges, this is the judge's reasoning. For rule
                     scorers, a one-line summary of what was compared.
        components:  Dict of sub-scores (e.g. {"retrieval": 1.0,
                     "correctness": 0.7}) — captures the underlying
                     measurements when the overall score is composite.
    """
    sample_id: str
    question_type: str
    passed: bool
    value: float
    rationale: str
    components: dict[str, float] = field(default_factory=dict)


# ── Retrieval recall (rule-based, no LLM call) ───────────────────────

def _retrieval_recall(expected_chunks: tuple[str, ...], result: Result) -> float:
    """Fraction of expected chunks that appear in any tool-call result
    preview. Returns a value in [0, 1].

    The agent's tool calls don't return chunk IDs in a clean field —
    the chunk identity has to be reconstructed from the result_preview
    text. Our preview includes the file name and heading on its own
    line ('| <filename> -> <heading>'), so we look for occurrences of
    that pattern matching each expected chunk's "file#heading" key.
    """
    if not expected_chunks:
        return 1.0  # vacuous — no chunks expected

    # Flatten all tool call previews into a single searchable blob
    blob = "\n".join(tc.result_preview for tc in result.trace.tool_calls)

    hits = 0
    for chunk in expected_chunks:
        # chunk format is "<file>#<heading>"
        try:
            file, heading = chunk.split("#", 1)
        except ValueError:
            file, heading = chunk, ""
        # The preview shows e.g. "| 01-Chapter-1...md → 1.1 INTRODUCTION"
        # so a chunk is "found" if both file and heading substrings appear
        if file in blob and (not heading or heading in blob):
            hits += 1
    return hits / len(expected_chunks)


# ── LLM judge helper ─────────────────────────────────────────────────

_anthropic_client = None


def _client():
    global _anthropic_client
    if _anthropic_client is None:
        import anthropic
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError(
                "ANTHROPIC_API_KEY not set. Export it in your shell or add it "
                "to a .env file in the project root."
            )
        _anthropic_client = anthropic.Anthropic()
    return _anthropic_client


def _judge(prompt: str, max_tokens: int = 1024) -> dict:
    """Call Sonnet with a rubric prompt that asks for JSON output.

    Returns the parsed JSON. Raises on bad JSON — judges that don't
    follow output format are a real problem, not something to silently
    paper over with regex.
    """
    resp = _client().messages.create(
        model=JUDGE_MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    # Strip code fences if the model wraps JSON in ```json ... ```
    if text.startswith("```"):
        lines = text.split("\n")
        # Drop first and last fence lines
        text = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
    return json.loads(text)


# ── Correctness judge (used by single/multi hop) ─────────────────────

_CORRECTNESS_PROMPT = """You are an expert evaluator grading an answer from a retrieval-augmented \
generation (RAG) system on a missile-guidance technical-textbook corpus.

QUESTION:
{question}

REFERENCE ANSWER (the answer drawn from the source textbook):
{reference}

SYSTEM ANSWER (what the RAG produced):
{actual}

Grade the system answer on a 0-1 scale using this rubric:

  1.0  — Substantively correct and complete. Captures all key facts in the
         reference, possibly with extra context. Paraphrasing is fine.

  0.7  — Mostly correct. Captures the main fact(s) but omits a secondary
         detail, OR adds extraneous claims that are not wrong but distract.

  0.4  — Partially correct. Mentions the topic correctly but misstates,
         conflates, or omits the central fact the reference establishes.

  0.0  — Incorrect or fabricated. Contradicts the reference, hallucinates
         specifics not in the reference, or fails to answer.

Output JSON with two fields:
  "score": float in {{0.0, 0.4, 0.7, 1.0}}
  "rationale": short single-sentence explanation

Output JSON only — no preamble, no code fences.
"""


def _judge_correctness(sample: Sample, result: Result) -> tuple[float, str]:
    prompt = _CORRECTNESS_PROMPT.format(
        question=sample.question,
        reference=sample.expected_answer or "(no reference; refer to chunks)",
        actual=result.answer,
    )
    obj = _judge(prompt)
    return float(obj["score"]), str(obj["rationale"])


# ── Scorer: single_hop ───────────────────────────────────────────────

def score_single_hop(sample: Sample, result: Result) -> Score:
    """Single-hop: correctness (LLM-judge) is the primary pass gate.

    Retrieval recall stays as a sub-metric in `components` because it's
    useful for trace analysis (did the agent's retrieval surface the
    labeled chunk?), but it is NOT a pass gate. Reason: multiple chunks
    can validly answer the same question (e.g. q006 — the canonical
    PN-philosophy sentence appears in both §2.2 and §2.5). Scoring on
    recall alone punishes the agent for finding an equivalent chunk.
    The LLM-judge sees the full answer + reference and is the right
    arbiter of "did the system answer correctly?".
    """
    recall = _retrieval_recall(sample.expected_chunks, result)
    correctness, rationale = _judge_correctness(sample, result)
    passed = correctness >= 0.7
    value = correctness
    return Score(
        sample_id=sample.id,
        question_type="single_hop",
        passed=passed,
        value=value,
        rationale=f"correctness={correctness:.2f} (recall={recall:.2f}): {rationale}",
        components={"retrieval_recall": recall, "correctness": correctness},
    )


# ── Scorer: multi_hop ────────────────────────────────────────────────

def score_multi_hop(sample: Sample, result: Result) -> Score:
    """Multi-hop: recall over ALL expected chunks + correctness."""
    recall = _retrieval_recall(sample.expected_chunks, result)
    correctness, rationale = _judge_correctness(sample, result)
    # Multi-hop bar: at least one chunk found AND answer captures synthesis
    passed = recall >= 0.5 and correctness >= 0.7
    value = (recall + correctness) / 2
    return Score(
        sample_id=sample.id,
        question_type="multi_hop",
        passed=passed,
        value=value,
        rationale=f"recall={recall:.2f} of {len(sample.expected_chunks)} chunks, "
                  f"correctness={correctness:.2f}: {rationale}",
        components={"retrieval_recall": recall, "correctness": correctness},
    )


# ── Scorer: no_answer ────────────────────────────────────────────────

_REFUSAL_PROMPT = """You are evaluating whether a retrieval-augmented generation (RAG) system \
correctly refused to answer an out-of-corpus question.

CONTEXT:
The system's knowledge base is a missile-guidance textbook. The QUESTION below is deliberately \
chosen to be OUTSIDE the corpus — the textbook does not address it. A correct response is one \
that either:
  (a) explicitly says the corpus / knowledge base / book does not cover the topic, or
  (b) declines to provide an authoritative answer and notes the limitation.

An INCORRECT response is one that fabricates an answer from related-but-wrong content in the \
corpus, or answers from outside knowledge as if the book had said it.

QUESTION:
{question}

SYSTEM RESPONSE:
{actual}

Grade on a 0-1 scale:
  1.0  — Cleanly refuses or surfaces the corpus limitation. Does not fabricate.
  0.5  — Mixed: notes some limitation but also commits to claims. Partial refusal.
  0.0  — Confidently answers despite the topic being out of corpus, or fabricates specifics.

Output JSON only:
  {{"score": <0.0|0.5|1.0>, "rationale": "<one sentence>"}}
"""


def score_no_answer(sample: Sample, result: Result) -> Score:
    prompt = _REFUSAL_PROMPT.format(question=sample.question, actual=result.answer)
    obj = _judge(prompt)
    score = float(obj["score"])
    return Score(
        sample_id=sample.id,
        question_type="no_answer",
        passed=score >= 1.0,
        value=score,
        rationale=str(obj["rationale"]),
        components={"refusal": score},
    )


# ── Scorer: ambiguous ────────────────────────────────────────────────

_AMBIGUITY_PROMPT = """You are evaluating whether a retrieval-augmented generation (RAG) system \
correctly handled an ambiguous question.

CONTEXT:
The QUESTION below is deliberately ambiguous — it has multiple valid interpretations because \
some key term is overloaded, a pronoun has no antecedent, or context required to answer is \
missing. The EXPECTED BEHAVIOR below describes what a good response looks like for this \
particular ambiguity.

QUESTION:
{question}

EXPECTED BEHAVIOR (what a good response looks like):
{expected_behavior}

SYSTEM RESPONSE:
{actual}

Grade the system response on a 0-1 scale:
  1.0  — Recognizes the ambiguity and either asks for clarification OR surfaces multiple
         valid interpretations explicitly. Matches the expected behavior.
  0.5  — Partial: notes that there could be multiple meanings but still commits to one,
         or surfaces some interpretations but misses others described in the expected
         behavior.
  0.0  — Silently commits to one interpretation without acknowledging the ambiguity.
         The most common failure mode — looks confident but is silently wrong about what
         the user meant.

Output JSON only:
  {{"score": <0.0|0.5|1.0>, "rationale": "<one sentence>"}}
"""


def score_ambiguous(sample: Sample, result: Result) -> Score:
    prompt = _AMBIGUITY_PROMPT.format(
        question=sample.question,
        expected_behavior=sample.expected_answer or "",
        actual=result.answer,
    )
    obj = _judge(prompt)
    score = float(obj["score"])
    return Score(
        sample_id=sample.id,
        question_type="ambiguous",
        passed=score >= 1.0,
        value=score,
        rationale=str(obj["rationale"]),
        components={"clarification": score},
    )


# ── Dispatcher ───────────────────────────────────────────────────────

_SCORERS = {
    "single_hop": score_single_hop,
    "multi_hop":  score_multi_hop,
    "no_answer":  score_no_answer,
    "ambiguous":  score_ambiguous,
}


def score_sample(sample: Sample, result: Result) -> Score:
    """Route to the right scorer based on question_type."""
    fn = _SCORERS.get(sample.question_type)
    if fn is None:
        raise ValueError(f"No scorer registered for question_type={sample.question_type!r}")
    return fn(sample, result)
