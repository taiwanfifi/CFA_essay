#!/usr/bin/env python3
"""
Main CLI runner for LLM confidence calibration experiments.

Usage:
    # Smoke test (5 questions, 1 model, 1 method)
    python -m experiments.calibration.run_calibration \
        --models gpt-4o-mini --methods verbalized --dataset challenge --limit 5

    # Full pilot
    python -m experiments.calibration.run_calibration \
        --models gpt-4o-mini qwen3:32b llama3.1:8b deepseek-r1:14b \
        --methods verbalized self_consistency logit ensemble \
        --dataset challenge
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from experiments.cfa_agent.evaluate import load_dataset
from experiments.calibration.config import (
    CALIBRATION_BINS,
    MODEL_REGISTRY,
    SELF_CONSISTENCY_K,
    VALID_ANSWERS,
    ModelConfig,
)
from experiments.calibration.llm_client import LLMClient
from experiments.calibration.confidence import (
    ConfidenceResult,
    ensemble_disagreement,
    logit_confidence,
    self_consistency,
    verbalized_confidence,
)
from experiments.calibration.metrics import compute_all_metrics
from experiments.calibration.visualize import (
    plot_confidence_histogram,
    plot_coverage_accuracy_curve,
    plot_reliability_diagram,
)

CHECKPOINT_INTERVAL = 10  # save every N results


# ---------------------------------------------------------------------------
# Checkpoint helpers
# ---------------------------------------------------------------------------

def _checkpoint_path(output_dir: Path) -> Path:
    return output_dir / "checkpoint.json"


def _load_checkpoint(output_dir: Path) -> Dict[str, Any]:
    """Load checkpoint if it exists, otherwise return empty state."""
    cp_path = _checkpoint_path(output_dir)
    if cp_path.exists():
        with open(cp_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"results": [], "completed_keys": []}


def _save_checkpoint(output_dir: Path, state: Dict[str, Any]):
    cp_path = _checkpoint_path(output_dir)
    with open(cp_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2, default=str)


def _result_key(model: str, method: str, question_id: str) -> str:
    return f"{model}|{method}|{question_id}"


# ---------------------------------------------------------------------------
# Run single method on a question
# ---------------------------------------------------------------------------

def run_single(
    client: LLMClient,
    method: str,
    question: str,
    question_id: str,
    correct_answer: str,
    all_clients: Optional[Dict[str, LLMClient]] = None,
    sc_k: int = SELF_CONSISTENCY_K,
) -> Dict[str, Any]:
    """Run one confidence method on one question, return serializable dict."""
    if method == "verbalized":
        result = verbalized_confidence(client, question)
    elif method == "self_consistency":
        result = self_consistency(client, question, k=sc_k)
    elif method == "logit":
        result = logit_confidence(client, question)
    elif method == "ensemble":
        if all_clients is None:
            raise ValueError("ensemble method requires all_clients dict")
        result = ensemble_disagreement(all_clients, question)
    else:
        raise ValueError(f"Unknown method: {method}")

    # Set correctness
    is_correct = (result.answer == correct_answer) if result.answer else False
    result.correct = is_correct

    return {
        "model": client.name if method != "ensemble" else "ensemble",
        "method": result.method,
        "question_id": question_id,
        "answer": result.answer,
        "correct_answer": correct_answer,
        "correct": is_correct,
        "confidence": result.confidence,
        "raw_response": result.raw_response,
        "metadata": result.metadata,
    }


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def run_calibration(
    model_names: List[str],
    methods: List[str],
    dataset_name: str,
    limit: int = 0,
    sc_k: int = SELF_CONSISTENCY_K,
    output_dir: Optional[Path] = None,
    no_viz: bool = False,
):
    """Run the full calibration experiment."""
    # Setup output
    if output_dir is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(__file__).parent / "results" / f"run_{ts}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load dataset
    print(f"Loading dataset: {dataset_name}" + (f" (limit={limit})" if limit else ""))
    questions = load_dataset(dataset_name, limit)
    print(f"Loaded {len(questions)} questions")

    # Initialize clients
    clients: Dict[str, LLMClient] = {}
    for name in model_names:
        if name not in MODEL_REGISTRY:
            print(f"WARNING: Unknown model '{name}', skipping")
            continue
        clients[name] = LLMClient(MODEL_REGISTRY[name])
    print(f"Models: {', '.join(clients.keys())}")
    print(f"Methods: {', '.join(methods)}")

    # Load checkpoint
    state = _load_checkpoint(output_dir)
    completed_keys = set(state["completed_keys"])
    all_results = state["results"]
    n_skipped = len(completed_keys)
    if n_skipped > 0:
        print(f"Resuming from checkpoint: {n_skipped} results already completed")

    t0 = time.time()
    n_since_save = 0

    # Separate ensemble from per-model methods
    per_model_methods = [m for m in methods if m != "ensemble"]
    run_ensemble = "ensemble" in methods

    # --- Per-model methods ---
    for model_name, client in clients.items():
        for method in per_model_methods:
            # Skip logit for models that don't support it
            if method == "logit" and not client.supports_logprobs:
                print(f"Skipping logit for {model_name} (no logprobs support)")
                continue

            print(f"\n--- {model_name} / {method} ({len(questions)} questions) ---")

            for item in questions:
                key = _result_key(model_name, method, item["id"])
                if key in completed_keys:
                    continue

                try:
                    result = run_single(
                        client=client,
                        method=method,
                        question=item["query"],
                        question_id=item["id"],
                        correct_answer=item["answer"],
                        sc_k=sc_k,
                    )
                except Exception as e:
                    print(f"  ERROR {item['id']}: {e}")
                    result = {
                        "model": model_name,
                        "method": method,
                        "question_id": item["id"],
                        "answer": None,
                        "correct_answer": item["answer"],
                        "correct": False,
                        "confidence": 0.0,
                        "raw_response": "",
                        "metadata": {"error": str(e)},
                    }

                all_results.append(result)
                completed_keys.add(key)
                n_since_save += 1

                # Progress
                status = "OK" if result["correct"] else "X "
                conf_str = f"{result['confidence']:.2f}"
                ans = result["answer"] or "?"
                print(f"  [{status}] {item['id']}: {ans} (conf={conf_str})")

                # Checkpoint
                if n_since_save >= CHECKPOINT_INTERVAL:
                    state["results"] = all_results
                    state["completed_keys"] = list(completed_keys)
                    _save_checkpoint(output_dir, state)
                    n_since_save = 0

    # --- Ensemble method ---
    if run_ensemble and len(clients) >= 2:
        print(f"\n--- ensemble ({len(questions)} questions, {len(clients)} models) ---")
        # Pick any client as the "primary" for the run_single interface
        primary_client = next(iter(clients.values()))

        for item in questions:
            key = _result_key("ensemble", "ensemble", item["id"])
            if key in completed_keys:
                continue

            try:
                result = run_single(
                    client=primary_client,
                    method="ensemble",
                    question=item["query"],
                    question_id=item["id"],
                    correct_answer=item["answer"],
                    all_clients=clients,
                )
            except Exception as e:
                print(f"  ERROR {item['id']}: {e}")
                result = {
                    "model": "ensemble",
                    "method": "ensemble",
                    "question_id": item["id"],
                    "answer": None,
                    "correct_answer": item["answer"],
                    "correct": False,
                    "confidence": 0.0,
                    "raw_response": "",
                    "metadata": {"error": str(e)},
                }

            all_results.append(result)
            completed_keys.add(key)
            n_since_save += 1

            status = "OK" if result["correct"] else "X "
            conf_str = f"{result['confidence']:.2f}"
            ans = result["answer"] or "?"
            print(f"  [{status}] {item['id']}: {ans} (conf={conf_str})")

            if n_since_save >= CHECKPOINT_INTERVAL:
                state["results"] = all_results
                state["completed_keys"] = list(completed_keys)
                _save_checkpoint(output_dir, state)
                n_since_save = 0

    elif run_ensemble and len(clients) < 2:
        print("WARNING: Ensemble requires at least 2 models, skipping")

    # Final save
    state["results"] = all_results
    state["completed_keys"] = list(completed_keys)
    _save_checkpoint(output_dir, state)

    total_elapsed = time.time() - t0

    # ---------------------------------------------------------------------------
    # Compute metrics per (model, method) combo
    # ---------------------------------------------------------------------------

    print("\n" + "=" * 90)
    print("CALIBRATION RESULTS")
    print("=" * 90)

    metrics_all: Dict[str, Dict[str, Any]] = {}
    coverage_curves: Dict[str, Any] = {}

    # Group results by (model, method)
    groups: Dict[str, List[Dict]] = {}
    for r in all_results:
        gkey = f"{r['model']}|{r['method']}"
        groups.setdefault(gkey, []).append(r)

    header = f"{'Model + Method':<35} | {'ECE':>7} | {'MCE':>7} | {'Brier':>7} | {'AUROC':>7} | {'Acc':>7} | {'AvgConf':>7} | {'N':>4}"
    print(header)
    print("-" * len(header))

    for gkey, items in sorted(groups.items()):
        confidences = [r["confidence"] for r in items]
        correctness = [r["correct"] for r in items]
        m = compute_all_metrics(confidences, correctness, CALIBRATION_BINS)
        metrics_all[gkey] = m
        coverage_curves[gkey] = m["coverage_accuracy_curve"]

        auroc_str = f"{m['auroc']:.4f}" if m["auroc"] is not None else "  N/A "
        print(f"{gkey:<35} | {m['ece']:>7.4f} | {m['mce']:>7.4f} | "
              f"{m['brier_score']:>7.4f} | {auroc_str:>7} | "
              f"{m['accuracy']:>6.1%} | {m['avg_confidence']:>7.4f} | {m['n']:>4}")

    print("=" * len(header))
    print(f"Total wall time: {total_elapsed:.1f}s")
    print(f"Total results: {len(all_results)}")

    # ---------------------------------------------------------------------------
    # Save final results
    # ---------------------------------------------------------------------------

    output_data = {
        "metadata": {
            "dataset": dataset_name,
            "limit": limit,
            "models": model_names,
            "methods": methods,
            "sc_k": sc_k,
            "n_questions": len(questions),
            "total_results": len(all_results),
            "total_elapsed_seconds": round(total_elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        },
        "metrics": metrics_all,
        "results": all_results,
    }

    results_path = output_dir / "results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nResults saved to: {results_path}")

    # ---------------------------------------------------------------------------
    # Visualizations
    # ---------------------------------------------------------------------------

    if not no_viz:
        print("\nGenerating visualizations...")
        for gkey, m in metrics_all.items():
            safe_name = gkey.replace("|", "_").replace(":", "-")

            # Reliability diagram
            path = plot_reliability_diagram(
                m["bins"], m["ece"],
                title=f"Reliability: {gkey}",
                output_path=str(output_dir / f"reliability_{safe_name}.png"),
            )
            print(f"  Saved: {path}")

            # Confidence histogram
            confidences = [r["confidence"] for r in groups[gkey]]
            path = plot_confidence_histogram(
                confidences,
                title=f"Confidence Distribution: {gkey}",
                output_path=str(output_dir / f"histogram_{safe_name}.png"),
            )
            print(f"  Saved: {path}")

        # Coverage-accuracy curves (all methods on one plot per model)
        models_in_results = set()
        for gkey in groups:
            model_name = gkey.split("|")[0]
            models_in_results.add(model_name)

        for model_name in models_in_results:
            model_curves = {
                gkey.split("|")[1]: coverage_curves[gkey]
                for gkey in coverage_curves
                if gkey.startswith(model_name + "|")
            }
            if model_curves:
                safe_model = model_name.replace(":", "-")
                path = plot_coverage_accuracy_curve(
                    model_curves,
                    title=f"Coverage-Accuracy: {model_name}",
                    output_path=str(output_dir / f"coverage_{safe_model}.png"),
                )
                print(f"  Saved: {path}")

    # Cleanup checkpoint
    cp_path = _checkpoint_path(output_dir)
    if cp_path.exists():
        cp_path.unlink()
        print("Checkpoint cleaned up.")

    print("Done.")
    return output_data


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="LLM Confidence Calibration Experiment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Smoke test
  python -m experiments.calibration.run_calibration \\
    --models gpt-4o-mini --methods verbalized --dataset challenge --limit 5

  # Full pilot (all 4 models, all 4 methods)
  python -m experiments.calibration.run_calibration \\
    --models gpt-4o-mini qwen3:32b llama3.1:8b deepseek-r1:14b \\
    --methods verbalized self_consistency logit ensemble \\
    --dataset challenge
""",
    )
    parser.add_argument(
        "--models", nargs="+",
        default=["gpt-4o-mini"],
        choices=list(MODEL_REGISTRY.keys()),
        help="Models to evaluate.",
    )
    parser.add_argument(
        "--methods", nargs="+",
        default=["verbalized"],
        choices=["verbalized", "self_consistency", "logit", "ensemble"],
        help="Confidence estimation methods.",
    )
    parser.add_argument(
        "--dataset", type=str, default="challenge",
        choices=["challenge", "easy", "both"],
        help="Dataset to evaluate on.",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Max questions per dataset (0 = all).",
    )
    parser.add_argument(
        "--sc-k", type=int, default=SELF_CONSISTENCY_K,
        help=f"Number of samples for self-consistency (default: {SELF_CONSISTENCY_K}).",
    )
    parser.add_argument(
        "--output-dir", type=str, default="",
        help="Output directory (default: auto-generated under results/).",
    )
    parser.add_argument(
        "--no-viz", action="store_true",
        help="Skip generating visualizations.",
    )
    args = parser.parse_args()

    # Validate: OpenAI API key needed for gpt-4o-mini
    if "gpt-4o-mini" in args.models and not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set. Export it or add to .env file.")
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else None

    run_calibration(
        model_names=args.models,
        methods=args.methods,
        dataset_name=args.dataset,
        limit=args.limit,
        sc_k=args.sc_k,
        output_dir=output_dir,
        no_viz=args.no_viz,
    )


if __name__ == "__main__":
    main()
