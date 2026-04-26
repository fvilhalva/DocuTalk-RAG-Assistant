# DocuTalk: Local-First RAG Assistant for Technical PDFs

DocuTalk is a lean, local-first RAG template for technical PDF question answering.
It uses Ollama for generation and embeddings, FAISS for retrieval, and Streamlit for the UI.

## What Changed Recently

- Added NVIDIA GPU-safe Docker mode with conservative defaults.
- Added `docker-compose.gpu-safe.yml` override for Ollama GPU runtime.
- Added `scripts/bootstrap-docker-gpu-safe.sh` for one-command GPU startup.
- Standardized bootstrap scripts for local and Docker flows.
- Updated git hygiene: `data/` and `.github/` are ignored to avoid pushing runtime/private local files.

## Project Structure

```text
DocuTalk-RAG-Assistant/
├── data/                          # Runtime data (git-ignored)
│   ├── raw/                       # Input PDFs
│   ├── index/                     # Persisted FAISS index (generated)
│   └── logs/                      # Interaction CSV logs (generated)
├── scripts/
│   ├── bootstrap-local.sh
│   ├── run-local.sh
│   ├── rebuild-index.sh
│   ├── bootstrap-docker.sh
│   └── bootstrap-docker-gpu-safe.sh
├── src/
│   └── docutalk/
│       ├── app.py                 # Streamlit interface
│       ├── cli.py                 # Index utility command
│       ├── config.py              # Environment-based settings
│       └── rag.py                 # Ingestion, indexing, retrieval, generation, logging
├── .env.example
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── docker-compose.gpu-safe.yml
├── Dockerfile
└── requirements.txt
```

## Architecture (Small Scope)

- Local-first by default: no paid/cloud API required.
- Grounded answers: responses are generated from retrieved PDF chunks.
- Minimal moving parts: one app service and one Ollama service.
- Clear extension path: retrieval/generation modules can evolve without changing the app entrypoint.

## Requirements

- Python 3.11+ (for local mode)
- Docker + Docker Compose (recommended)
- Ollama models (defaults): `deepseek-r1:8b` and `nomic-embed-text`

## Quick Start (Recommended: Docker GPU-Safe)

1. Create `.env` from template:

```bash
cp .env.example .env
```

2. Put PDFs into `data/raw`.

3. Start full stack in GPU-safe mode:

```bash
./scripts/bootstrap-docker-gpu-safe.sh
```

4. Open UI:

```text
http://localhost:8501
```

Notes:

- First run downloads Ollama image and models, which can take time and disk space.
- The script waits for Ollama readiness, pulls embedding and LLM models, then starts the app.

## Other Run Modes

### Docker (Default/CPU-Friendly)

One command:

```bash
./scripts/bootstrap-docker.sh
```

Or manual steps:

```bash
docker compose up -d ollama
docker compose exec -T ollama ollama pull nomic-embed-text
docker compose exec -T ollama ollama pull deepseek-r1:8b
docker compose up -d --build app
```

### Local Host Mode (Without Docker App)

One command bootstrap:

```bash
./scripts/bootstrap-local.sh
```

Then start app:

```bash
./scripts/run-local.sh
```

If you are not using Docker Ollama, run host Ollama once and pull models:

```bash
ollama serve
ollama pull nomic-embed-text
ollama pull deepseek-r1:8b
```

## GPU-Safe Profile Defaults

The GPU-safe mode uses `docker-compose.gpu-safe.yml` and these defaults:

- `OLLAMA_NUM_PARALLEL=2`
- `OLLAMA_MAX_LOADED_MODELS=1`
- `OLLAMA_MAX_QUEUE=32`
- `OLLAMA_KEEP_ALIVE=20m`
- `NVIDIA_VISIBLE_DEVICES=all`
- `NVIDIA_DRIVER_CAPABILITIES=compute,utility`

Override any of them in `.env` when tuning throughput.

## Rebuild Vector Index

Run from terminal:

```bash
./scripts/rebuild-index.sh
```

If no PDFs are found in `data/raw`, rebuild fails with a clear error message.

## Configuration

Core runtime variables live in `.env`:

- `OLLAMA_BASE_URL`
- `OLLAMA_LLM_MODEL`
- `OLLAMA_EMBEDDING_MODEL`
- `DOCUTALK_DATA_DIR`
- `DOCUTALK_CHUNK_SIZE`
- `DOCUTALK_CHUNK_OVERLAP`
- `DOCUTALK_TOP_K`
- `DOCUTALK_LOG_FILE`

GPU-safe tuning variables:

- `NVIDIA_VISIBLE_DEVICES`
- `NVIDIA_DRIVER_CAPABILITIES`
- `OLLAMA_NUM_PARALLEL`
- `OLLAMA_MAX_LOADED_MODELS`
- `OLLAMA_MAX_QUEUE`
- `OLLAMA_KEEP_ALIVE`

## Logs, Data, and Monitoring

- PDFs: `data/raw`
- FAISS index: `data/index`
- Interaction logs: `data/logs/interactions.csv`

Useful commands:

```bash
docker compose logs -f app
docker compose logs -f ollama
```

For GPU-safe stack logs:

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu-safe.yml logs -f app
docker compose -f docker-compose.yml -f docker-compose.gpu-safe.yml logs -f ollama
```

## Stop Commands

Default stack:

```bash
docker compose stop
docker compose down
```

GPU-safe stack:

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu-safe.yml stop
docker compose -f docker-compose.yml -f docker-compose.gpu-safe.yml down
```

## Git Tracking Behavior

This repository currently ignores these paths:

- `data/`
- `.github/`

That prevents runtime artifacts and local agent files from being pushed.

If these paths were previously tracked, remove them from the Git index (without deleting local files):

```bash
git rm -r --cached data .github
```

## Design Notes

- Retrieval quality comes from chunking + embedding + top-k configuration.
- Current defaults prioritize stability and local privacy over maximum throughput.
- The codebase is intentionally small to simplify maintenance and iteration.
