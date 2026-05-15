"""Ingest a raw PDF or TXT file into the knowledge-base layout.

Pipeline:
    raw file -> extract text -> heading-detect or window-chunk
        -> write `## `-segmented markdown -> trigger build_index()

The existing BM25 pipeline (expert_index.py) consumes markdown files
with `## ` section headings under `KB_ROOT/<corpus>/`. This module is
the bridge from "arbitrary user-supplied document" to that layout.

CLI:
    python -m lib.ingestion --input book.pdf --corpus my_book
    python -m lib.ingestion --input notes.txt --corpus my_notes \\
        --kb-root ~/knowledge-bases
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from .expert_index import build_index, save_index

# Heading-like patterns in raw text. Order matters — more specific first.
# The bare "1. Title" pattern was dropped because numbered-list bullets in
# textbook prose ("1. First you would consider...") triggered hundreds of
# false-positive splits on a real-world test.
_HEADING_PATTERNS = [
    re.compile(r"^\s*CHAPTER\s+\d+\b.*$"),
    re.compile(r"^\s*Chapter\s+\d+\b.*$"),
    re.compile(r"^\s*SECTION\s+\d+(\.\d+)*\b.*$"),
    re.compile(r"^\s*Section\s+\d+(\.\d+)*\b.*$"),
    re.compile(r"^\s*\d+(\.\d+)+\s+\S.{0,80}$"),   # 1.2.3 Subtitle
]

_WORDS_PER_WINDOW = 800              # fallback window size
_MIN_BODY_CHARS = 50                 # mirrors expert_index.py drop threshold
_HEADING_DETECT_THRESHOLD = 3        # need this many to trust heading detection


def load_pdf(path: Path) -> str:
    """Extract text from a PDF as a single string (pages joined by blank lines).

    Failure modes left to the caller: scanned PDFs (no text layer) return
    empty pages; heavy-LaTeX or multi-column layouts may produce garbled
    text. For scanned PDFs, OCR (e.g. pytesseract) is the next step — not
    in scope for v1.
    """
    try:
        import pypdf
    except ImportError as e:
        raise ImportError(
            "pypdf is required for PDF ingestion. Install: pip install pypdf"
        ) from e

    reader = pypdf.PdfReader(str(path))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")
    text = "\n\n".join(pages)
    # pypdf occasionally emits unpaired UTF-16 surrogates (math symbols,
    # ligatures, mis-decoded glyphs). They'd later crash UTF-8 encoding
    # downstream. Sanitize by round-tripping through UTF-8 with replacement.
    return text.encode("utf-8", errors="replace").decode("utf-8")


def load_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _is_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) > 120:
        return False
    return any(pat.match(stripped) for pat in _HEADING_PATTERNS)


def to_markdown(text: str, source_name: str) -> str:
    """Convert raw text to markdown with `## ` section headings.

    Two strategies, picked automatically:
      - Heading-detection: scan for chapter/section markers in the text
        and promote them to `## `. Used when >= _HEADING_DETECT_THRESHOLD
        headings are found.
      - Fixed-size windows: split on word count with synthetic
        `## Section N` headings. Fallback for unstructured prose.
    """
    lines = text.splitlines()
    # Require a blank line before each heading candidate. Filters out
    # numbered list items embedded inside running prose, which were the
    # dominant source of false positives on a real-world textbook test.
    def heading_at(i: int) -> bool:
        if not _is_heading(lines[i]):
            return False
        if i == 0:
            return True
        return lines[i - 1].strip() == ""
    heading_idx = [i for i in range(len(lines)) if heading_at(i)]

    if len(heading_idx) >= _HEADING_DETECT_THRESHOLD:
        return _markdown_from_detected_headings(lines, heading_idx, source_name)
    return _markdown_from_windows(text, source_name)


def _markdown_from_detected_headings(
    lines: list[str], heading_idx: list[int], source_name: str
) -> str:
    out = [f"# {source_name}", ""]

    # Preamble = anything before the first heading
    if heading_idx[0] > 0:
        preamble = "\n".join(lines[:heading_idx[0]]).strip()
        if len(preamble) >= _MIN_BODY_CHARS:
            out += ["## Preamble", "", preamble, ""]

    for n, start in enumerate(heading_idx):
        end = heading_idx[n + 1] if n + 1 < len(heading_idx) else len(lines)
        heading = lines[start].strip()
        body = "\n".join(lines[start + 1:end]).strip()
        if len(body) < _MIN_BODY_CHARS:
            continue
        out += [f"## {heading}", "", body, ""]
    return "\n".join(out)


def _markdown_from_windows(text: str, source_name: str) -> str:
    words = text.split()
    sections: list[str] = []
    for i in range(0, len(words), _WORDS_PER_WINDOW):
        chunk = " ".join(words[i:i + _WORDS_PER_WINDOW])
        if len(chunk) < _MIN_BODY_CHARS:
            continue
        sec = i // _WORDS_PER_WINDOW + 1
        sections.append(f"## Section {sec}\n\n{chunk}\n")
    if not sections:
        raise ValueError("input text too short to ingest")
    return f"# {source_name}\n\n" + "\n".join(sections)


def ingest(input_path: Path, corpus_name: str, kb_root: Path) -> Path:
    """Convert a raw file into the corpus layout and build its BM25 index.

    Returns the corpus directory under kb_root.
    """
    input_path = Path(input_path).resolve()
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    suffix = input_path.suffix.lower()
    if suffix == ".pdf":
        raw = load_pdf(input_path)
    elif suffix in (".txt", ".md"):
        raw = load_txt(input_path)
    else:
        raise ValueError(
            f"unsupported file type: {suffix}. supported: .pdf, .txt, .md"
        )

    if len(raw.strip()) < _MIN_BODY_CHARS:
        hint = (" — this looks like a scanned/image PDF with no text layer. "
                "OCR is not supported in v1; convert it to text first "
                "(e.g. ocrmypdf input.pdf out.pdf)."
                if suffix == ".pdf" else "")
        raise ValueError(f"file appears empty or unreadable: {input_path}{hint}")

    # If input is already markdown with `## ` headings, trust the author.
    # The existing expert_index chunker splits on `## ` directly, so any
    # extra processing would be lossy.
    if suffix == ".md" and "\n## " in raw:
        md = raw
    else:
        md = to_markdown(raw, source_name=input_path.stem)

    corpus_dir = Path(kb_root) / corpus_name
    corpus_dir.mkdir(parents=True, exist_ok=True)
    out_file = corpus_dir / f"{input_path.stem}.md"
    out_file.write_text(md, encoding="utf-8")

    index = build_index(corpus_dir, domain=corpus_name)
    index_path = corpus_dir / ".index" / f"{corpus_name}.bm25.pkl"
    save_index(index, index_path)

    return corpus_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest a PDF or TXT file into the knowledge-base layout."
    )
    parser.add_argument("--input", required=True, type=Path,
                        help="path to a .pdf, .txt, or .md file")
    parser.add_argument("--corpus", required=True,
                        help="name for the new corpus (becomes the domain name)")
    parser.add_argument("--kb-root", type=Path, default=None,
                        help="knowledge-base root "
                             "(default: $KB_ROOT or ~/knowledge-bases)")
    args = parser.parse_args()

    kb_root = args.kb_root or Path(os.environ.get(
        "KB_ROOT", Path.home() / "knowledge-bases"
    ))

    try:
        corpus_dir = ingest(args.input, args.corpus, kb_root)
    except Exception as e:
        print(f"ingest failed: {e}", file=sys.stderr)
        sys.exit(1)

    md_count = sum(1 for _ in corpus_dir.glob("*.md"))
    print(f"ingested {args.input.name} -> {corpus_dir}")
    print(f"  {md_count} markdown file(s) written")
    print(f"  BM25 index: {corpus_dir}/.index/{args.corpus}.bm25.pkl")
    print(f"  query with: ask-expert --domain {args.corpus} -q '...'")


if __name__ == "__main__":
    main()
