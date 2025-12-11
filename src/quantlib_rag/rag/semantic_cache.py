# src/rag/semantic_cache.py

#from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


class SemanticAnswerCache:
    """
    Semantic cache odpowiedzi:
    - embeduje *pytania* (page_content = question)
    - trzyma pełny wynik (question_en, answer_en, sources) w metadata["payload"]
    """

    def __init__(
        self,
        persist_dir: str | Path,
        embeddings: HuggingFaceBgeEmbeddings,
        collection_name: str = "semantic_answer_cache",
        score_threshold: float = 0.75,   # na start trochę niżej
        verbose: bool = True,
    ) -> None:
        self.persist_dir = Path(persist_dir)
        self.score_threshold = score_threshold
        self.verbose = verbose

        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=str(self.persist_dir),
        )

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def get(self, question: str) -> Optional[Dict[str, Any]]:
        """
        Zwraca cached answer, jeśli najbardziej podobne pytanie
        ma podobieństwo >= score_threshold.
        """
        try:
            results = self.vectorstore.similarity_search_with_relevance_scores(
                question,
                k=1,
            )
        except TypeError:
            self._log("[SEMANTIC CACHE] similarity_search_with_relevance_scores not supported")
            return None

        if not results:
            self._log("[SEMANTIC CACHE MISS] no candidates")
            return None

        doc, relevance = results[0]
        self._log(
            f"[SEMANTIC CACHE CANDIDATE] score={relevance:.3f} | stored_q={doc.page_content!r}"
        )

        if relevance < self.score_threshold:
            self._log(
                f"[SEMANTIC CACHE MISS] score {relevance:.3f} < threshold {self.score_threshold:.3f}"
            )
            return None

        payload_json = doc.metadata.get("payload")
        if not payload_json:
            self._log("[SEMANTIC CACHE ERROR] no payload in metadata")
            return None

        try:
            payload = json.loads(payload_json)
        except Exception:
            self._log("[SEMANTIC CACHE ERROR] failed to parse JSON payload")
            return None

        self._log(f"[SEMANTIC CACHE HIT] using cached answer (score={relevance:.3f})")
        return payload

    def set(self, question: str, payload: Dict[str, Any]) -> None:
        """
        Zapisuje nową odpowiedź do cache.
        """
        self._log(f"[SEMANTIC CACHE STORE] storing answer for question: {question!r}")
        doc = Document(
            page_content=question,  # <-- embedujemy TYLKO pytanie
            metadata={
                "payload": json.dumps(payload, ensure_ascii=False),
            },
        )
        self.vectorstore.add_documents([doc])
