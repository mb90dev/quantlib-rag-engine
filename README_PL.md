QuantLib RAG Assistant — Wyszukiwanie i Asystent oparty o dokumentację QuantLib-Python

Ten projekt to kompletny, produkcyjny przykład budowy RAG (Retrieval-Augmented Generation) nad wewnętrzną dokumentacją QuantLib-Python.

Projekt pokazuje:

pełny pipeline RAG (od .md → embeddingi → retriever → LLM),

lokalny i chmurowy backend (Mistral/Ollama oraz Groq/Llama 3.1),

dokładne zabezpieczenia przed halucynacjami,

cache dokładny (JSON) i cache semantyczny,

ewaluację jakości RAG,

warstwę Guarded RAG z LangGraph — identyczną jak w rozwiązaniach enterprise,

frontend w Streamlit z trybem chmurowym i lokalnym.

Model nie może korzystać z wiedzy spoza dokumentacji — to projekt stricte dokumentacyjny.

🧱 Kluczowe komponenty
1. Przetwarzanie dokumentacji

Źródło: dokumentacja QuantLib-Python zamieniona na markdown.

Używany jest markdown-aware splitter:

fragmenty są spójne semantycznie,

każdy chunk ma metadane: source, sekcje, nagłówki, pozycję w pliku.

2. Embeddingi
Tryb lokalny

Model: BAAI/bge-m3

Backend: HuggingFace

Normalizacja embeddingów + query instruction

Tryb chmurowy

Embeddingi generowane przez Gemini

Zapisywane do Qdrant Cloud

3. Vector store / retriever

Lokalnie: ChromaDB

W chmurze: Qdrant Cloud

W obu przypadkach pipeline używa klasy QuantLibIndex lub QuantLibQdrantIndex.

4. LLM-y

Lokalnie: Mistral przez Ollama

W chmurze: Llama 3.1 przez Groq

Oba tryby korzystają z asystentów:

QuantLibAssistant (lokalny)

QuantLibCloudAssistant (chmurowy)

Wspólne dla obu:

model pracuje wyłącznie na podstawie dokumentacji,

prompt zabrania halucynowania API,

zawsze używa import QuantLib as ql.

📐 Architektura lokalna i chmurowa
Lokalny RAG (offline)
Markdown → Chunking → Chroma(BGE) → Retriever → Mistral(Ollama) → Odpowiedź oparta o dokumentację

Chmurowy RAG (Groq + Qdrant)
Markdown → Gemini embeddings → Qdrant Cloud → Retriever → Llama 3.1 (Groq) → Odpowiedź

🧪 Ewaluacja (Retrieval + LLM)

Projekt zawiera evaluator QuantLibRAGEvaluator, który mierzy:

🔹 1. Retrieval

hit@k — czy poprawny dokument znalazł się w top-k

porównanie Chroma vs Qdrant

🔹 2. Hallucination detection

procent wspólnych tokenów odpowiedzi i kontekstu (overlap_percent)

analiza ql.*:

które API pojawia się w odpowiedzi,

które pojawia się w dokumentacji.

🔹 3. LLM-as-judge (Groq)

faithfulness: 1–5

helpfulness: 1–5

notatka opisowa

Sędzia dostaje:

pytanie,

kontekst (retrieved docs),

odpowiedź asystenta.

🔹 4. Metryki czasu

czas retrievalu,

czas generacji odpowiedzi.

💾 Cache lokalnego LLM
Exact cache (JSON)

klucz: (normalized_question, k, mode)

wartość: pełna odpowiedź z metadanymi.

Semantic cache

embeddingi BGE-M3,

Chroma z oddzielną kolekcją,

próg podobieństwa (domyślnie 0.75),

zwraca odpowiedź Mistrala bez jego wywoływania.

Daje to ogromne przyspieszenie UI.

🚀 Streamlit UI

Interfejs pozwala:

wyszukiwać fragmenty dokumentacji (Search only),

generować odpowiedzi oparte wyłącznie o dokumentację,

przeglądać źródła .md,

działa zarówno lokalnie, jak i w chmurze,

posiada tryb Guarded mode (patrz kolejna sekcja).

🛡️ Guarded RAG z LangGraph (LLM-as-Judge)

To najbardziej „enterprise-ready” część projektu.
Guarded RAG został dodany, aby:

chronić system przed halucynacjami,

wycinać pytania spoza dokumentacji,

wymuszać pełną zgodność odpowiedzi z dokumentacją QuantLib,

zapewnić kontrolowalny, deterministyczny przepływ.

Guarded RAG działa jako dodatkowa warstwa nad standardowym pipeline RAG.

🔧 Jak to działa?

Guarded pipeline składa się z trzech kroków:

1. generate_answer

Wywołuje QuantLibQuoteAssistant:

cache 1:1,

semantic cache,

retriever → kontekst,

wygenerowana odpowiedź answer_en.

2. retrieve_context

Oddzielny retriever pobiera pełne dokumenty jako Document,
– te dokumenty są przekazywane do modelu-sędziego.

3. verify_answer (Groq LLM-as-judge)

Niezależny model Groq ocenia:

{
  "is_grounded": true | false,
  "out_of_scope": true | false,
  "faithfulness_score": 1–5,
  "reason": "..."
}


JSON jest parsowany, a wynik trafia do routera LangGraph.

Finalizacja:

Jeśli odpowiedź jest poprawna → zostaje.

Jeśli nie jest:

odpowiedź zostaje zastąpiona:

"I don't know based on the provided documentation.", lub

rozszerzoną wersją z informacją o out-of-scope.

🔁 LangGraph — przepływ Guarded RAG
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
(zachowaj odpowiedź)         (podmień na "I don't know…")

🖥️ Streamlit — Guarded Cloud Mode

W trybie chmurowym UI posiada:

☑️ Guarded mode (LLM-as-judge, no hallucinations, out-of-scope detection)


Po włączeniu:

odpowiedź jest generowana przez Groq,

następnie przechodzi przez warstwę LangGraph + judge,

UI pokazuje:

odpowiedź,

źródła,

strukturę JSON od sędziego.

Przykład (screen):

Answer:
import QuantLib as ql
...

Sources:
- termstructures.md
- basics.md
...

Verification:
{
  "is_grounded": true,
  "out_of_scope": false,
  "faithfulness_score": 5,
  "reason": "The answer accurately explains how to build a flat yield curve using FlatForward in QuantLib."
}

📦 Struktura projektu
quantlib-rag-engine/
├── src/
│   └── quantlib_rag/
│       ├── rag/
│       │   ├── quantlib_assistant.py
│       │   ├── quantlib_cloud_assistant.py
│       │   ├── quantlib_index.py
│       │   ├── qdrant_index.py
│       │   ├── quantlib_rag_evaluator.py
│       │   ├── judge.py
│       │   └── ...
│       ├── graph/
│       │   ├── state.py
│       │   ├── guarded_rag.py
│       │   └── ...
│       ├── config.py
│       └── ...
├── db/
│   ├── quantlib_chroma_bge_md_v2/
│   └── cache/local_mistral_cache.json
├── data/
├── scripts/
│   ├── run_rag_eval.py
│   └── run_guarded_rag_demo.py
└── README.md
✍️ Autor
mb90dev — 2025