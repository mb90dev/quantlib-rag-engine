
from typing import TypedDict, List, Optional, Dict, Any
from langchain_core.documents import Document


class RAGState(TypedDict):
    """
    Shared state for the guarded RAG LangGraph pipeline.
    """
    question: str
    answer: Optional[str]
    contexts: List[Document]
    sources: List[Dict[str, Any]]
    verification: Optional[Dict[str, Any]]