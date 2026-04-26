from __future__ import annotations

import time

import streamlit as st
from langchain_core.documents import Document

from docutalk.config import Settings, load_settings
from docutalk.rag import append_interaction_log, answer_question, get_or_create_index


def _format_source(doc: Document) -> str:
    source = str(doc.metadata.get("source", "unknown"))
    page = doc.metadata.get("page")
    if page is None:
        return source
    if isinstance(page, int):
        return f"{source} (page {page + 1})"
    return f"{source} (page {page})"


st.set_page_config(page_title="DocuTalk", page_icon=":books:", layout="wide")

SETTINGS: Settings = load_settings()
SETTINGS.ensure_directories()

if "rebuild_token" not in st.session_state:
    st.session_state.rebuild_token = 0


@st.cache_resource(show_spinner=False)
def load_vector_store(rebuild_token: int):
    rebuild = rebuild_token > 0
    return get_or_create_index(SETTINGS, rebuild=rebuild)


st.title("DocuTalk - Local-First RAG Assistant")
st.caption("Technical PDF Q&A using Ollama embeddings + FAISS retrieval.")

pdf_count = len(list(SETTINGS.raw_docs_dir.glob("*.pdf")))

with st.sidebar:
    st.subheader("Runtime")
    st.write(f"LLM model: {SETTINGS.llm_model}")
    st.write(f"Embedding model: {SETTINGS.embedding_model}")
    st.write(f"Ollama URL: {SETTINGS.ollama_base_url}")
    st.write(f"PDF directory: {SETTINGS.raw_docs_dir}")
    st.write(f"PDF files found: {pdf_count}")

    if st.button("Rebuild vector index", use_container_width=True):
        st.session_state.rebuild_token += 1
        load_vector_store.clear()
        st.success("Index rebuild will run on next question.")

if pdf_count == 0:
    st.warning(
        f"No PDFs found in {SETTINGS.raw_docs_dir}. Add files first, then ask questions."
    )

question = st.text_area(
    "Question",
    placeholder="Ex: Quais sao os requisitos de instalacao para o modulo X?",
    height=120,
)

if st.button("Ask DocuTalk", type="primary"):
    if not question.strip():
        st.error("Please provide a non-empty question.")
    else:
        try:
            with st.spinner("Running retrieval and generation..."):
                started = time.perf_counter()
                vector_store, index_built_now, chunk_count = load_vector_store(
                    st.session_state.rebuild_token
                )
                answer, sources = answer_question(SETTINGS, vector_store, question.strip())
                latency = time.perf_counter() - started

            append_interaction_log(
                settings=SETTINGS,
                question=question.strip(),
                answer=answer,
                latency_seconds=latency,
                sources=sources,
            )

            st.subheader("Answer")
            st.write(answer)

            c1, c2, c3 = st.columns(3)
            c1.metric("Latency (s)", f"{latency:.2f}")
            c2.metric("Sources", str(len(sources)))
            c3.metric("Chunks indexed", str(chunk_count if index_built_now else "cached"))

            if sources:
                st.subheader("Retrieved Sources")
                for source_line in [_format_source(doc) for doc in sources]:
                    st.write(f"- {source_line}")
        except FileNotFoundError as exc:
            st.error(str(exc))
        except Exception as exc:  # pragma: no cover - defensive for runtime issues
            st.error(f"Runtime error: {exc}")
