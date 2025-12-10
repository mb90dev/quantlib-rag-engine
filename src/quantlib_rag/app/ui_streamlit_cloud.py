# src/quantlib_rag/app/ui_streamlit_cloud_qdrant.py

import streamlit as st

from src.quantlib_rag.rag.quantlib_cloud_assistant import QuantLibCloudAssistant


def get_cloud_assistant() -> QuantLibCloudAssistant:
    if "ql_cloud_assistant" not in st.session_state:
        st.session_state.ql_cloud_assistant = QuantLibCloudAssistant(
            groq_model="llama-3.1-8b-instant",
            temperature=0.0,
        )
    return st.session_state.ql_cloud_assistant


def main():
    st.set_page_config(page_title="QuantLib RAG — Cloud (Groq + Gemini + Qdrant)", layout="wide")
    st.title("📘 QuantLib RAG — Cloud profile")

    st.markdown(
        "- Retriever: **Qdrant Cloud** (Gemini embeddings)\n"
        "- LLM: **Groq** (`llama-3.1-8b-instant`)\n"
        "- Mode: **quote-only** on QuantLib-Python docs\n"
    )

    question = st.text_area(
        "Question about QuantLib-Python:",
        height=100,
        placeholder="e.g. Give a QuantLib-Python example of building a flat yield curve using FlatForward.",
    )

    k = st.slider("Number of retrieved chunks (k)", 1, 8, value=5)

    if st.button("Run") and question.strip():
        assistant = get_cloud_assistant()

        with st.spinner("Asking Groq with Qdrant + Gemini..."):
            res = assistant.quote_only_answer(question, k=k)

        st.subheader("🧾 Answer")
        st.write(res["answer_en"])

        st.subheader("📂 Sources")
        for s in res["sources"]:
            st.markdown(f"- `{s['source']}`")


if __name__ == "__main__":
    main()
