#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "nvidia-smi not found. Install NVIDIA drivers before using GPU mode."
  exit 1
fi

LLM_MODEL="${OLLAMA_LLM_MODEL:-deepseek-r1:8b}"
EMBED_MODEL="${OLLAMA_EMBEDDING_MODEL:-nomic-embed-text}"

export OLLAMA_NUM_PARALLEL="${OLLAMA_NUM_PARALLEL:-2}"
export OLLAMA_MAX_LOADED_MODELS="${OLLAMA_MAX_LOADED_MODELS:-1}"
export OLLAMA_MAX_QUEUE="${OLLAMA_MAX_QUEUE:-32}"
export OLLAMA_KEEP_ALIVE="${OLLAMA_KEEP_ALIVE:-20m}"
export NVIDIA_VISIBLE_DEVICES="${NVIDIA_VISIBLE_DEVICES:-all}"
export NVIDIA_DRIVER_CAPABILITIES="${NVIDIA_DRIVER_CAPABILITIES:-compute,utility}"

COMPOSE_FILES=(-f docker-compose.yml -f docker-compose.gpu-safe.yml)

docker compose "${COMPOSE_FILES[@]}" up -d ollama

ready=0
for _ in $(seq 1 60); do
  if docker compose "${COMPOSE_FILES[@]}" exec -T ollama ollama list >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 1
done

if [[ "$ready" -ne 1 ]]; then
  echo "Ollama did not become ready in time."
  exit 1
fi

docker compose "${COMPOSE_FILES[@]}" exec -T ollama ollama pull "$EMBED_MODEL"
docker compose "${COMPOSE_FILES[@]}" exec -T ollama ollama pull "$LLM_MODEL"
docker compose "${COMPOSE_FILES[@]}" up -d --build app

echo "DocuTalk GPU-safe stack is up."
echo "Open: http://localhost:8501"
echo "Safety defaults -> OLLAMA_NUM_PARALLEL=$OLLAMA_NUM_PARALLEL, OLLAMA_MAX_LOADED_MODELS=$OLLAMA_MAX_LOADED_MODELS, OLLAMA_MAX_QUEUE=$OLLAMA_MAX_QUEUE, OLLAMA_KEEP_ALIVE=$OLLAMA_KEEP_ALIVE"