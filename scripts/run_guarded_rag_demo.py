from src.quantlib_rag.rag.quantlib_assistant import QuantLibQuoteAssistant
from src.quantlib_rag.rag.llm_groq import create_groq_llm
from src.quantlib_rag.graph.guarded_rag import GuardedQuantLibRAG
from src.quantlib_rag.config import CHROMA_BGE_MD, LOCAL_MISTRAL_CACHE 


def create_local_quantlib_assistant() -> QuantLibQuoteAssistant:

    return QuantLibQuoteAssistant(
        db_path=CHROMA_BGE_MD,
        llm_model="mistral",
        temperature=0.0,
        k_default=5,
        cache_path=LOCAL_MISTRAL_CACHE,
        use_semantic_cache=True,
    )


def main():
    # 1) asystent lokalny (Mistral + Chroma + cache)
    assistant = create_local_quantlib_assistant()

    # 2) Groq jako LLM-as-judge
    judge_llm = create_groq_llm(
        model="llama-3.1-70b-versatile",
        temperature=0.0,
    )

    guarded = GuardedQuantLibRAG(
            assistant=assistant,
            judge_llm=judge_llm,
            k_for_verification=None,  # użyje assistant.k_default
        )   
    
    question = "How to build a FlatForward yield curve in QuantLib?"

    result = guarded.invoke(question_en=question)

    print("\n=== QUESTION ===")
    print(result["question_en"])

    print("\n=== ANSWER (guarded) ===")
    print(result["answer_en"])

    print("\n=== VERIFICATION ===")
    print(result["verification"])

    print("\n=== SOURCES ===")
    for src in result["sources"]:
        print(src)


if __name__ == "__main__":
    main()