#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${HOME}/.local/share/agentic-rag"
BIN_DIR="${HOME}/.local/bin"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="${INSTALL_DIR}/venv/bin/python3"

echo "=== Agentic RAG (BM25 + Tool-Calling) Setup ==="
echo ""

# 1. Create venv
echo "[1/4] Creating Python venv at ${INSTALL_DIR}..."
mkdir -p "${INSTALL_DIR}"
python3 -m venv "${INSTALL_DIR}/venv"
source "${INSTALL_DIR}/venv/bin/activate"

# 2. Install deps
echo "[2/4] Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r "${SCRIPT_DIR}/requirements.txt"

# 3. Install ask-expert with venv shebang + correct lib path
echo "[3/4] Installing ask-expert to ${BIN_DIR}..."
mkdir -p "${BIN_DIR}"

# Rewrite shebang to venv Python and lib path to installed location
sed "1s|#!/usr/bin/env python3|#!${VENV_PYTHON}|" \
    "${SCRIPT_DIR}/ask-expert" > "${BIN_DIR}/ask-expert"
chmod +x "${BIN_DIR}/ask-expert"

# Copy lib files to install dir (ask-expert resolves relative to its own location)
cp -r "${SCRIPT_DIR}/lib" "${INSTALL_DIR}/lib"

# Fix the sys.path in installed copy to point to installed lib
sed -i "s|str(Path(__file__).resolve().parent / \"lib\")|\"${INSTALL_DIR}/lib\"|" \
    "${BIN_DIR}/ask-expert"

echo "  ✓ ask-expert"

# 4. Check config
echo "[4/4] Checking environment..."
if [ -z "${WORKER_API_KEY:-}" ] && [ -z "${MOONSHOT_API_KEY:-}" ]; then
    echo ""
    echo "⚠  No API key found. Set in your shell profile:"
    echo ""
    echo "  export WORKER_API_KEY=\"your-key-here\""
    echo "  export WORKER_BASE_URL=\"https://api.moonshot.ai/v1\"  # or DeepSeek/Ollama"
    echo "  export WORKER_MODEL=\"kimi-k2.5\"                      # or deepseek-chat, etc."
fi

if [ -z "${KB_ROOT:-}" ]; then
    echo ""
    echo "⚠  KB_ROOT not set. Default: ~/knowledge-bases/"
    echo "  export KB_ROOT=\"/path/to/your/knowledge-bases\""
    echo ""
    echo "  Knowledge base structure:"
    echo "    \$KB_ROOT/"
    echo "    ├── physics/          # domain name = folder name"
    echo "    │   ├── chapter1.md"
    echo "    │   └── chapter2.md"
    echo "    └── control-systems/"
    echo "        ├── intro.md"
    echo "        └── pid-tuning.md"
fi

echo ""
echo "=== Done! ==="
echo ""
echo "Make sure ${BIN_DIR} is on your PATH, then try:"
echo "  ask-expert --list-domains"
echo "  ask-expert -q 'your question here'"
