import os
import time
import json
from typing import Any, Dict, List, Optional

import pandas as pd
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage

from ..config import DEFAULT_K


class QuantLibRAGEvaluator:
    """
    Ewaluacja RAG-a na dokumentacji QuantLib-Python.

    - liczy hit@k (retriever)
    - opcjonalnie używa LLM-as-judge (faithfulness, helpfulness)
    - korzysta z analyze_answer_vs_context jako dodatkowej metryki
    - potrafi też dograć oceny sędziego na już gotowym DataFrame (offline judge)
    """

    def __init__(
        self,
        assistant: Any,             # QuantLibQuoteAssistant lub QuantLibCloudAssistant
        judge_llm: Any,             # np. ChatGroq / ChatOllama, może być też None
        backend_name: str,          # "local" / "cloud" / co chcesz
        k_default: Optional[int] = None,
    ) -> None:
        self.assistant = assistant
        self.judge_llm = judge_llm
        self.backend_name = backend_name

        if k_default is not None:
            self.k_default = k_default
        else:
            self.k_default = getattr(assistant, "k_default", DEFAULT_K)

    # ---------- RETRIEVAL: HIT@K ----------

    def compute_hit_at_k(
        self,
        question_en: str,
        gold_source: str,
        k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        gold_source: np. 'termstructures.md' albo pełna ścieżka, którą potem obcinasz do basename.
        """
        if k is None:
            k = self.k_default

        retriever = self.assistant.index.get_retriever(k=k)
        docs: List[Document] = retriever.invoke(question_en)

        sources = [
            os.path.basename(d.metadata.get("source", "")) for d in docs[:k]
        ]
        gold_basename = os.path.basename(gold_source)

        hit = 1 if gold_basename in sources else 0

        return {
            "backend": self.backend_name,
            "question": question_en,
            "gold_source": gold_basename,
            "retrieved_sources": sources,
            "hit_at_k": hit,
            "k": k,
        }

    # ---------- LLM-AS-JUDGE (INLINE) ----------

    def judge_answer(
        self,
        question_en: str,
        context_docs: List[Document],
        answer: str,
    ) -> Dict[str, Any]:
        """
        LLM ocenia:
        - faithfulness (1-5)
        - helpfulness (1-5)
        """

        # jeśli nie ma sędziego -> nic nie robimy
        if self.judge_llm is None:
            return {
                "backend": self.backend_name,
                "faithfulness": None,
                "helpfulness": None,
                "notes": "judge_disabled",
            }

        context_text = self.assistant._format_context(
            context_docs, max_chars_per_doc=800
        )

        system = SystemMessage(
            content=(
                "You are an evaluator for a RAG system over QuantLib-Python docs.\n"
                "You get a QUESTION, CONTEXT (retrieved docs) and an ANSWER.\n"
                "You must judge:\n"
                "- faithfulness: does the answer follow only from CONTEXT? (1-5)\n"
                "- helpfulness: does the answer properly answer the QUESTION? (1-5)\n"
                "Return STRICT JSON with keys: faithfulness, helpfulness, notes.\n"
                "Example:\n"
                "{\n"
                '  \"faithfulness\": 4,\n'
                '  \"helpfulness\": 5,\n'
                '  \"notes\": \"short explanation\"\n'
                "}\n"
                "Do not add any other text."
            )
        )

        user = HumanMessage(
            content=(
                f"QUESTION:\n{question_en}\n\n"
                f"CONTEXT:\n{context_text}\n\n"
                f"ANSWER:\n{answer}\n\n"
                "Now respond ONLY with JSON."
            )
        )

        # --- 1. bezpieczne wywołanie sędziego (błędy sieci itp.) ---
        try:
            resp = self.judge_llm.invoke([system, user])
            raw = resp.content.strip()
        except Exception as e:
            return {
                "backend": self.backend_name,
                "faithfulness": None,
                "helpfulness": None,
                "notes": f"judge_invoke_error: {e}",
            }

        # --- 2. parsowanie JSON-a z odpowiedzi modelu ---
        def _safe_parse_json(text: str) -> Dict[str, Any]:
            # 1) czysty JSON
            if text.startswith("{") and text.endswith("}"):
                return json.loads(text)

            # 2) wytnij fragment między pierwszym '{' a ostatnim '}'
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                candidate = text[start : end + 1]
                return json.loads(candidate)

            raise ValueError(
                "Could not extract JSON from judge response: %r" % text
            )

        try:
            scores = _safe_parse_json(raw)
        except Exception as e:
            return {
                "backend": self.backend_name,
                "faithfulness": None,
                "helpfulness": None,
                "notes": f"judge_parse_error: {e}",
            }

        return {
            "backend": self.backend_name,
            "faithfulness": scores.get("faithfulness"),
            "helpfulness": scores.get("helpfulness"),
            "notes": scores.get("notes", ""),
        }

    # ---------- PEŁNA EWALUACJA JEDNEGO PYTANIA ----------

    def evaluate_single(
        self,
        question_en: str,
        gold_source: str,
        k: Optional[int] = None,
        use_judge: bool = True,
    ) -> Dict[str, Any]:
        """
        1. retrieval -> docs
        2. assistant -> answer
        3. hit@k
        4. judge (LLM-as-judge) - jeśli use_judge=True
        5. analyze_answer_vs_context
        """
        if k is None:
            k = self.k_default

        retriever = self.assistant.index.get_retriever(k=k)

        # retrieval
        t0 = time.time()
        docs = retriever.invoke(question_en)
        t1 = time.time()

        # odpowiedź z asystenta (quote-only, ale możesz podmienić)
        result = self.assistant.quote_only_answer(question_en, k=k)
        answer = result["answer_en"]
        t2 = time.time()

        # hit@k
        hit_data = self.compute_hit_at_k(question_en, gold_source, k=k)

        # judge (opcjonalnie)
        if use_judge:
            judge_data = self.judge_answer(question_en, docs[:k], answer)
        else:
            judge_data = {
                "backend": self.backend_name,
                "faithfulness": None,
                "helpfulness": None,
                "notes": "judge_skipped",
            }

        # analiza halucynacji
        hallucination_data = self.assistant.analyze_answer_vs_context(
            question_en, answer, k=k
        )

        return {
            "backend": self.backend_name,
            "question": question_en,
            "gold_source": hit_data["gold_source"],
            "hit_at_k": hit_data["hit_at_k"],
            "faithfulness": judge_data["faithfulness"],
            "helpfulness": judge_data["helpfulness"],
            "judge_notes": judge_data["notes"],
            "latency_retrieval_ms": (t1 - t0) * 1000,
            "latency_llm_ms": (t2 - t1) * 1000,
            "overlap_percent": hallucination_data["overlap_percent"],
            "api_only_in_answer": list(hallucination_data["api_only_in_answer"]),
            "answer_en": answer,
        }

    # ---------- BATCH + DATAFRAME (INLINE) ----------

    def evaluate_dataset(
        self,
        test_set: List[Dict[str, str]],
        k: Optional[int] = None,
        use_judge: bool = True,
    ) -> pd.DataFrame:
        """
        test_set = [
            {"question": "...", "gold_source": "termstructures.md"},
            ...
        ]

        use_judge:
            - True  -> od razu liczy oceny sędziego (cloud, stabilna sieć)
            - False -> zbiera tylko odpowiedzi + hit@k + overlap (local Mistral),
                      można później dograć sędziego metodą judge_existing_answers.
        """
        rows: List[Dict[str, Any]] = []
        for item in test_set:
            row = self.evaluate_single(
                question_en=item["question"],
                gold_source=item["gold_source"],
                k=k,
                use_judge=use_judge,
            )
            rows.append(row)

        df = pd.DataFrame(rows)
        return df

    # ---------- FAZA 2: SĘDZIA NA GOTOWYM DATAFRAME ----------

    def judge_existing_answers(
        self,
        df: pd.DataFrame,
        k: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Dogrywa oceny sędziego do istniejącego DataFrame'a.

        Zakłada, że w df są kolumny:
        - 'question'
        - 'answer_en'

        Zwraca NOWY DataFrame z dodanymi/uzupełnionymi:
        - 'faithfulness'
        - 'helpfulness'
        - 'judge_notes'
        """
        if self.judge_llm is None:
            # nic nie robimy - tylko kopiujemy
            df_out = df.copy()
            if "judge_notes" not in df_out.columns:
                df_out["judge_notes"] = "judge_disabled"
            return df_out

        if k is None:
            k = self.k_default

        faithfulness_list = []
        helpfulness_list = []
        notes_list = []

        # używamy retrievera z tego samego assistanta
        retriever = self.assistant.index.get_retriever(k=k)

        for _, row in df.iterrows():
            question = row["question"]
            answer = row["answer_en"]

            docs = retriever.invoke(question)
            judge_data = self.judge_answer(question, docs[:k], answer)

            faithfulness_list.append(judge_data["faithfulness"])
            helpfulness_list.append(judge_data["helpfulness"])
            notes_list.append(judge_data["notes"])

        df_out = df.copy()
        df_out["faithfulness"] = faithfulness_list
        df_out["helpfulness"] = helpfulness_list
        df_out["judge_notes"] = notes_list

        return df_out
