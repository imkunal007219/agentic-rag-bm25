"""BM25 index builder for the ask-expert RAG system.

How it works:
1. Reads all chapter .md files from a knowledge-base directory
2. Splits each file into chunks on '## ' headings (section-level)
3. Tokenizes each chunk (lowercase, strip markdown, split on whitespace)
4. Builds a BM25Okapi index over all tokenized chunks
5. Saves index + chunk metadata to a pickle file

The index is loaded instantly on subsequent runs (~5ms vs ~200ms rebuild).
"""

import os
import re
import pickle
import hashlib
from pathlib import Path
from dataclasses import dataclass, field
from rank_bm25 import BM25Okapi


# ── Data structures ──────────────────────────────────────────────

@dataclass
class Chunk:
    """One section from a knowledge-base chapter."""
    file: str          # source filename (e.g. "02-Chapter-2---Parallel-Navigation.md")
    heading: str       # section heading (e.g. "2.1 INTRODUCTION")
    chapter: str       # chapter title (e.g. "Parallel Navigation")
    text: str          # raw markdown text of this section
    domain: str = ""   # knowledge base name (e.g. "guidance")
    tokens: list = field(default_factory=list)  # tokenized words (for BM25)


@dataclass
class ExpertIndex:
    """Serializable BM25 index with chunk metadata."""
    domain: str
    chunks: list          # list of Chunk objects
    bm25: BM25Okapi       # the BM25 index
    source_hash: str      # hash of source files (to detect staleness)


# ── Tokenizer ────────────────────────────────────────────────────

# Markdown syntax to strip before tokenizing
_MD_NOISE = re.compile(
    r'!\[.*?\]\(.*?\)'     # images ![alt](path)
    r'|\[([^\]]*)\]\(.*?\)'  # links [text](url) → keep text
    r'|\*\*|__'            # bold markers
    r'|\*|_'               # italic markers
    r'|`{1,3}'             # code markers
    r'|^#{1,6}\s+'         # heading markers
    r'|<br>'               # HTML breaks
    r'|\-{3,}'             # horizontal rules
    r'|\|'                 # table pipes
    , re.MULTILINE
)

# Keep only word characters, hyphens, dots (for decimals/versions)
_SPLIT = re.compile(r'[^\w\-\.]+')

def tokenize(text: str) -> list[str]:
    """Convert markdown text to lowercase word tokens for BM25."""
    # Strip markdown syntax
    clean = _MD_NOISE.sub(lambda m: m.group(1) or ' ', text)
    # Lowercase and split
    words = _SPLIT.split(clean.lower())
    # Filter: keep words with at least 2 chars, drop pure numbers
    return [w for w in words if len(w) >= 2 and not w.isdigit()]


# ── Chunker ──────────────────────────────────────────────────────

def _extract_chapter_title(first_heading: str) -> str:
    """Extract a clean chapter title from the first heading in a file.
    '2[Parallel Navigation]' → 'Parallel Navigation'
    'Chapter 2 — Parallel Navigation' → 'Parallel Navigation'
    """
    # Pattern: N[Title] (our pdf-to-chapters format)
    m = re.match(r'\d+\[(.+)\]', first_heading)
    if m:
        return m.group(1)
    # Pattern: Chapter N — Title  or  Chapter N - Title
    m = re.match(r'(?:Chapter|CHAPTER)\s+\d+\s*[—\-:]\s*(.+)', first_heading, re.I)
    if m:
        return m.group(1)
    # Appendix
    m = re.match(r'Appendix\s+[A-Z]\b\s*[—\-:]?\s*(.*)', first_heading, re.I)
    if m:
        return m.group(1) or first_heading
    return first_heading


def chunk_file(filepath: Path) -> list[Chunk]:
    """Split a markdown file into section-level chunks on '## ' headings."""
    text = filepath.read_text(errors='replace')
    fname = filepath.name

    # Split on ## headings, keeping the heading text
    parts = re.split(r'^(## .+)$', text, flags=re.MULTILINE)

    # parts = [pre-heading text, heading1, body1, heading2, body2, ...]
    chunks = []
    chapter_title = fname  # fallback

    # Handle text before first heading (if any)
    if parts[0].strip():
        heading = "(preamble)"
        body = parts[0]
    else:
        heading = None
        body = None

    # Extract chapter title from the first heading
    if len(parts) > 1:
        first_h = parts[1].replace('## ', '').strip().strip('*')
        chapter_title = _extract_chapter_title(first_h)

    if heading and body and len(body.strip()) > 50:
        tokens = tokenize(body)
        if tokens:
            chunks.append(Chunk(
                file=fname, heading=heading,
                chapter=chapter_title, text=body.strip(), tokens=tokens
            ))

    # Process heading+body pairs
    for i in range(1, len(parts), 2):
        heading = parts[i].replace('## ', '').strip().strip('*')
        body = parts[i + 1] if i + 1 < len(parts) else ''

        # Skip tiny chunks (< 50 chars of actual text)
        if len(body.strip()) < 50:
            continue

        tokens = tokenize(body)
        if not tokens:
            continue

        chunks.append(Chunk(
            file=fname, heading=heading,
            chapter=chapter_title, text=body.strip(), tokens=tokens
        ))

    return chunks


# ── Index builder ────────────────────────────────────────────────

def _source_hash(kb_dir: Path) -> str:
    """Hash all .md file sizes+mtimes to detect changes."""
    h = hashlib.md5()
    for f in sorted(kb_dir.glob('*.md')):
        stat = f.stat()
        h.update(f"{f.name}:{stat.st_size}:{stat.st_mtime_ns}".encode())
    return h.hexdigest()


def build_index(kb_dir: str | Path, domain: str) -> ExpertIndex:
    """Build a BM25 index from all .md files in a knowledge-base directory.

    Args:
        kb_dir: path to the knowledge base (e.g. memory/knowledge-bases/guidance/)
        domain: name for this domain (e.g. "guidance")

    Returns:
        ExpertIndex with BM25 ready for searching
    """
    kb_dir = Path(kb_dir)
    if not kb_dir.is_dir():
        raise FileNotFoundError(f"Knowledge base not found: {kb_dir}")

    all_chunks = []
    for md_file in sorted(kb_dir.glob('*.md')):
        # Skip index and front matter
        if md_file.name in ('00-INDEX.md',):
            continue
        chunks = chunk_file(md_file)
        # Tag each chunk with its domain
        for c in chunks:
            c.domain = domain
        all_chunks.extend(chunks)

    if not all_chunks:
        raise ValueError(f"No chunks found in {kb_dir}")

    # Build BM25 from tokenized chunks
    corpus = [c.tokens for c in all_chunks]
    bm25 = BM25Okapi(corpus)

    return ExpertIndex(
        domain=domain,
        chunks=all_chunks,
        bm25=bm25,
        source_hash=_source_hash(kb_dir),
    )


def save_index(index: ExpertIndex, path: str | Path):
    """Serialize index to pickle."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(index, f)


def load_index(path: str | Path) -> ExpertIndex:
    """Load a previously saved index."""
    with open(path, 'rb') as f:
        return pickle.load(f)


def get_or_build_index(kb_dir: str | Path, domain: str,
                       cache_dir: str | Path = None) -> ExpertIndex:
    """Load cached index if fresh, otherwise rebuild.

    The index is rebuilt if the source files have changed (based on
    file sizes and modification times).
    """
    kb_dir = Path(kb_dir)
    if cache_dir is None:
        cache_dir = kb_dir / '.index'
    cache_dir = Path(cache_dir)
    pkl_path = cache_dir / f'{domain}.bm25.pkl'

    # Try loading cached index
    if pkl_path.exists():
        try:
            idx = load_index(pkl_path)
            if idx.source_hash == _source_hash(kb_dir):
                return idx
        except Exception:
            pass  # corrupted cache, rebuild

    # Build fresh
    idx = build_index(kb_dir, domain)
    save_index(idx, pkl_path)
    return idx


# ── Global (multi-domain) index ──────────────────────────────────

def _global_source_hash(kb_root: Path) -> str:
    """Hash all .md files across all domain directories."""
    h = hashlib.md5()
    for domain_dir in sorted(kb_root.iterdir()):
        if not domain_dir.is_dir():
            continue
        for f in sorted(domain_dir.glob('*.md')):
            stat = f.stat()
            h.update(f"{domain_dir.name}/{f.name}:{stat.st_size}:{stat.st_mtime_ns}".encode())
    return h.hexdigest()


def discover_domains(kb_root: str | Path) -> dict[str, Path]:
    """Find all knowledge-base domains (directories with .md files)."""
    kb_root = Path(kb_root)
    domains = {}
    if kb_root.is_dir():
        for d in sorted(kb_root.iterdir()):
            if d.is_dir() and list(d.glob('*.md')):
                domains[d.name] = d
    return domains


def build_global_index(kb_root: str | Path) -> ExpertIndex:
    """Build a unified BM25 index across ALL knowledge base domains.

    Each chunk is tagged with its domain name so search results show
    which book they came from.
    """
    kb_root = Path(kb_root)
    domains = discover_domains(kb_root)
    if not domains:
        raise FileNotFoundError(f"No knowledge bases found in {kb_root}")

    all_chunks = []
    for domain_name, domain_dir in domains.items():
        for md_file in sorted(domain_dir.glob('*.md')):
            if md_file.name in ('00-INDEX.md',):
                continue
            chunks = chunk_file(md_file)
            for c in chunks:
                c.domain = domain_name
            all_chunks.extend(chunks)

    if not all_chunks:
        raise ValueError(f"No chunks found across any domain in {kb_root}")

    corpus = [c.tokens for c in all_chunks]
    bm25 = BM25Okapi(corpus)

    return ExpertIndex(
        domain="_global_",
        chunks=all_chunks,
        bm25=bm25,
        source_hash=_global_source_hash(kb_root),
    )


def get_or_build_global_index(kb_root: str | Path) -> ExpertIndex:
    """Load cached global index if fresh, otherwise rebuild."""
    kb_root = Path(kb_root)
    cache_dir = kb_root / '.index'
    pkl_path = cache_dir / '_global_.bm25.pkl'

    if pkl_path.exists():
        try:
            idx = load_index(pkl_path)
            if idx.source_hash == _global_source_hash(kb_root):
                return idx
        except Exception:
            pass

    idx = build_global_index(kb_root)
    save_index(idx, pkl_path)
    return idx


def search_by_domain(index: ExpertIndex, query: str, domain: str,
                     top_k: int = 5) -> list[dict]:
    """Search only chunks from a specific domain within a global index."""
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    scores = index.bm25.get_scores(query_tokens)

    # Filter to only chunks from the target domain, then rank
    domain_indices = [i for i, c in enumerate(index.chunks) if c.domain == domain]
    ranked = sorted(domain_indices, key=lambda i: scores[i], reverse=True)[:top_k]

    results = []
    for rank, idx in enumerate(ranked, 1):
        chunk = index.chunks[idx]
        if scores[idx] <= 0:
            break
        results.append({
            'domain': chunk.domain,
            'file': chunk.file,
            'chapter': chunk.chapter,
            'heading': chunk.heading,
            'text': chunk.text,
            'score': round(float(scores[idx]), 3),
            'rank': rank,
        })
    return results


# ── Search ───────────────────────────────────────────────────────

def search(index: ExpertIndex, query: str, top_k: int = 5) -> list[dict]:
    """Search the BM25 index and return top-K results.

    Returns list of dicts:
        [{"file": str, "chapter": str, "heading": str,
          "text": str, "score": float, "rank": int}, ...]
    """
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    scores = index.bm25.get_scores(query_tokens)

    # Get top-K indices sorted by score descending
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    results = []
    for rank, idx in enumerate(ranked, 1):
        chunk = index.chunks[idx]
        if scores[idx] <= 0:
            break  # no more relevant results
        results.append({
            'domain': chunk.domain,
            'file': chunk.file,
            'chapter': chunk.chapter,
            'heading': chunk.heading,
            'text': chunk.text,
            'score': round(float(scores[idx]), 3),
            'rank': rank,
        })

    return results


# ── CLI for testing ──────────────────────────────────────────────

if __name__ == '__main__':
    import sys, json
    if len(sys.argv) < 3:
        print("Usage: expert_index.py <kb_dir> <query>")
        print("  e.g.: expert_index.py memory/knowledge-bases/guidance/ 'proportional navigation law'")
        sys.exit(1)

    kb_dir = sys.argv[1]
    query = ' '.join(sys.argv[2:])
    domain = Path(kb_dir).name

    print(f"Building/loading index for '{domain}'...", file=sys.stderr)
    idx = get_or_build_index(kb_dir, domain)
    print(f"Index: {len(idx.chunks)} chunks from {domain}", file=sys.stderr)

    results = search(idx, query, top_k=5)
    for r in results:
        print(f"\n--- [{r['rank']}] score={r['score']} | {r['file']} → {r['heading']} ---")
        # Print first 200 chars of text
        print(r['text'][:200] + '...' if len(r['text']) > 200 else r['text'])
