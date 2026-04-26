#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -x .venv/bin/streamlit ]]; then
  echo "Virtual environment not ready. Run ./scripts/bootstrap-local.sh first."
  exit 1
fi

PORT="${DOCUTALK_PORT:-8501}"
PYTHONPATH=src \
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
  .venv/bin/streamlit run src/docutalk/app.py \
  --server.port "$PORT" \
  --server.headless true \
  --browser.gatherUsageStats false \
  "$@"
