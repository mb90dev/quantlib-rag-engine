# QuantLib RAG Assistant (Internal Documentation Search)

This project implements a **Retrieval-Augmented Generation (RAG)** system over  
the official **QuantLib-Python documentation**, downloaded and processed locally.

It is designed as a **portfolio-ready example of building an enterprise-style RAG**:

- local documentation → markdown
- text chunking with markdown-aware splitter
- embeddings with **BAAI/bge-m3** (local) and **Gemini embeddings** (cloud)
- vector databases: **ChromaDB** (local) and **Qdrant Cloud** (remote)
- **local LLM (Mistral via Ollama)** used only as a *document-bound reasoning engine*
- **cloud LLM (Groq / Llama 3.1)** as a fast, production-like backend
- Streamlit frontend with two modes:
  - **Search only (retriever)**
  - **Docs-based answer (LLM constrained to documentation)**

The model is **not allowed to use outside knowledge** – it must answer strictly based on the retrieved QuantLib docs.

---

## 🧱 Core Components

### 1. Documentation ingestion

- Source: official QuantLib-Python docs converted to markdown (`.md`)
- Markdown-aware splitter with headers → stable, semantically meaningful chunks
- Each chunk keeps metadata:
  - `source` (file name)
  - heading / section info
  - position in file

### 2. Embeddings

**Local mode**:

- Model: `BAAI/bge-m3`
- Backend: HuggingFace
- Enterprise settings:
  - `normalize_embeddings=True`
  - query instruction string for better retrieval quality

**Cloud mode**:

- Embeddings via **Gemini** (Google)
- Stored remotely in **Qdrant Cloud**

### 3. Vector stores / retrievers

- Local:
  - `Chroma` persisted in `db/quantlib_chroma_bge_md_v2/`
  - wrapped by `QuantLibIndex` with `as_retriever(k=...)`
- Cloud:
  - `Qdrant` (managed / cloud)
  - wrapped by `QuantLibQdrantIndex`

### 4. LLM backends

- **Local**: Mistral via **Ollama** (CPU-friendly, offline)
  - wrapped by `QuantLibAssistant` (`src/quantlib_rag/rag/quantlib_assistant.py`)
- **Cloud**: Llama 3.1 via **Groq**
  - wrapped by `QuantLibCloudAssistant` (`src/quantlib_rag/rag/quantlib_cloud_assistant.py`)

Both assistants are **quote-only RAG**:

- LLM sees only:
  - user question
  - context = few chunks from documentation
- Prompts explicitly forbid:
  - hallucinating new QuantLib APIs
  - using imports other than `import QuantLib as ql`
  - using knowledge outside the docs

---

## ☁️ Local vs Cloud: Architecture

### Local RAG (offline, CPU, Chroma)

```text
+-----------------------+         +-----------------------+
|  QuantLib Markdown    |         |   User Question       |
|  Docs (.md)           |         +-----------+-----------+
+-----------+-----------+                     |
            |                                 v
            |                         +-------+--------+
            |                         | QuantLibIndex |
            |                         | (Chroma+BGE)  |
            |                         +-------+--------+
            |                                 |
            v                                 v
+-----------------------+             +-------+--------+
| Markdown Splitter     |   chunks    | Retriever      |
| (headers-aware)       +-----------> | (top-k docs)   |
+-----------------------+             +-------+--------+
                                              |
                                              v
                                     +--------+---------+
                                     | QuantLibAssistant|
                                     | (Mistral/Ollama) |
                                     +--------+---------+
                                              |
                                              v
                                      +-------+--------+
                                      |  Answer based  |
                                      |  only on docs  |
                                      +----------------+

Cloud RAG (Groq + Qdrant + Gemini)

+-------------------+      +-------------------------+
| QuantLib Markdown |      | Qdrant Cloud            |
| Docs (.md)        +----> | (vectors from Gemini)   |
+-------------------+      +-----------+-------------+
                                        ^
                                        |
                              +---------+---------+
                              |  Cloud Retriever  |
                              | (QuantLibQdrant   |
                              |  + Gemini emb)    |
                              +---------+---------+
                                        |
+-----------------------+               v
|  Streamlit Frontend   +------> +------+---------+
|  (cloud UI)           |        | QuantLibCloud |
+-----------------------+        | Assistant     |
                                 | (Groq Llama)  |
                                 +------+--------+
                                        |
                                        v
                                 +------+--------+
                                 | Docs-based    |
                                 | Answer        |
                                 +---------------+

Local mode: ideal for offline work, experimentation and showing that you can run the full pipeline on your own machine.

Cloud mode: more production-like — fast responses, managed vector DB, external LLM.


🧪 Evaluation Framework (RAG quality)

The project includes an evaluator QuantLibRAGEvaluator (src/quantlib_rag/rag/quantlib_rag_evaluator.py) that measures:

1. Retrieval metrics

    hit@k – whether the correct document (gold_source) is present in the top-k retrieved results

    list of sources returned by the retriever

    comparison between BGE (local) and Gemini (cloud) embeddings

2. Hallucination / consistency metrics

simple overlap:

    percentage of answer tokens present in the retrieved context (overlap_percent)

analysis of ql.* symbols:

    which appear in the answer

    which exist in the context

    potential hallucinated API calls

3. LLM-as-judge (answer quality)

A separate judge model (Llama 3.1 70B on Groq) scores:

    faithfulness (1–5) – how well the answer matches the context

    helpfulness (1–5) – how well the answer addresses the question

    short textual notes (notes)

The judge receives:

    QUESTION

    CONTEXT (retrieved docs)

    ANSWER (from local/cloud assistant)

and returns a structured JSON with scores.

4. Latency metrics

For each query, the evaluator measures:

    latency_retrieval_ms – retriever time

    latency_llm_ms – LLM generation time

This allows a direct comparison between local and cloud profiles, both in terms of quality and performance.

🔁 Two-phase Evaluation for Local Mistral

Local Mistral is slower (CPU, no GPU), so evaluation is split into two phases:

Phase 1 – answers + cache population

    retriever returns top-k docs (Chroma + BGE)

    QuantLibAssistant generates an answer

    each question from the test set is run through the full RAG pipeline

    the result is written to:

        Exact JSON Cache

        Semantic Cache

    no judge calls yet (to avoid unnecessary network calls)

Phase 2 – judging cached answers (no local LLM calls)

    Mistral is not called again – answers are read from cache

    evaluator loads answers from cache

    Groq judge scores:

        faithfulness

        helpfulness

        hallucination flags

    final metrics and CSV reports are produced

This allows:

    running the heavy local LLM only once per dataset,

    then iterating on evaluation as many times as needed at low cost.

💾 Local LLM Cache (JSON)

The local QuantLibAssistant has a very simple exact 1:1 cache (SimpleAnswerCache):

key: (normalized_question, k, mode) → string of the form
mode||k=5||how do i set up the evaluation date in quantlib

value:

{
  "question_en": "...",
  "answer_en": "...",
  "sources": [...]
}

backend:

    in-memory dict

    persisted as a single JSON file

Benefits:

    repeated questions with the same k never re-run Mistral,

    Phase 2 evaluation reads from exactly the same answers,

    easier offline debugging and analysis.

Cache location is configurable in config.py
(e.g. db/cache/local_mistral_cache.json).


🧠 Semantic Cache (semantic memory for questions)

Besides the exact 1:1 cache, the project uses a Semantic Answer Cache that recognizes paraphrased questions and returns answers without re-running Mistral.

Mechanism:

    questions are embedded with BAAI/bge-m3

    written into a dedicated Chroma collection

    the full answer payload is stored in metadata["payload"]

    for a new question, the system performs:

        similarity_search_with_relevance_scores(k=1)

        if score ≥ threshold (e.g. 0.75):
        → cached answer is returned, Mistral is not called

Benefits:

    massive speed-up for the UI

    paraphrased questions (“same thing, different words”) feel instant

    100% safe because results are still doc-grounded

Recommended way to pre-fill semantic cache:

    Run full evaluate_dataset()

    Phase 1 writes all answers

    Semantic cache becomes a rich “memory” of the system

🧰 Evaluation Runner

In addition to notebooks, the project includes a simple CLI-style evaluation runner.

Example runner script (scripts/run_rag_eval.py) can:

    execute local full eval (with cache + judge),

    execute cloud full eval,

    write results to eval_results/*.csv.

Example usage:

    python scripts/run_rag_eval.py

Each result file contains e.g.:

    hit_at_k

    faithfulness

    helpfulness

    overlap_percent

    latency_retrieval_ms

    latency_llm_ms

    backend (local/cloud)

Perfect base for analysis in notebooks or BI tools.


🚀 Streamlit UI

The project ships with a Streamlit frontend that lets you:

    type a question in English,

    choose a mode (local / cloud / guarded),

    inspect:

        final answer,

        underlying documentation chunks,

        which .md files were used.

The frontend is aware that:

    the model must not use external knowledge,

    answers must be doc-grounded,

    guardrails can be enabled to enforce this property.


🛡️ Guarded RAG with LangGraph (LLM-as-Judge)

On top of the standard RAG pipeline, the project includes a guarded RAG layer built with LangGraph.
The goal is to enforce production-grade safety guarantees:

    no hallucinations,

    answers are strictly grounded in QuantLib-Python docs,

    out-of-scope detection for questions that go beyond the internal documentation,

    deterministic fallbacks:

        "I don't know based on the provided documentation."

        or extended variant when the question is out-of-scope.

1. Components

Guarded RAG is built on:

    QuantLibQuoteAssistant – existing quote-only RAG assistant:

        retrieval + prompt + local LLM,

        exact JSON cache + semantic cache,

        documentation-only guarantees.

verify_answer + Groq LLM:

    independent LLM-as-judge (Llama 3.1 on Groq),

    receives question + retrieved context + answer,

    returns a structured JSON:

    {
    "is_grounded": true/false,
    "out_of_scope": true/false,
    "faithfulness_score": 1-5,
    "reason": "..."
    }


2. Guarded RAG pipeline (LangGraph)

The guarded pipeline is implemented as GuardedQuantLibRAG (src/quantlib_rag/graph/guarded_rag.py) and orchestrated by LangGraph over a shared state:

class GuardedRAGState(TypedDict):
    question_en: str
    answer_en: Optional[str]
    sources: List[Dict[str, Any]]
    contexts: List[Document]
    verification: Optional[Dict[str, Any]]


High-level flow:

generate_answer

    calls QuantLibQuoteAssistant.quote_only_answer(...)

    reuses JSON + semantic cache

    writes answer_en and sources to the state

retrieve_context

    uses the underlying QuantLibIndex retriever

    fetches k documents for verification only

    writes full Document objects to contexts

verify_answer

    calls verify_answer(judge_llm, question, answer_en, contexts)

    strips Markdown code fences from model output

    parses JSON into verification dict

conditional routing

    if is_grounded == true and out_of_scope == false → finalize_ok

    otherwise → finalize_reject

finalize_ok / finalize_reject

    finalize_ok → answer stays as-is

    finalize_reject → answer is replaced with one of:

        "I don't know based on the provided documentation."

        "I don't know based on the provided documentation. The question also seems to go beyond the internal QuantLib-Python docs."

question_en
      ↓
[ generate_answer ]  → odpowiedź z cache lub Mistrala
      ↓
[ retrieve_context ] → dokumenty dla sędziego
      ↓
[ verify_answer ]    → JSON z: is_grounded/out_of_scope
      ↓
   ┌─────────────── yes ───────────────┐
   ↓                                    ↓
finalize_ok                    finalize_reject
(keep answer_en)         ( "safe I don't know...)

This turns a standard RAG pipeline into a guarded RAG with explicit, inspectable control flow.

3. Streamlit – Guarded Cloud Profile

The cloud Streamlit app exposes a Guarded mode toggle:

    Retriever: Qdrant Cloud (Gemini embeddings) or local Chroma

    LLM (answer): Groq – Llama 3.1

    Guardrail: LLM-as-judge via LangGraph

The UI shows:

    Answer – doc-grounded answer if it passes verification

    Sources – list of .md files used to generate the answer

    Verification (LLM-as-judge) – raw JSON from the judge model

Example view (cloud profile):

QuantLib RAG — Cloud profile

Retriever: Qdrant Cloud (Gemini embeddings)
LLM: Groq (llama-3.1-8b-instant)
Mode: quote-only on QuantLib-Python docs

[ ] Guarded mode (LLM-as-judge, no hallucinations, out-of-scope detection)

[Run]


When Guarded mode is enabled, the answer is always checked by LangGraph + judge before being shown to the user.

quantlib-rag-engine/
├── src/
│   └── quantlib_rag/
│       ├── rag/
│       │   ├── quantlib_assistant.py          # local Mistral-based RAG assistant
│       │   ├── quantlib_cloud_assistant.py    # cloud Groq+Qdrant assistant
│       │   ├── quantlib_index.py              # Chroma + BGE index
│       │   ├── qdrant_index.py                # Qdrant Cloud index
│       │   ├── quantlib_rag_evaluator.py      # evaluation (hit@k, judge, latencies)
│       │   ├── judge.py                       # LLM-as-judge helper (Groq, JSON output)
│       │   └── ...
│       ├── graph/
│       │   ├── state.py                       # GuardedRAGState definition
│       │   ├── guarded_rag.py                 # GuardedQuantLibRAG (LangGraph orchestration)
│       │   └── ...
│       ├── config.py                          # paths, constants, embedding configs
│       └── ...
├── db/
│   ├── quantlib_chroma_bge_md_v2/             # local Chroma index
│   └── cache/
│       └── local_mistral_cache.json           # JSON cache for local LLM answers
├── data/                                      # raw / processed docs (if used)
├── scripts/
│   ├── run_rag_eval.py                        # example evaluation runner
│   └── run_guarded_rag_demo.py                # example guarded RAG runner (LangGraph)
└── README.md


🎯 What this project demonstrates

a full RAG pipeline: from .md docs to a working retriever + LLM

both local and cloud backends on the same documentation

prompts that constrain the model to doc-only answers

evaluation metrics (retrieval + answer quality)

local LLM caching (exact + semantic)

two-phase evaluation with external judge

Streamlit UI for exploration

Guarded RAG with LangGraph:

    explicit control flow,

    LLM-as-judge,

    hallucination and out-of-scope protection.


🙌 Credits

Built as a personal research project to demonstrate practical RAG system design
for internal enterprise documentation (here: QuantLib-Python).

Author: mb90dev