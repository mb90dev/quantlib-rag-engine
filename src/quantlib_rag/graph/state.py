

from typing import TypedDict, List, Optional, Dict, Any
from langchain_core.documents import Document


class GuardedRAGState(TypedDict):
    """
    Shared state for the guarded QuantLib RAG pipeline.
    """
    question_en: str
    answer_en: Optional[str]
    sources: List[Dict[str, Any]]
    contexts: List[Document]
    verification: Optional[Dict[str, Any]]
