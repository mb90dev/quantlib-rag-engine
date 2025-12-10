# src/quantlib_rag/rag/quantlib_cloud_assistant.py

import os
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

    @staticmethod
    def _format_context(docs: List[Document], max_chars_per_doc: int = 800) -> str:
        snippets = [d.page_content[:max_chars_per_doc] for d in docs]
        return "\n\n--- DOC SPLIT ---\n\n".join(snippets)

    def quote_only_answer(
        self,
        question_en: str,
        k: Optional[int] = None,
        max_chars_per_doc: int = 800,
    ) -> Dict[str, Any]:
        if k is None:
            k = self.k_default

        docs = self.retriever.invoke(question_en)

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
