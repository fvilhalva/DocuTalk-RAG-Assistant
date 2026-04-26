#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

LLM_MODEL="${OLLAMA_LLM_MODEL:-deepseek-r1:8b}"
EMBED_MODEL="${OLLAMA_EMBEDDING_MODEL:-nomic-embed-text}"

docker compose up -d ollama

for _ in $(seq 1 60); do
	if docker compose exec -T ollama ollama list >/dev/null 2>&1; then
		break
	fi
	sleep 1
done

docker compose exec -T ollama ollama pull "$EMBED_MODEL"
docker compose exec -T ollama ollama pull "$LLM_MODEL"
docker compose up -d --build app

echo "DocuTalk stack is up."
echo "Open: http://localhost:8501"
