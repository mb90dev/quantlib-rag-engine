from pathlib import Path
import os
# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------
# Plik config.py znajduje się w:
#     src/quantlib_rag/config.py
# czyli root to 3 poziomy wyżej.
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# DATA DIRECTORIES
# ---------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# markdowny pobrane z ReadTheDocs
MD_DIR = PROCESSED_DATA_DIR / "quantlib_md"


# ---------------------------------------------------------
# DATABASE / VECTORSTORE
# ---------------------------------------------------------
DB_DIR = PROJECT_ROOT / "db"

# domyślna lokalizacja Chroma z embeddingami BGE-M3
CHROMA_BGE_MD = DB_DIR / "quantlib_chroma_bge_md"


# ---------------------------------------------------------
# MODELS / EMBEDDINGS
# ---------------------------------------------------------
EMBEDDING_MODEL = "BAAI/bge-m3"

# instrukcja do BGE (prawidłowa dla retrievera)
BGE_QUERY_INSTRUCTION = (
    "Represent this question for retrieving relevant internal documentation: "
)

# ---------------------------------------------------------
# RAG / CHUNKING PARAMETERS
# ---------------------------------------------------------
MARKDOWN_HEADERS = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]

# jeśli będziesz używać klasycznego chunkera
DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200

# ile dokumentów pobiera retriever
DEFAULT_K = 5
QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_COLLECTION = "quantlib-rag-engine"

# Gemini embeddings
GEMINI_EMBED_MODEL = "gemini-embedding-001"