from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from docutalk.config import Settings


def _embedding_client(settings: Settings) -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )


def _load_pdf_pages(raw_docs_dir: Path) -> list[Document]:
    documents: list[Document] = []
    for pdf_path in sorted(raw_docs_dir.glob("*.pdf")):
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        for page in pages:
            page.metadata.setdefault("source", pdf_path.name)
        documents.extend(pages)
    return documents


def _split_documents(
    documents: list[Document],
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


def load_index(settings: Settings) -> FAISS | None:
    index_file = settings.index_dir / "index.faiss"
    metadata_file = settings.index_dir / "index.pkl"
    if not index_file.exists() or not metadata_file.exists():
        return None

    return FAISS.load_local(
        folder_path=str(settings.index_dir),
        embeddings=_embedding_client(settings),
        allow_dangerous_deserialization=True,
    )


def build_index(settings: Settings) -> tuple[FAISS, int]:
    settings.ensure_directories()
    pages = _load_pdf_pages(settings.raw_docs_dir)
    if not pages:
        raise FileNotFoundError(
            f"No PDF files found in {settings.raw_docs_dir}. Add files before indexing."
        )

    chunks = _split_documents(
        documents=pages,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    vector_store = FAISS.from_documents(chunks, _embedding_client(settings))
    vector_store.save_local(str(settings.index_dir))
    return vector_store, len(chunks)


def get_or_create_index(settings: Settings, rebuild: bool = False) -> tuple[FAISS, bool, int]:
    if rebuild:
        vector_store, chunk_count = build_index(settings)
        return vector_store, True, chunk_count

    loaded = load_index(settings)
    if loaded is not None:
        return loaded, False, 0

    vector_store, chunk_count = build_index(settings)
    return vector_store, True, chunk_count


def answer_question(
    settings: Settings,
    vector_store: FAISS,
    question: str,
) -> tuple[str, list[Document]]:
    retriever = vector_store.as_retriever(search_kwargs={"k": settings.top_k})
    try:
        documents = retriever.invoke(question)
    except AttributeError:
        documents = retriever.get_relevant_documents(question)

    context = "\n\n".join(doc.page_content for doc in documents)
    if not context:
        return "No relevant context was retrieved for this question.", []

    prompt = (
        "You are DocuTalk, a grounded assistant for technical PDFs. "
        "Use only the provided context. If context is insufficient, state that clearly.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        "Answer in Portuguese with concise technical language."
    )

    llm = ChatOllama(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )
    response = llm.invoke(prompt)
    answer = response.content if hasattr(response, "content") else str(response)
    return answer, documents


def append_interaction_log(
    settings: Settings,
    question: str,
    answer: str,
    latency_seconds: float,
    sources: list[Document],
) -> None:
    settings.ensure_directories()

    source_names = []
    for doc in sources:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        if page is None:
            source_names.append(str(source))
        elif isinstance(page, int):
            source_names.append(f"{source}:page-{page + 1}")
        else:
            source_names.append(f"{source}:page-{page}")

    row = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "answer": answer,
        "latency_seconds": round(latency_seconds, 4),
        "source_count": len(sources),
        "sources": " | ".join(source_names),
    }

    if settings.log_file.exists():
        current = pd.read_csv(settings.log_file)
        updated = pd.concat([current, pd.DataFrame([row])], ignore_index=True)
    else:
        updated = pd.DataFrame([row])

    updated.to_csv(settings.log_file, index=False)
