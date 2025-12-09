from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


from ..config import (
    MD_DIR,
    CHROMA_BGE_MD,
    EMBEDDING_MODEL,
    BGE_QUERY_INSTRUCTION,
    MARKDOWN_HEADERS,
    DEFAULT_K,
)

class QuantLibMarkdownIndexBuilder:
    """
    Buduje index Chroma na plikach .md z dokumentacja QuantLib:
    - laduje .md z katalogu (domyslnie: data/processed/quantlib_md)
    - dzieli po naglowkach markdown (h1/h2/h3)
    - embeduje BAAI/bge-m3
    - zapisuje index w db/quantlib_chroma_bge_md
    """

    def __init__(
        self,
        source_dir: Optional[Path] = None,
        db_dir: Optional[Path] = None,
        model_name: str = EMBEDDING_MODEL,
    ) -> None:


        self.source_dir = source_dir or MD_DIR
        self.db_dir = db_dir or CHROMA_BGE_MD

        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            encode_kwargs={"normalize_embeddings": True},
            query_instruction=BGE_QUERY_INSTRUCTION,
        )

    # 1. Ładowanie dokumentów (1:1 z Twojego kodu)

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

    # 2. Chunkowanie markdown-aware (1:1 z Twojego kodu)

    def split_markdown(self, docs: List[Document]) -> List[Document]:
        headers = [
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ]

        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers,
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

    # 3. Budowa i zapis indexu Chroma

    def build_index(self, chunks: List[Document]) -> Chroma:
        self.db_dir.parent.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Building Chroma index in: {self.db_dir}")

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=str(self.db_dir),
        )

        try:
            vectorstore.persist()
        except AttributeError:
            pass

        print("[INFO] Index built and persisted.")
        return vectorstore

    # 4. Pipeline end-to-end

    def run(self) -> None:
        docs = self.load_documents()
        chunks = self.split_markdown(docs)
        self.build_index(chunks)


def main() -> None:
    builder = QuantLibMarkdownIndexBuilder()
    builder.run()


if __name__ == "__main__":
    main()
