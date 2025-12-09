from pathlib import Path
from typing import Optional

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever


from ..config import *

class QuantLibIndex:
    """
    Odpowiada za:
    - wczytanie embeddings (BAAI/bge-m3)
    - wczytanie ChromaDB z dysku
    - wystawienie retrievera (as_retriever)

    Zakładamy, że index został wcześniej zbudowany
    (np. build_index.py) w katalogu db/quantlib_chroma_bge_md_v2.
    """

    def __init__(
        self,
        db_path: Optional[str | Path] = None,
        model_name: str = EMBEDDING_MODEL,
        k_default: int = DEFAULT_K,
    ) -> None:
        if db_path is None:
            db_path = CHROMA_BGE_MD

        self.db_path = Path(db_path)
        self.k_default = k_default

        # Embeddings BGE (enterprise mode)
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            encode_kwargs={"normalize_embeddings": True},
            query_instruction=BGE_QUERY_INSTRUCTION,
        )

        # Podpięcie Chroma
        self.vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory=str(self.db_path),
        )

    def get_retriever(self, k: Optional[int] = None) -> VectorStoreRetriever:
        """
        Zwraca VectorStoreRetriever z ustawionym k.
        """
        if k is None:
            k = self.k_default
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
