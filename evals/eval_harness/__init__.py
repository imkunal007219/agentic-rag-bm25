"""Eval harness for agentic-rag-bm25.

Loads the ground-truth dataset, runs the RAG system over each row,
scores per-row results with type-appropriate scorers, and produces
aggregated reports.

Modules:
    dataset  — typed loader + validator for groundtruth.jsonl
    runner   — invokes the RAG agent on each sample, captures traces
    scorer   — four scorers (one per question_type)
    report   — aggregates Scores into metrics and writes JSON + Markdown
    cli      — entry point
"""
