#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -x .venv/bin/python ]]; then
  echo "Virtual environment not ready. Run ./scripts/bootstrap-local.sh first."
  exit 1
fi

PYTHONPATH=src .venv/bin/python -m docutalk.cli --rebuild
