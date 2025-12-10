
from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.quantlib_rag.config import (
    MD_DIR,
    MARKDOWN_HEADERS,
    QDRANT_URL,
    QDRANT_API_KEY,
    QDRANT_COLLECTION,
)
from src.quantlib_rag.rag.embeddings_gemini import create_gemini_embeddings


class QuantLibQdrantIndexBuilder:
    """
    Buduje index Qdrant na plikach .md z dokumentacją QuantLib:
    - ładuje .md z katalogu (domyślnie: MD_DIR)
    - dzieli po nagłówkach markdown (MARKDOWN_HEADERS z configu)
    - embeduje przez Gemini embeddings
    - wrzuca dokumenty do kolekcji Qdrant (QDRANT_COLLECTION)
    """

    def __init__(
        self,
        source_dir: Optional[Path] = None,
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None,
        collection_name: str = QDRANT_COLLECTION,
    ) -> None:
        self.source_dir = source_dir or MD_DIR
        self.qdrant_url = qdrant_url or QDRANT_URL
        self.qdrant_api_key = qdrant_api_key or QDRANT_API_KEY
        self.collection_name = collection_name

        if not self.qdrant_url or not self.qdrant_api_key:
            raise RuntimeError("QDRANT_URL / QDRANT_API_KEY are not set")

        # Klient Qdrant
        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
        )

        # Embeddings (Gemini)
        self.embeddings = create_gemini_embeddings()

    # 1. Ładowanie dokumentów

    def load_documents(self) -> List[Document]:
        loader = DirectoryLoader(
            str(self.source_dir),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        docs = loader.load()
        print("Docs:", len(docs))
        return docs

    # 2. Chunkowanie markdown-aware

    def split_markdown(self, docs: List[Document]) -> List[Document]:
        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=MARKDOWN_HEADERS,
            strip_headers=False,
        )

        chunks: List[Document] = []
        for d in docs:
            md_chunks = md_splitter.split_text(d.page_content)
            for c in md_chunks:
                c.metadata.update(d.metadata)
            chunks.extend(md_chunks)

        print("Markdown-aware chunks:", len(chunks))
        return chunks

    # 3. Budowa kolekcji i indexu Qdrant

    def _recreate_collection(self) -> None:
        """
        Tworzy (lub odtwarza) kolekcję w Qdrant z poprawnym wymiarem wektora.
        """
        # Ustalamy rozmiar wektora z embeddings
        test_vec = self.embeddings.embed_query("dimension_check")
        dim = len(test_vec)
        print(f"[INFO] Embedding dimension: {dim}")

        # Jeśli kolekcja istnieje – usuwamy
        if self.client.collection_exists(self.collection_name):
            print(f"[INFO] Deleting existing collection '{self.collection_name}'")
            self.client.delete_collection(self.collection_name)

        print(f"[INFO] Creating collection '{self.collection_name}'")
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=dim,
                distance=Distance.COSINE,
            ),
        )

    def build_index(self, chunks: List[Document]) -> None:
        print(
            f"[INFO] Pushing {len(chunks)} chunks to Qdrant collection "
            f"'{self.collection_name}'"
        )

        # 1) (Re)tworzymy kolekcję
        self._recreate_collection()

        # 2) Tworzymy vectorstore na istniejącej kolekcji
        vectorstore = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
        )

        # 3) Dodajemy dokumenty
        vectorstore.add_documents(chunks)

        print("[INFO] Qdrant index built.")

    def run(self) -> None:
        docs = self.load_documents()
        chunks = self.split_markdown(docs)
        self.build_index(chunks)