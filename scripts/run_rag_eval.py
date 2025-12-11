# src/quantlib_rag/scripts/run_rag_eval.py

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Dict

import pandas as pd

from pathlib import Path
import sys


from src.quantlib_rag.rag.quantlib_assistant import QuantLibQuoteAssistant
from src.quantlib_rag.rag.quantlib_cloud_assistant import QuantLibCloudAssistant
from src.quantlib_rag.rag.quantlib_rag_evaluator import QuantLibRAGEvaluator
from src.quantlib_rag.rag.llm_groq import create_groq_llm
from src.quantlib_rag.config import DEFAULT_K


# ---------- TEST SET ----------

def build_test_set() -> List[Dict[str, str]]:
    """Zestaw pytań do ewaluacji RAG-a."""

    return [
        # basics.md
        {
            "question": "How do I set up the evaluation date in QuantLib?",
            "gold_source": "basics.md",
        },
        {
            "question": "Which core QuantLib types are typically used when starting a simple pricing example?",
            "gold_source": "basics.md",
        },

        # dates.md
        {
            "question": "How do I create a QuantLib Date and convert it from a Python datetime?",
            "gold_source": "dates.md",
        },
        {
            "question": "How can I advance a date by a given number of months using QuantLib?",
            "gold_source": "dates.md",
        },

        # cashflows.md
        {
            "question": "How do I build a leg of fixed cashflows in QuantLib?",
            "gold_source": "cashflows.md",
        },
        {
            "question": "How can I get the payment dates and amounts from a cashflow leg in QuantLib?",
            "gold_source": "cashflows.md",
        },

        # indexes.md
        {
            "question": "How do I construct an IborIndex in QuantLib?",
            "gold_source": "indexes.md",
        },
        {
            "question": "How can I link an index to a yield term structure in QuantLib?",
            "gold_source": "indexes.md",
        },

        # instruments.md
        {
            "question": "How do I create a simple fixed-rate bond instrument in QuantLib?",
            "gold_source": "instruments.md",
        },
        {
            "question": "How can I retrieve the NPV of an instrument after assigning a pricing engine in QuantLib?",
            "gold_source": "instruments.md",
        },

        # pricing_engines.md
        {
            "question": "How do I set a discounting bond pricing engine in QuantLib?",
            "gold_source": "pricing_engines.md",
        },
        {
            "question": "Which pricing engines are commonly used for bond and swap pricing in QuantLib?",
            "gold_source": "pricing_engines.md",
        },

        # termstructures.md
        {
            "question": "How do I build a flat yield term structure in QuantLib?",
            "gold_source": "termstructures.md",
        },
        {
            "question": "How can I bootstrap a zero curve from market instruments in QuantLib?",
            "gold_source": "termstructures.md",
        },
    ]


# ---------- RUNNERS ----------

def run_local_phase1(out_dir: Path) -> pd.DataFrame:
    """Local Mistral – FAZA 1: bez judge (odpalenie Mistrala + zapis do cache)."""
    test_set = build_test_set()

    local_assistant = QuantLibQuoteAssistant(
        llm_model="mistral",
        temperature=0.0,
        k_default=DEFAULT_K,
        # cache_path domyślnie z configu (LOCAL_MISTRAL_CACHE)
    )

    evaluator = QuantLibRAGEvaluator(
        assistant=local_assistant,
        judge_llm=None,
        backend_name="local",
        k_default=DEFAULT_K,
    )

    df = evaluator.evaluate_dataset(
        test_set=test_set,
        k=None,
        use_judge=False,
    )

    out_dir.mkdir(exist_ok=True, parents=True)
    df.to_csv(out_dir / "local_eval_phase1_no_judge.csv", index=False)
    return df


def run_local_full(out_dir: Path) -> pd.DataFrame:
    """Local Mistral – FAZA 2: z judge (korzysta z cache odpowiedzi)."""
    test_set = build_test_set()

    local_assistant = QuantLibQuoteAssistant(
        llm_model="mistral",
        temperature=0.0,
        k_default=DEFAULT_K,
    )

    judge_llm = create_groq_llm(
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )

    evaluator = QuantLibRAGEvaluator(
        assistant=local_assistant,
        judge_llm=judge_llm,
        backend_name="local",
        k_default=DEFAULT_K,
    )

    df = evaluator.evaluate_dataset(
        test_set=test_set,
        k=None,
        use_judge=True,
    )

    out_dir.mkdir(exist_ok=True, parents=True)
    df.to_csv(out_dir / "local_eval_full_with_judge.csv", index=False)
    return df


def run_cloud_full(out_dir: Path) -> pd.DataFrame:
    """Cloud Groq + Qdrant – pełna ewaluacja za jednym strzałem."""
    test_set = build_test_set()

    cloud_assistant = QuantLibCloudAssistant(
        groq_model="llama-3.1-8b-instant",
        temperature=0.0,
        k_default=DEFAULT_K,
    )

    judge_llm = create_groq_llm(
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )

    evaluator = QuantLibRAGEvaluator(
        assistant=cloud_assistant,
        judge_llm=judge_llm,
        backend_name="cloud",
        k_default=DEFAULT_K,
    )

    df = evaluator.evaluate_dataset(
        test_set=test_set,
        k=None,
        use_judge=True,
    )

    out_dir.mkdir(exist_ok=True, parents=True)
    df.to_csv(out_dir / "cloud_eval_full_with_judge.csv", index=False)
    return df


# ---------- CLI ----------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run QuantLib RAG evaluation (local/cloud).",
    )
    parser.add_argument(
        "--mode",
        choices=["local-phase1", "local-full", "cloud-full", "all"],
        default="all",
        help="What to run: local-phase1 (no judge), local-full, cloud-full, or all.",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="eval_results",
        help="Directory to store CSV results.",
    )

    args = parser.parse_args()
    out_dir = Path(args.out_dir)

    if args.mode in ("local-phase1", "all"):
        print(">> Running LOCAL phase1 (no judge)...")
        df_local_phase1 = run_local_phase1(out_dir)
        print(df_local_phase1.head())

    if args.mode in ("local-full", "all"):
        print(">> Running LOCAL full (with judge)...")
        df_local_full = run_local_full(out_dir)
        print(df_local_full.head())

    if args.mode in ("cloud-full", "all"):
        print(">> Running CLOUD full (with judge)...")
        df_cloud_full = run_cloud_full(out_dir)
        print(df_cloud_full.head())

    # jeśli chcesz od razu złożyć wspólny plik:
    if args.mode == "all":
        local_full_csv = out_dir / "local_eval_full_with_judge.csv"
        cloud_full_csv = out_dir / "cloud_eval_full_with_judge.csv"
        if local_full_csv.exists() and cloud_full_csv.exists():
            df_local = pd.read_csv(local_full_csv)
            df_cloud = pd.read_csv(cloud_full_csv)
            df_local["backend"] = "local"
            df_cloud["backend"] = "cloud"
            df_all = pd.concat([df_local, df_cloud], ignore_index=True)
            df_all.to_csv(out_dir / "all_eval_full.csv", index=False)
            print(">> Saved combined results to all_eval_full.csv")


if __name__ == "__main__":
    main()
