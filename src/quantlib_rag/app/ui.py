import streamlit as st
from src.quantlib_rag.rag.quantlib_index import QuantLibIndex
from src.quantlib_rag.rag.quantlib_assistant import QuantLibQuoteAssistant
st.set_page_config(page_title="QuantLib RAG", layout="wide")

st.title("🔍 QuantLib RAG – minimalny test UI")
st.write("Jeśli to widzisz, sama aplikacja Streamlit działa, bez logiki RAG.")