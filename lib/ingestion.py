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
    re.compile(r"^\s*BOOK\s+[IVXLCDM]+\.?\s*$"),    # BOOK II. / BOOK XII
    re.compile(r"^\s*Book\s+[IVXLCDM]+\.?\s*$"),
]

_WORDS_PER_WINDOW = 800              # fallback window size
_MIN_BODY_CHARS = 50                 # mirrors expert_index.py drop threshold
_HEADING_DETECT_THRESHOLD = 3        # need this many to trust heading detection

# Sub-section detection via PDF page-header repetition.
# Textbooks repeat the current section name with the page number on each
# page, e.g. "Voting Classifiers  | 191" or "192 | Chapter 7: Ensemble...".
# Real sub-section titles thus appear in BOTH the page-header form AND as
# standalone titles at the section start. Titlecase-looking noise (figure
# captions, page numbers, code) does not. We use that redundancy.
_PAGE_HEADER_RIGHT = re.compile(
    r"^\s*([A-Z][A-Za-z0-9'’ \-]{2,60})\s+\|\s+\d{1,4}\s*$"
)
_PAGE_HEADER_LEFT = re.compile(
    r"^\s*\d{1,4}\s+\|\s+(.+?)\s*$"
)

# Numbered-paragraph marker: "  5.  Word..." or "12.   Word..."
# Used for aphoristic/numbered texts (Meditations, Tractatus, Pensees, etc.)
# Requires 2+ spaces after the period AND a capital letter following — both
# rule out date fragments ("180 A.D."), decimals, and inline references.
_PARA_NUMBER = re.compile(r"^\s*(\d{1,3})\.\s{2,}[A-Z\"‘’“”]")
_MIN_PARA_MARKERS = 4   # need this many in a chapter body to trust the signal


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


def to_markdown(text: str, source_name: str, *, paragraph_split: bool = True) -> str:
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
        return _markdown_from_detected_headings(
            lines, heading_idx, source_name, paragraph_split=paragraph_split
        )
    return _markdown_from_windows(text, source_name)


def _detect_subsections(body: str) -> set[str]:
    """Extract sub-section titles from a chapter body using PDF page-header
    repetition as the signal.

    Returns the set of titles that appeared at least once in a page-header
    line. These are high-confidence — titlecase noise does not appear in
    page headers, so this filter rules out figure captions, code-comment
    titles, table labels, etc.
    """
    candidates: set[str] = set()
    for line in body.splitlines():
        stripped = line.strip()
        m = _PAGE_HEADER_RIGHT.match(stripped)
        if m:
            candidates.add(m.group(1).strip())
        else:
            m = _PAGE_HEADER_LEFT.match(stripped)
            if m:
                # Drop "Chapter N: ..." forms — those are book-level headers
                title = m.group(1).strip()
                if not title.lower().startswith("chapter "):
                    candidates.add(title)
    # Drop anything that contains "Chapter " — book-level, not sub-section
    return {c for c in candidates if "Chapter " not in c and len(c) >= 3}


def _split_body_by_subsections(body: str, subsections: set[str]) -> str:
    """Within a chapter body, promote standalone occurrences of detected
    sub-section titles to `## ` markdown headings AND drop the page-header
    repetitions (now noise after we've extracted them).
    """
    if not subsections:
        return body
    out: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        # Drop page-header lines — they served their purpose during detection
        if _PAGE_HEADER_RIGHT.match(stripped) or _PAGE_HEADER_LEFT.match(stripped):
            continue
        # Promote a standalone subsection-title line to a `## ` heading
        if stripped in subsections:
            out.append(f"## {stripped}")
        else:
            out.append(line)
    return "\n".join(out)


def _split_body_by_paragraph_numbers(body: str, chapter_heading: str) -> str | None:
    """For aphoristic/numbered texts, split a chapter body on `N. Word...`
    paragraph markers. Each marker becomes a `## <chapter> N.` sub-heading.

    Returns the rewritten body, or None if not enough markers were found
    to trust the signal (in which case caller leaves the body intact).
    """
    matches = [
        (i, m.group(1))
        for i, line in enumerate(body.splitlines())
        if (m := _PARA_NUMBER.match(line))
    ]
    if len(matches) < _MIN_PARA_MARKERS:
        return None
    chapter_label = chapter_heading.strip().rstrip(".")
    lines = body.splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        m = _PARA_NUMBER.match(line)
        if m:
            n = m.group(1)
            rest = line[m.end() - 1:]  # keep the leading capital letter
            out.append(f"## {chapter_label}.{n}")
            out.append(rest)
        else:
            out.append(line)
    return "\n".join(out)


def _markdown_from_detected_headings(
    lines: list[str], heading_idx: list[int], source_name: str,
    *, paragraph_split: bool = True,
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
        # Sub-section split: detect titles via page-header repetition, then
        # promote standalone occurrences within this chapter to `## `.
        subsections = _detect_subsections(body)
        body = _split_body_by_subsections(body, subsections)
        # If no titled sub-sections were found, fall back to numbered-paragraph
        # detection for aphoristic texts (Meditations, Tractatus, etc.).
        # Numbered-paragraph splits HELP when paragraphs have distinct vocab
        # (e.g. textbook lists) but HURT when paragraphs share thematic vocab
        # and BM25 can't isolate the right one (measured on Meditations:
        # 75% -> 58% pass rate). Caller can opt out via paragraph_split=False.
        if paragraph_split and not subsections:
            split = _split_body_by_paragraph_numbers(body, heading)
            if split is not None:
                # The chapter-level `## <heading>` will be emitted below; the
                # split injects `## <heading>.N` markers within. The leading
                # chapter line is redundant once paragraphs are promoted, so
                # skip it and emit just the paragraph chunks.
                out += [split, ""]
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


def ingest(input_path: Path, corpus_name: str, kb_root: Path,
           *, paragraph_split: bool = True) -> Path:
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
        md = to_markdown(raw, source_name=input_path.stem,
                         paragraph_split=paragraph_split)

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
    parser.add_argument("--no-paragraph-split", action="store_true",
                        help="disable numbered-paragraph splitting "
                             "(use for aphoristic texts where small chunks "
                             "hurt BM25 retrieval, e.g. Meditations)")
    args = parser.parse_args()

    kb_root = args.kb_root or Path(os.environ.get(
        "KB_ROOT", Path.home() / "knowledge-bases"
    ))

    try:
        corpus_dir = ingest(args.input, args.corpus, kb_root,
                            paragraph_split=not args.no_paragraph_split)
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
