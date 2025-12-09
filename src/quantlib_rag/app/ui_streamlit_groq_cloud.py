import os
import streamlit as st

from src.quantlib_rag import config
from src.quantlib_rag.ingestion.download_quantlib_docs import QuantLibDocsDownloader
from src.quantlib_rag.ingestion.build_index import QuantLibMarkdownIndexBuilder
from src.quantlib_rag.rag.llm_groq import create_groq_llm
from src.quantlib_rag.rag.quantlib_assistant import QuantLibQuoteAssistant


# --------- HELPERY: DOCS + INDEX ---------

def ensure_docs_and_index() -> None:
    """Upewnia się, że .md i index Chroma są gotowe (Cloud / lokalnie)."""
    # 1) markdowny
    if not any(config.MD_DIR.glob("*.md")):
        st.write("📥 Downloading QuantLib-Python docs...")
        downloader = QuantLibDocsDownloader()
        downloader.run()
    else:
        print("[BOOTSTRAP] Markdown docs already present.")

    # 2) index chroma
    if not config.CHROMA_BGE_MD.exists() or not any(config.CHROMA_BGE_MD.glob("*")):
        st.write("🔧 Building Chroma index...")
        builder = QuantLibMarkdownIndexBuilder()
        builder.run()
    else:
        print("[BOOTSTRAP] Chroma index already present.")


# --------- PASSWORD GATE ---------

def check_password() -> bool:
    """
    Hasło do apki:
    - APP_PASSWORD w st.secrets (Cloud)
    - albo w env APP_PASSWORD (lokalnie do testów)
    """
    expected = st.secrets.get("APP_PASSWORD", None) or os.environ.get("APP_PASSWORD")

    if not expected:
        # jak nie ustawisz hasła -> brak blokady
        return True

    if "pw_ok" not in st.session_state:
        st.session_state.pw_ok = False

    if not st.session_state.pw_ok:
        st.write("This app is password protected.")
        pw = st.text_input("Password", type="password")
        if pw == "":
            st.stop()
        if pw == expected:
            st.session_state.pw_ok = True
        else:
            st.error("Wrong password")
            st.stop()

    return True


# --------- LAZY INIT ASSISTANTA Z GROQ ---------

def get_groq_assistant() -> QuantLibQuoteAssistant:
    if "ql_groq_assistant" not in st.session_state:
        # 🔥 tu dbamy o docs + index
        ensure_docs_and_index()

        llm = create_groq_llm(
            model="llama-3.1-8b-instant",
            temperature=0.0,
        )

        st.session_state.ql_groq_assistant = QuantLibQuoteAssistant(
            llm=llm,
            k_default=5,
        )
    return st.session_state.ql_groq_assistant


# --------- STREAMLIT UI (Cloud) ---------

def main():
    st.set_page_config(page_title="QuantLib RAG (Groq, Cloud)", layout="wide")
    st.title("📘 QuantLib RAG Assistant — Groq (Streamlit Cloud)")

    # 🔐 hasło (opcjonalne – jak ustawisz APP_PASSWORD)
    check_password()

    st.markdown(
        "Backend:\n"
        "- **Retriever**: Chroma + BGE (BAAI/bge-m3)\n"
        "- **LLM**: Groq `llama-3.1-8b-instant`\n"
        "- Tryb: **quote-only** (LLM TYLKO cytuje dokumentację)\n"
    )

    question = st.text_area(
        "Question about QuantLib-Python:",
        height=100,
        placeholder="e.g. What is a Date in QuantLib-Python?",
    )

    k = st.slider("Number of retrieved chunks (k)", 1, 8, value=5)

    if st.button("Run") and question.strip():
        assistant = get_groq_assistant()

        with st.spinner("Asking Groq (quote-only)..."):
            res = assistant.quote_only_answer(question, k=k)

        st.subheader("🧾 Quote-only answer")
        st.write(res["answer_en"])

        st.subheader("📂 Sources")
        for s in res["sources"]:
            st.markdown(f"- `{s['source']}`")


if __name__ == "__main__":
    main()
