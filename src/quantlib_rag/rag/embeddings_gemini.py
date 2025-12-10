# src/quantlib_rag/rag/embeddings_gemini.py

import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
from src.quantlib_rag.config import GEMINI_EMBED_MODEL


def create_gemini_embeddings() -> GoogleGenerativeAIEmbeddings:
    """
    Embeddingi oparte o Google Gemini (gemini-embedding-001).
    Wymaga GOOGLE_API_KEY w env / secrets.
    """
    api_key = os.environ.get("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", None)

    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set")

    return GoogleGenerativeAIEmbeddings(
        model=GEMINI_EMBED_MODEL,
        google_api_key=api_key,
    )
