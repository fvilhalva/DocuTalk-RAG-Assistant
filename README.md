# DocuTalk: RAG-Based Technical Document Assistant

## 🚀 Overview
DocuTalk is an intelligent conversational agent designed to interact with technical documentation (PDFs). It leverages **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers based on uploaded documents.

Unlike standard LLM interactions, this project focuses on reducing hallucinations by grounding the model's responses in specific external data sources.

## 🛠️ Tech Stack
* **Core:** Python 3.10+
* **LLM Orchestration:** LangChain
* **Interface:** Streamlit
* **Vector Store:** FAISS (Facebook AI Similarity Search) - *Chosen for efficient dense vector clustering.*
* **Embeddings:** OpenAI Embeddings / HuggingFace
* **Data Analysis:** Pandas (for conversation logging and performance metrics)

## 🧮 Mathematical Concept
The retrieval system is based on **Cosine Similarity** between high-dimensional vectors. Given a query vector $A$ and a document vector $B$, relevance is calculated as:

$$\text{similarity} = \cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$$

## 🔮 Future Improvements (GraphRAG)
Currently, the retrieval is based on vector similarity chunks. The next roadmap step is to implement a **Knowledge Graph** approach (using Neo4j or NetworkX) to map relationships between entities in the document, allowing for multi-hop reasoning – leveraging my background in **Graph Theory**.

## 📊 Analytics
The application logs user interactions to a CSV file to monitor:
* Response latency.
* Token usage.
* User feedback loops.
