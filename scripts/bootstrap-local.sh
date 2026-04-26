#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d .venv ]]; then
  python -m venv .venv
fi

.venv/bin/pip install -r requirements.txt

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

echo "Local environment ready."
echo "Run Ollama separately, then:"
echo "PYTHONPATH=src .venv/bin/streamlit run src/docutalk/app.py"
