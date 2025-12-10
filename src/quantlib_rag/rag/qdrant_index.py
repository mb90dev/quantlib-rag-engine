# src/quantlib_rag/rag/qdrant_index.py

from typing import Optional

from langchain_qdrant import QdrantVectorStore
import streamlit as st

from src.quantlib_rag.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    QDRANT_COLLECTION,
)
from src.quantlib_rag.rag.embeddings_gemini import create_gemini_embeddings


class QuantLibQdrantIndex:
    """
    Index QuantLib na Qdrant Cloud + Gemini embeddings.
  
    """

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        collection_name: Optional[str] = None,
        k_default: int = 5,
    ) -> None:
        self.url = url or QDRANT_URL or st.secrets.get("QDRANT_URL", None)
        self.api_key = api_key or QDRANT_API_KEY or st.secrets.get("QDRANT_API_KEY", None)
        self.collection_name = collection_name or QDRANT_COLLECTION
        self.k_default = k_default

        if not self.url:
            raise RuntimeError("QDRANT_URL is not set")
        if not self.api_key:
            raise RuntimeError("QDRANT_API_KEY is not set")

        self.embeddings = create_gemini_embeddings()
        vectorstore = QdrantVectorStore.from_existing_collection(

            embedding=self.embeddings,
            collection_name=QDRANT_COLLECTION,
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )

        self.vectorstore = vectorstore

    def get_retriever(self, k: Optional[int] = None) -> QdrantVectorStore:
        if k is None:
            k = self.k_default
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
