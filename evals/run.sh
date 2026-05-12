#!/usr/bin/env bash
# Convenience wrapper for the eval harness.
# Uses the kimi-tools venv (where rank_bm25, anthropic, openai live)
# and points at the project's knowledge bases.
#
# Usage:
#   ./evals/run.sh --label v1-bm25-default
#   ./evals/run.sh --label smoke --limit 3
#   ./evals/run.sh --label v2-prompt-fix --force --types ambiguous

set -euo pipefail

VPY="${VPY:-/home/kunal/.local/share/kimi-tools/venv/bin/python3}"
KB_ROOT_DEFAULT="/home/kunal/Downloads/mc08&mc07_code/memory/knowledge-bases"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

exec env \
  PYTHONPATH=evals \
  "$VPY" -m eval_harness \
  --kb-root "${KB_ROOT:-$KB_ROOT_DEFAULT}" \
  "$@"
