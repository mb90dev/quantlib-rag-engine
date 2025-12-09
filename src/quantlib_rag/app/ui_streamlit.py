import streamlit as st

#from quantlib_rag.rag.quantlib_assistant import QuantLibQuoteAssistant
#from quantlib_rag.rag.quantlib_index import QuantLibIndex
from src.quantlib_rag.rag.quantlib_assistant import QuantLibQuoteAssistant
from src.quantlib_rag.rag.quantlib_index import QuantLibIndex

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
            # db_path domyślnie z configu, więc nic nie podajemy
        )
    return st.session_state.ql_index


def main():
    st.set_page_config(page_title="QuantLib RAG Assistant", layout="wide")
    st.title("📘 QuantLib RAG Assistant (internal docs only)")

    st.markdown(
        "- **Search only** – pokazuje surowe fragmenty dokumentacji z retrievera\n"
        "- **Docs-based answer** – LLM odpowiada WYŁĄCZNIE na podstawie dokumentacji\n"
    )

    question = st.text_area(
        "Question about QuantLib-Python:",
        height=100,
        placeholder="e.g. Give a QuantLib-Python example of building a flat yield curve using FlatForward.",
    )

    mode = st.radio(
        "Mode",
        ["Search only (retriever)", "Docs-based answer (quote-only)"],
        index=0,
    )

    k = st.slider("Number of retrieved chunks (k)", 1, 8, value=5)

    if st.button("Run") and question.strip():
        if mode.startswith("Search"):
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

        else:  # Docs-based answer (quote-only)
            assistant = get_quote_assistant()
            with st.spinner("Asking LLM (docs-constrained)..."):
                res = assistant.quote_only_answer(question, k=k)

            st.subheader("🧾 Answer based on documentation")
            st.write(res["answer_en"])

            st.subheader("📂 Sources")
            for s in res["sources"]:
                st.markdown(f"- `{s['source']}`")


if __name__ == "__main__":
    main()
