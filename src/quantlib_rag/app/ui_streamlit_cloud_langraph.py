# src/quantlib_rag/app/ui_streamlit_cloud_qdrant.py

import os
import hmac
import streamlit as st

from src.quantlib_rag.rag.quantlib_cloud_assistant import QuantLibCloudAssistant
from src.quantlib_rag.rag.llm_groq import create_groq_llm
from src.quantlib_rag.graph.guarded_rag import GuardedQuantLibRAG


def check_password() -> bool:
    """
    Simple password gate for Streamlit apps.
    - password is stored in st.secrets["APP_PASSWORD"] or env APP_PASSWORD
    - uses constant-time compare (hmac.compare_digest)
    - keeps auth state in st.session_state
    """
    if st.session_state.get("authenticated", False):
        return True

    # Read password from Streamlit Secrets or environment
    expected = None
    try:
        expected = st.secrets.get("APP_PASSWORD", None)
    except Exception:
        expected = None

    expected = expected or os.environ.get("APP_PASSWORD")

    if not expected:
        st.error("APP_PASSWORD is not configured. Set it in Streamlit Secrets or as env var.")
        st.stop()

    st.markdown("### 🔒 Enter password to access this app")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if hmac.compare_digest(pwd, expected):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Wrong password.")
            st.session_state["authenticated"] = False

    return False


def get_cloud_assistant() -> QuantLibCloudAssistant:
    """
    Lazy-init cloud assistant (Groq + Gemini + Qdrant) in Streamlit session.
    """
    if "ql_cloud_assistant" not in st.session_state:
        st.session_state.ql_cloud_assistant = QuantLibCloudAssistant(
            groq_model="llama-3.1-8b-instant",
            temperature=0.0,
        )
    return st.session_state.ql_cloud_assistant


def get_guarded_cloud_pipeline() -> GuardedQuantLibRAG:
    """
    Lazy-init guarded RAG wrapper around the cloud assistant.
    Uses Groq as LLM-as-judge.
    """
    if "ql_guarded_cloud" not in st.session_state:
        assistant = get_cloud_assistant()
        judge_llm = create_groq_llm(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
        )
        st.session_state.ql_guarded_cloud = GuardedQuantLibRAG(
            assistant=assistant,
            judge_llm=judge_llm,
            k_for_verification=None,  # użyje assistant.k_default
        )
    return st.session_state.ql_guarded_cloud


def main():
    # ✅ set_page_config TYLKO RAZ, na początku
    st.set_page_config(
        page_title="QuantLib RAG — Cloud (Groq + Gemini + Qdrant)",
        layout="wide",
    )

    # ✅ PASSWORD GATE NA START
    if not check_password():
        st.stop()

    # ✅ Logout w sidebarze
    with st.sidebar:
        st.markdown("### Session")
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

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

    guarded_mode = st.checkbox(
        "Guarded mode (LLM-as-judge, no hallucinations, out-of-scope detection)",
        value=True,
    )

    if st.button("Run") and question.strip():
        assistant = get_cloud_assistant()

        if guarded_mode:
            guarded = get_guarded_cloud_pipeline()
            with st.spinner("Running guarded RAG (Groq + Qdrant + judge)..."):
                res = guarded.invoke(question_en=question)
        else:
            with st.spinner("Asking Groq with Qdrant + Gemini..."):
                res = assistant.quote_only_answer(question, k=k)

        st.subheader("🧾 Answer")
        st.write(res["answer_en"])

        st.subheader("📂 Sources")
        for s in res["sources"]:
            source = s.get("source", "")
            short = os.path.basename(source)
            st.markdown(f"- `{short}`")

        if guarded_mode:
            st.subheader("🔍 Verification (LLM-as-judge)")
            st.json(res["verification"])


if __name__ == "__main__":
    main()
