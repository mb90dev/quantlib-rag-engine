# src/quantlib_rag/rag/judge.py

from typing import Dict, Any, List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
import json


JUDGE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a strict judge for a documentation-based QA assistant.
You receive: question, context, answer.
Return ONLY JSON with:
- is_grounded: true/false
- out_of_scope: true/false
- faithfulness_score: integer 1-5
- reason: short explanation in English."""),
    ("user", """Question:
{question}

Context:
{context}

Answer:
{answer}"""),
])


def _strip_code_fences(raw: str) -> str:
    """
    Remove Markdown ``` fences (optionally ```json) around the JSON payload.
    """
    text = raw.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        # wywal pierwszą linię ``` lub ```json
        lines = lines[1:]
        # jeśli ostatnia linia to znowu ``` – też wywalamy
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    return text


def verify_answer(
    llm: Runnable,
    question: str,
    answer: str,
    contexts: List[Document],
) -> Dict[str, Any]:
    context_str = "\n\n---\n\n".join([d.page_content for d in contexts])

    prompt = JUDGE_PROMPT.invoke({
        "question": question,
        "context": context_str,
        "answer": answer,
    })

    result = llm.invoke(prompt)

    # ChatGroq zwraca AIMessage z .content
    if hasattr(result, "content"):
        raw = result.content
    else:
        raw = str(result)

    cleaned = _strip_code_fences(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # awaryjnie – bez pieprzenia się, ale bez zabijania grafu
        data = {
            "is_grounded": False,
            "out_of_scope": True,
            "faithfulness_score": 1,
            "reason": f"Failed to parse judge JSON output. Raw content: {raw[:200]}",
        }

    return data
