"""
Main bootstrap script for QuantLib RAG Engine.

Usage:
    python main.py
"""

import subprocess
from pathlib import Path
import sys

from src.quantlib_rag.config import (
    MD_DIR,
    CHROMA_BGE_MD,
)
from src.quantlib_rag.ingestion.download_quantlib_docs import QuantLibDocsDownloader
from src.quantlib_rag.ingestion.build_index import QuantLibMarkdownIndexBuilder


def run_streamlit():

    #print("\n[INFO] Launching Streamlit UI...\n")
    #project_root = Path(__file__).resolve().parent  # katalog z main.py
    #ui_path = project_root / "src" / "quantlib_rag" / "app" / "ui_streamlit.py"

    #subprocess.run(
    #    [sys.executable, "-m", "streamlit", "run", str(ui_path)],
    #    cwd=project_root,
    #)

    print("\n[INFO] Launching Streamlit UI...\n")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "src/quantlib_rag/app/ui_streamlit_groq.py"]
    )


def ensure_docs():
    if any(MD_DIR.glob("*.md")):
        print("[INFO] Markdown docs already present — skipping download.")
        return

    print("[INFO] Markdown docs NOT found — downloading...")
    QuantLibDocsDownloader().run()


def ensure_index():
    if CHROMA_BGE_MD.exists() and any(CHROMA_BGE_MD.glob("*")):
        print("[INFO] Chroma index already exists — skipping rebuild.")
        return

    print("[INFO] Chroma index NOT found — building index...")
    builder = QuantLibMarkdownIndexBuilder()
    builder.run()


def main():
    print("\n=== QuantLib RAG Engine ===")

    ensure_docs()
    ensure_index()
    run_streamlit()


if __name__ == "__main__":
    main()
