import os
import re
from typing import Any, Dict, List, Optional

from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage

from src.quantlib_rag.rag.qdrant_index import QuantLibQdrantIndex
from src.quantlib_rag.rag.llm_groq import create_groq_llm
from src.quantlib_rag.config import DEFAULT_K


class QuantLibCloudAssistant:
    """
    Cloudowy asystent:
    - Retriever: Qdrant Cloud + Gemini embeddings
    - LLM: Groq (np. llama-3.1-8b-instant)
    - Tryb: quote-only / RAG (możesz rozbudować)
    """

    def __init__(
        self,
        groq_model: str = "llama-3.1-8b-instant",
        temperature: float = 0.0,
        k_default: int = DEFAULT_K,
    ) -> None:
        self.index = QuantLibQdrantIndex(k_default=k_default)
        self.retriever = self.index.get_retriever()
        self.k_default = k_default

        self.llm_en = create_groq_llm(
            model=groq_model,
            temperature=temperature,
        )

    # ---------- INTERNAL UTILS ----------

    @staticmethod
    def _format_context(docs: List[Document], max_chars_per_doc: int = 800) -> str:
        """Składa context z kilku chunków, każdy przycięty osobno."""
        snippets = [d.page_content[:max_chars_per_doc] for d in docs]
        return "\n\n--- DOC SPLIT ---\n\n".join(snippets)

    # ---------- GŁÓWNA METODA: QUOTE-ONLY ----------

    def quote_only_answer(
        self,
        question_en: str,
        k: Optional[int] = None,
        max_chars_per_doc: int = 800,
    ) -> Dict[str, Any]:
        """
        Tryb: LLM jako 'inteligentny filtr':
        - MA PRAWO TYLKO CYTOWAĆ / LEKKO PRZEPISAĆ fragmenty kontekstu
        - NIE WOLNO mu dodawać nowych API
        """
        if k is None:
            k = self.k_default

        # ważne: retriever zależny od k (spójne z evaluatorem)
        retriever = self.index.get_retriever(k=k)
        docs = retriever.invoke(question_en)

        if not docs:
            return {
                "question_en": question_en,
                "answer_en": "I couldn't find any relevant context in the documentation.",
                "sources": [],
            }

        context = self._format_context(docs, max_chars_per_doc=max_chars_per_doc)

        messages = [
            SystemMessage(
                content=(
                    "You are assisting with internal QuantLib-Python documentation.\n"
                    "You MUST use ONLY classes, methods and functions that appear in the provided context.\n"
                    "Always use the following import style in code examples:\n"
                    "import QuantLib as ql\n"
                    "Never use 'from quantlib...' or 'import quantlib'.\n"
                    "Do NOT invent new method or class names.\n"
                    "If the context does not clearly show a working code example, reply:\n"
                    "'I don't know based on the provided documentation.'\n"
                    "When you show code, it must be valid QuantLib-Python and must only use APIs visible in the context."
                )
            ),
            HumanMessage(
                content=(
                    f"Question:\n{question_en}\n\n"
                    f"Context (multiple document chunks):\n{context}\n\n"
                    "Answer the question ONLY by copying or lightly reformatting relevant parts "
                    "from the context above. Do not invent new APIs."
                )
            ),
        ]

        resp = self.llm_en.invoke(messages)
        answer = resp.content.strip()

        sources = [
            {
                "source": os.path.basename(d.metadata.get("source", "")),
                "preview": d.page_content[:300],
            }
            for d in docs[:k]
        ]

        return {
            "question_en": question_en,
            "answer_en": answer,
            "sources": sources,
        }

    # ---------- DEBUG / EVAL: ANSWER VS CONTEXT ----------

    def analyze_answer_vs_context(
        self,
        question_en: str,
        answer: str,
        k: Optional[int] = None,
        max_chars_per_doc: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Analizuje:
        - jaki % słów z odpowiedzi występuje w kontekście (overlap)
        - jakie symbole ql.* pojawiają się w odpowiedzi
        - które z nich są też w kontekście (API z dokumentacji),
          a które tylko w odpowiedzi (potencjalna halucynacja).
        """
        if k is None:
            k = self.k_default

        retriever = self.index.get_retriever(k=k)
        docs = retriever.invoke(question_en)
        docs = docs[:k]

        if max_chars_per_doc is None:
            parts = [d.page_content for d in docs]
        else:
            parts = [d.page_content[:max_chars_per_doc] for d in docs]

        context_text = "\n\n--- DOC SPLIT ---\n\n".join(parts)

        answer_tokens = set(re.findall(r"\w+", answer.lower()))
        context_tokens = set(re.findall(r"\w+", context_text.lower()))

        if answer_tokens:
            overlap = len(answer_tokens & context_tokens) / len(answer_tokens) * 100
        else:
            overlap = 0.0

        api_in_answer = set(re.findall(r"ql\.\w+", answer))
        api_in_context = set(re.findall(r"ql\.\w+", context_text))

        api_only_in_answer = api_in_answer - api_in_context
        api_in_both = api_in_answer & api_in_context

        return {
            "question": question_en,
            "answer": answer,
            "overlap_percent": overlap,
            "api_in_answer": api_in_answer,
            "api_in_context": api_in_context,
            "api_only_in_answer": api_only_in_answer,
            "api_in_both": api_in_both,
            "docs": docs,
            "context_text": context_text,
        }
