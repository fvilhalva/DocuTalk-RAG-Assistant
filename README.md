# DocuTalk: Local-First RAG Assistant for Technical PDFs

DocuTalk is a small, modular RAG project designed for local execution.
It uses Ollama for generation/embeddings, FAISS for retrieval, and Streamlit for UI.
The structure below is optimized for a non-enterprise codebase that still needs clean boundaries.

## Project Structure

```text
DocuTalk-RAG-Assistant/
├── .github/
│   └── agents/
├── data/
│   ├── raw/            # Put your PDF files here
│   ├── index/          # Persisted FAISS index (generated)
│   └── logs/           # CSV interaction logs (generated)
├── src/
│   └── docutalk/
│       ├── app.py      # Streamlit interface
│       ├── cli.py      # Index utility commands
│       ├── config.py   # Environment-based settings
│       └── rag.py      # Ingestion, indexing, retrieval, generation, logging
├── .env.example
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Architecture (Small Scope)

- Local-first by default: no paid/cloud API required.
- Grounded answers: response uses retrieved PDF chunks from FAISS.
- Minimal moving parts: one app service and one Ollama service.
- Safe evolution path: you can later split ingestion/retrieval into separate modules without refactor chaos.

## Requirements

- Python 3.11+
- Docker + Docker Compose (recommended)
- Ollama model availability (`deepseek-r1:8b` and `nomic-embed-text` by default)

## Local Run (Without Docker App)

1. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create environment file:

```bash
cp .env.example .env
```

3. Start Ollama and pull models (one time):

```bash
ollama serve
ollama pull nomic-embed-text
ollama pull deepseek-r1:8b
```

4. Add PDFs to `data/raw` and run Streamlit:

```bash
./scripts/run-local.sh
```

Quick bootstrap option:

```bash
./scripts/bootstrap-local.sh
```

## Docker Compose Run (Recommended)

1. Start Ollama service:

```bash
docker compose up -d ollama
```

2. Pull required models inside Ollama container:

```bash
docker compose exec ollama ollama pull nomic-embed-text
docker compose exec ollama ollama pull deepseek-r1:8b
```

3. Build and run app:

```bash
docker compose up --build app
```

4. Open UI:

```text
http://localhost:8501
```

Quick bootstrap option:

```bash
./scripts/bootstrap-docker.sh
```

## CLI Utility

Build or rebuild index from terminal:

```bash
./scripts/rebuild-index.sh
```

## Data and Logs

- Put PDFs in `data/raw`.
- FAISS files are generated in `data/index`.
- Interaction analytics are recorded in `data/logs/interactions.csv`.

## Design Notes

- Retrieval relevance follows cosine similarity behavior in normalized embedding space.
- The current implementation prioritizes clarity and maintainability over complex orchestration.
- Future GraphRAG expansion can be added on top of this template without changing app entrypoint contracts.
