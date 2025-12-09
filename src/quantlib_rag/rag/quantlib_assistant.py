# src/rag/quantlib_quote_assistant.py 

import os
import re
from typing import Any, Dict, List, Optional

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.documents import Document

from .quantlib_index import QuantLibIndex
from ..config import *


class QuantLibQuoteAssistant:
    """
    Quote-only assistant dla dokumentacji QuantLib-Python.

    Używa:
    - QuantLibIndex -> retriever (Chroma + BGE)
    - ChatOllama(model="mistral", temperature=0.0)

    Metody:
    - quote_only_answer(...)          -> LLM TYLKO cytuje kontekst
    - debug_retrieval(...)            -> podgląd, co zwraca retriever
    - analyze_answer_vs_context(...)  -> ile odpowiedzi jest z docs, a ile z 'głowy'
    """

    def __init__(
        self,
        db_path: Optional[str | os.PathLike] = None,
        llm_model: str = "mistral",
        temperature: float = 0.0,
        k_default: int = DEFAULT_K,
        llm = None
    ) -> None:
        # Index + retriever
        self.index = QuantLibIndex(db_path=db_path, k_default=k_default)
        self.retriever = self.index.get_retriever()


        
        if llm is not None:
            self.llm_en = llm
        else:
            self.llm_en = ChatOllama(
                model=llm_model,
                temperature=temperature,
            )  

        self.k_default = k_default

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
        - MA PRAWO TYLKO CYTOWAĆ fragmenty kontekstu
        - NIE WOLNO mu dodawać nowego kodu ani tekstu
        """
        if k is None:
            k = self.k_default

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
                    "Do NOT invent new method or class names. If you need a day-count year fraction, "
                    "and the context only shows a FixedRateCoupon example, you may explain the idea "
                    "in words but DO NOT fabricate new API.\n"
                    "If the context does not clearly show a working code example, reply:\n"
                    "'I don't know based on the provided documentation.'\n"
                    "When you show code, it must be valid QuantLib-Python and must only use APIs visible in the context."
                )
            ),
            HumanMessage(
                content=(
                    f"Question:\n{question_en}\n\n"
                    f"Context (multiple document chunks):\n{context}\n\n"
                    "Answer the question ONLY by copying relevant parts from the context above. "
                    "Do not add any new text or code that is not already there."
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

    # ---------- DEBUG: RETRIEVER ----------

    def debug_retrieval(
        self,
        question_en: str,
        k: Optional[int] = None,
        max_chars_per_doc: Optional[int] = None,
    ) -> List[Document]:
        """
        Zwraca i drukuje chunki, które zwrócił retriever.
        Przydatne do ręcznej inspekcji.
        """
        if k is None:
            k = self.k_default

        retriever = self.index.get_retriever(k=k)
        docs = retriever.invoke(question_en)

        print(f"\n[QUESTION]\n{question_en}\n")
        print(f"Retrieved {len(docs)} docs (showing first {min(k, len(docs))})\n")

        for idx, d in enumerate(docs[:k]):
            source = os.path.basename(d.metadata.get("source", ""))
            print(f"================ DOC {idx} | source: {source} ================\n")

            content = d.page_content
            if max_chars_per_doc is not None:
                content = content[:max_chars_per_doc]

            block = 1000
            for i in range(0, len(content), block):
                print(content[i : i + block])
                print("")
            print("\n" + "=" * 80 + "\n")

        return docs

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

        print("\n========== ANALYSIS ==========\n")
        print(f"Question: {question_en}\n")
        print(f"Approx. token overlap: {overlap:.1f}% of answer tokens appear in context.\n")

        print("API symbols in answer (ql.*):")
        print("  ", api_in_answer if api_in_answer else "None")
        print("\nAPI symbols also in context:")
        print("  ", api_in_both if api_in_both else "None")
        print("\nAPI symbols ONLY in answer (potential hallucination):")
        print("  ", api_only_in_answer if api_only_in_answer else "None")

        print("\nSources used by retriever:")
        for i, d in enumerate(docs):
            print(f"  DOC {i}: {os.path.basename(d.metadata.get('source', ''))}")

        print("\n==============================\n")

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
