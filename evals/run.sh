#!/usr/bin/env bash
# Convenience wrapper for the eval harness.
# Picks up the venv installed by ./setup.sh and points at the KB_ROOT
# env var (or $HOME/knowledge-bases as a fallback).
#
# Usage:
#   ./evals/run.sh --label v1-bm25-default
#   ./evals/run.sh --label smoke --limit 3
#   ./evals/run.sh --label v2-prompt-fix --force --types ambiguous
#
# Overrides:
#   VPY=/path/to/python3 ./evals/run.sh ...   # custom interpreter
#   KB_ROOT=/path/to/kbs ./evals/run.sh ...   # custom knowledge-base root

set -euo pipefail

DEFAULT_VENV_PY="${HOME}/.local/share/agentic-rag/venv/bin/python3"
if [ -x "${DEFAULT_VENV_PY}" ]; then
  VPY="${VPY:-${DEFAULT_VENV_PY}}"
else
  VPY="${VPY:-python3}"
fi
KB_ROOT_DEFAULT="${HOME}/knowledge-bases"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

exec env \
  PYTHONPATH=evals \
  "$VPY" -m eval_harness \
  --kb-root "${KB_ROOT:-$KB_ROOT_DEFAULT}" \
  "$@"
