#!/usr/bin/env bash
# Wire the bundled sample corpora into your KB_ROOT and ask the agent
# a question against them. Run after ./setup.sh and after setting
# WORKER_API_KEY for the agent provider.
#
# Usage:
#   ./examples/try-sample.sh
#   ./examples/try-sample.sh "What does Marcus Aurelius say about death?"

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KB_ROOT="${KB_ROOT:-${HOME}/knowledge-bases}"
QUESTION="${1:-Begin the morning by saying what to thyself?}"

if [ -z "${WORKER_API_KEY:-}" ] && [ -z "${MOONSHOT_API_KEY:-}" ]; then
  echo "Set WORKER_API_KEY (or MOONSHOT_API_KEY) before running this script."
  echo "See the README quickstart section."
  exit 1
fi

mkdir -p "${KB_ROOT}"
for corpus in meditations physics; do
  if [ ! -d "${KB_ROOT}/${corpus}" ]; then
    echo "Copying sample corpus '${corpus}' into ${KB_ROOT}/${corpus}/"
    cp -r "${REPO_ROOT}/examples/sample-books/${corpus}" "${KB_ROOT}/${corpus}"
  fi
done

echo ""
echo "=== Asking the agent over the 'meditations' sample corpus ==="
echo "Q: ${QUESTION}"
echo ""

# Prefer the ask-expert installed by ./setup.sh (uses the project venv).
# Fall back to running the in-repo script with the project venv directly.
INSTALLED="${HOME}/.local/bin/ask-expert"
VENV_PY="${HOME}/.local/share/agentic-rag/venv/bin/python3"

if [ -x "${INSTALLED}" ]; then
  exec env KB_ROOT="${KB_ROOT}" \
    "${INSTALLED}" --domain meditations -q "${QUESTION}"
elif [ -x "${VENV_PY}" ]; then
  exec env KB_ROOT="${KB_ROOT}" \
    "${VENV_PY}" "${REPO_ROOT}/ask-expert" --domain meditations -q "${QUESTION}"
else
  echo "Neither ${INSTALLED} nor ${VENV_PY} is available."
  echo "Run ./setup.sh first."
  exit 1
fi
