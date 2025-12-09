# src/quantlib_rag/app/ui_streamlit_groq.py

import os

import streamlit as st

from src.quantlib_rag.rag.quantlib_assistant import QuantLibQuoteAssistant
from src.quantlib_rag.rag.llm_groq import create_groq_llm


# --------- PASSWORD GATE ---------

def check_password() -> bool:
    """
    Proste zabezpieczenie hasłem:
    - hasło w st.secrets["APP_PASSWORD"] (Streamlit Cloud)
      lub w env APP_PASSWORD
    """
    expected = None
    try:
        expected = st.secrets.get("APP_PASSWORD")
    except Exception:
        expected = None

    if not expected:
        expected = os.environ.get("APP_PASSWORD")

    # jeśli nie ustawiono hasła -> brak zabezpieczenia
    if not expected:
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
        llm = create_groq_llm(
            model="llama-3.1-8b-instant",  
            temperature=0.0,
        )
        st.session_state.ql_groq_assistant = QuantLibQuoteAssistant(
            llm=llm,      # 🔹 tu wstrzykujemy gotowy ChatGroq
            k_default=5,
        )
    return st.session_state.ql_groq_assistant


# --------- STREAMLIT UI (tylko Groq backend) ---------

def main():
    st.set_page_config(page_title="QuantLib RAG (Groq)", layout="wide")
    st.title("📘 QuantLib RAG Assistant — Groq backend")

    # 🔐 hasło
    #check_password()

    st.markdown(
        "This instance uses **Groq** as the LLM backend.\n\n"
        "- Retrieval: BGE + Chroma\n"
        "- LLM: Groq (e.g. LLaMA 3.1 8B)\n"
    )

    question = st.text_area(
        "Question about QuantLib-Python:",
        height=100,
        placeholder="e.g. Give a QuantLib-Python example of building a flat yield curve using FlatForward.",
    )

    mode = st.radio(
        "Mode",
        ["Quote-only (LLM copies docs)", "Full RAG (LLM + docs)"],
        index=0,
    )

    k = st.slider("Number of retrieved chunks (k)", 1, 8, value=5)

    if st.button("Run") and question.strip():
        assistant = get_groq_assistant()

        if mode.startswith("Quote-only"):
            with st.spinner("Asking Groq (quote-only)..."):
                res = assistant.quote_only_answer(question, k=k)

            st.subheader("🧾 Quote-only answer (copied from docs)")
            st.write(res["answer_en"])

            st.subheader("📂 Sources")
            for s in res["sources"]:
                st.markdown(f"- `{s['source']}`")

        else:
            # zakładam, że masz w QuantLibAssistant coś w stylu rag_answer(...)
            # Jeśli nie, użyjesz innej metody – dostosujesz pod swój kod.
            with st.spinner("Asking Groq with RAG..."):
                res = assistant.rag_answer(question, k=k)

            st.subheader("🧠 Full RAG answer")
            st.write(res["answer"])

            st.subheader("📂 Sources")
            for s in res["sources"]:
                st.markdown(f"- `{s['source']}`")


if __name__ == "__main__":
    main()
