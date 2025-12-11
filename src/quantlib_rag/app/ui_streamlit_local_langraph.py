import streamlit as st

from src.quantlib_rag.rag.quantlib_assistant import QuantLibQuoteAssistant
from src.quantlib_rag.rag.quantlib_index import QuantLibIndex
from src.quantlib_rag.rag.llm_groq import create_groq_llm
from src.quantlib_rag.graph.guarded_rag import GuardedQuantLibRAG


def get_quote_assistant() -> QuantLibQuoteAssistant:
    if "ql_quote_assistant" not in st.session_state:
        st.session_state.ql_quote_assistant = QuantLibQuoteAssistant(
            llm_model="mistral",
            temperature=0.0,
            k_default=5,
        )
    return st.session_state.ql_quote_assistant


def get_index() -> QuantLibIndex:
    if "ql_index" not in st.session_state:
        st.session_state.ql_index = QuantLibIndex(
            # db_path domyślnie z configu
        )
    return st.session_state.ql_index


def get_guarded_rag() -> GuardedQuantLibRAG:
    """
    Lazy-init GuardedQuantLibRAG (assistant + Groq judge) w session_state.
    """
    if "guarded_rag" not in st.session_state:
        assistant = get_quote_assistant()
        judge_llm = create_groq_llm(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
        )
        st.session_state.guarded_rag = GuardedQuantLibRAG(
            assistant=assistant,
            judge_llm=judge_llm,
            k_for_verification=None,  # użyje assistant.k_default
        )
    return st.session_state.guarded_rag


def main():
    st.set_page_config(page_title="QuantLib RAG Assistant", layout="wide")
    st.title("📘 QuantLib RAG Assistant (internal docs only)")

    st.markdown(
        "- **Search only** – pokazuje surowe fragmenty dokumentacji z retrievera\n"
        "- **Docs-based answer (guarded)** – odpowiedź z LLM **zweryfikowana** przez LLM-as-judge (LangGraph)\n"
    )

    question = st.text_area(
        "Question about QuantLib-Python:",
        height=100,
        placeholder="e.g. Give a QuantLib-Python example of building a flat yield curve using FlatForward.",
    )

    mode = st.radio(
        "Mode",
        ["Search only (retriever)", "Docs-based answer (guarded)"],
        index=0,
    )

    k = st.slider("Number of retrieved chunks (k)", 1, 8, value=5)

    if st.button("Run") and question.strip():
        if mode.startswith("Search"):
            # 🔎 czysty retriever, jak wcześniej
            index = get_index()
            retriever = index.get_retriever(k=k)

            with st.spinner("Retrieving documentation..."):
                docs = retriever.invoke(question)

            st.subheader("🔎 Retrieved documentation chunks")
            if not docs:
                st.info("No documents retrieved.")
            else:
                for i, d in enumerate(docs):
                    source = d.metadata.get("source", "")
                    source_name = source.split("/")[-1] if source else "unknown"
                    with st.expander(f"Result {i+1} — {source_name}"):
                        st.code(d.page_content)

        else:  # Docs-based answer (guarded)
            guarded = get_guarded_rag()

            with st.spinner("Running guarded RAG (docs-constrained + judge)..."):
                res = guarded.invoke(question_en=question)

            st.subheader("🧾 Answer based on documentation (guarded)")
            st.write(res["answer_en"])

            # verification info
            st.subheader("✅ Verification (LLM-as-judge)")
            v = res.get("verification") or {}
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("is_grounded", str(v.get("is_grounded", "n/a")))
            with col2:
                st.metric("out_of_scope", str(v.get("out_of_scope", "n/a")))
            with col3:
                st.metric("faithfulness_score", v.get("faithfulness_score", "n/a"))

            if v.get("reason"):
                st.caption(f"Judge reason: {v['reason']}")

            st.subheader("📂 Sources")
            for s in res["sources"]:
                st.markdown(f"- `{s['source']}`")


if __name__ == "__main__":
    main()
