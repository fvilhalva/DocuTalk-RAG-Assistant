from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str
    llm_model: str
    embedding_model: str
    data_dir: Path
    chunk_size: int
    chunk_overlap: int
    top_k: int
    log_file_name: str

    @property
    def raw_docs_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def index_dir(self) -> Path:
        return self.data_dir / "index"

    @property
    def logs_dir(self) -> Path:
        return self.data_dir / "logs"

    @property
    def log_file(self) -> Path:
        return self.logs_dir / self.log_file_name

    def ensure_directories(self) -> None:
        for directory in (self.raw_docs_dir, self.index_dir, self.logs_dir):
            directory.mkdir(parents=True, exist_ok=True)


def load_settings() -> Settings:
    return Settings(
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        llm_model=os.getenv("OLLAMA_LLM_MODEL", "deepseek-r1:8b"),
        embedding_model=os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"),
        data_dir=Path(os.getenv("DOCUTALK_DATA_DIR", "data")),
        chunk_size=int(os.getenv("DOCUTALK_CHUNK_SIZE", "1200")),
        chunk_overlap=int(os.getenv("DOCUTALK_CHUNK_OVERLAP", "120")),
        top_k=int(os.getenv("DOCUTALK_TOP_K", "4")),
        log_file_name=os.getenv("DOCUTALK_LOG_FILE", "interactions.csv"),
    )
