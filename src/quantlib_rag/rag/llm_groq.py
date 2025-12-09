from langchain_groq import ChatGroq
import os
import streamlit as st  # jeśli chcesz używać też w Streamlit


def create_groq_llm(
    model: str = "llama-3.1-8b-instant",   # ✅ poprawiona nazwa
    temperature: float = 0.0,
) -> ChatGroq:
    """
    Zwraca ChatGroq skonfigurowany do użycia w RAG-u.
    Wymaga GROQ_API_KEY w env lub w Streamlit secrets.
    """
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Set it as env var or in Streamlit secrets."
        )

    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=api_key,
    )