# QuantLib RAG Assistant (Internal Documentation Search)

This project implements a **Retrieval-Augmented Generation (RAG)** system over  
the official **QuantLib-Python documentation**, downloaded and processed locally.

It is designed as a **portfolio-ready example of building an enterprise-style RAG**:
- local documentation → markdown
- text chunking with markdown-aware splitter
- embeddings with **BAAI/bge-m3**
- vector database using **ChromaDB**
- **local LLM (Mistral via Ollama)** used only as a *document-bound reasoning engine*
- Streamlit frontend with two modes:
  - **Search only (retriever)**
  - **Docs-based answer (LLM constrained to documentation)**

The model is **not allowed to use outside knowledge**.  
All answers must come from retrieved QuantLib documentation.

---

## 🏗 Project Structure

```
quantlib-rag-engine/
│
├── src/
│   └── quantlib_rag/
│       ├── ingestion/
│       │   ├── download_quantlib_docs.py
│       │   └── build_index.py
│       ├── rag/
│       │   ├── quantlib_index.py
│       │   ├── quantlib_quote_assistant.py
│       │   └── ui_streamlit.py
│       └── config.py
│
├── data/
│   └── processed/
│       └── quantlib_md/     ← generated automatically
│
├── db/
│   └── quantlib_chroma_bge_md/   ← generated automatically
│
├── main.py      ← unified runner (download → index → UI)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Ollama (for local LLM)
https://ollama.ai/install

### 3. Pull the Mistral model
```bash
ollama pull mistral
```

### 4. Run the automatic bootstrap (docs → index → UI)

```bash
python main.py
```

This will:

1. Download documentation from ReadTheDocs  
2. Convert it to `.md` files  
3. Build Chroma vector index (`db/quantlib_chroma_bge_md/`)  
4. Launch the Streamlit UI at  

```
http://localhost:8501
```

---

## 🧠 System Overview

### Retrieval
- markdown chunking via `MarkdownHeaderTextSplitter`
- embeddings: **BAAI/bge-m3**
- vector DB: **ChromaDB** (persistent)

### Reasoning
- local LLM via **Ollama**
- constrained mode:
  - LLM may **only use retrieved documentation**
  - zero external knowledge
  - ideal for *internal-company documentation RAGs*

---

## 🖥 UI Modes

### 1. 🔎 Search only (retriever)
Shows raw documentation chunks retrieved by vector search.

### 2. 🧾 Docs-based answer (LLM)
LLM receives:
- user question
- retrieved chunks
- strict system instructions:
  - *answer only using provided context*
  - *do not invent API*
  - *never use outside knowledge*

---

## 🧪 Testing the RAG

Example queries:

- “Give a QuantLib-Python example of building a flat yield curve using `FlatForward`.”
- “How to compute year fraction using Actual/360?”
- “What are day count conventions supported by QuantLib-Python?”
- “Show the parameters of `Schedule` constructor.”

---

## 📦 Deployment Notes

This project is standalone:
- no external APIs needed
- works offline once downloaded the first time
- ideal for demonstrating RAG engineering skills

---

## 🙌 Credits

Built as a personal research project to demonstrate practical RAG system design  
for internal enterprise documentation.

```
Author: mb90dev
```
