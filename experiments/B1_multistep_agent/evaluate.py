#!/usr/bin/env python3
"""
CFA Agent Evaluation Runner.

Loads CFA exam datasets, runs zero_shot / cot / agent (and optional extras),
and outputs a comparison table + JSON results file.

Usage:
    python experiments/cfa_agent/evaluate.py --dataset challenge --limit 5
    python experiments/cfa_agent/evaluate.py --dataset easy --limit 50
    python experiments/cfa_agent/evaluate.py --dataset both --limit 50
    python experiments/cfa_agent/evaluate.py --dataset challenge --methods agent agent_verify
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv

load_dotenv()

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from experiments.cfa_agent.agent import METHODS, DEFAULT_MODEL
from tqdm import tqdm


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

DATASETS_DIR = PROJECT_ROOT / "datasets" / "FinEval"


def load_cfa_challenge(limit: int = 0) -> List[Dict[str, Any]]:
    """Load CFA-Challenge dataset (90 questions).

    Schema: {"query": str, "answer": str, "source": str}
    """
    path = DATASETS_DIR / "CFA_Challenge" / "data.json"
    if not path.exists():
        raise FileNotFoundError(f"CFA-Challenge data not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    items = []
    for i, entry in enumerate(raw):
        items.append({
            "id": f"challenge_{i}",
            "query": entry["query"],
            "answer": entry["answer"].strip().upper(),
            "dataset": "CFA_Challenge",
        })
    if limit > 0:
        items = items[:limit]
    return items


def load_cfa_easy(limit: int = 0) -> List[Dict[str, Any]]:
    """Load CFA-Easy dataset (1,032 questions).

    Schema: {"query": str, "answer": str, "text": str, "choices": list, "gold": int}
    """
    path = DATASETS_DIR / "CFA_Easy" / "data.json"
    if not path.exists():
        raise FileNotFoundError(f"CFA-Easy data not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    items = []
    for i, entry in enumerate(raw):
        items.append({
            "id": f"easy_{i}",
            "query": entry["query"],
            "answer": entry["answer"].strip().upper(),
            "dataset": "CFA_Easy",
        })
    if limit > 0:
        items = items[:limit]
    return items


def load_dataset(name: str, limit: int = 0) -> List[Dict[str, Any]]:
    """Load dataset by name."""
    if name == "challenge":
        return load_cfa_challenge(limit)
    elif name == "easy":
        return load_cfa_easy(limit)
    elif name == "both":
        challenge = load_cfa_challenge(limit)
        easy = load_cfa_easy(limit)
        return challenge + easy
    else:
        raise ValueError(f"Unknown dataset: {name}. Use 'challenge', 'easy', or 'both'.")


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate(
    questions: List[Dict[str, Any]],
    methods: List[str],
    model: str,
) -> List[Dict[str, Any]]:
    """Run all methods on all questions, return per-item results."""
    results = []

    for method_name in methods:
        method_fn = METHODS[method_name]
        print(f"\n--- Running: {method_name} ({len(questions)} questions) ---")

        for item in tqdm(questions, desc=method_name):
            try:
                result = method_fn(item["query"], model=model)
                result["question_id"] = item["id"]
                result["correct_answer"] = item["answer"]
                result["correct"] = (result["answer"] == item["answer"])
                result["dataset"] = item["dataset"]
                result["query"] = item["query"]
            except Exception as e:
                result = {
                    "method": method_name,
                    "question_id": item["id"],
                    "correct_answer": item["answer"],
                    "answer": None,
                    "correct": False,
                    "error": str(e),
                    "dataset": item["dataset"],
                    "query": item["query"],
                    "reasoning": "",
                    "turns": 0,
                    "tool_calls": [],
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "cost_usd": 0,
                    "elapsed_seconds": 0,
                    "model": model,
                }
                tqdm.write(f"  ERROR on {item['id']}: {e}")
            results.append(result)

    return results


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------

def print_summary(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Print a summary comparison table and return summary dict."""
    # Group by method
    by_method: Dict[str, List[Dict]] = {}
    for r in results:
        by_method.setdefault(r["method"], []).append(r)

    summary = {}
    header = f"{'Method':<20} | {'Accuracy':>8} | {'Avg Tokens':>10} | {'Avg Turns':>9} | {'Tool Calls':>10} | {'Cost':>8}"
    print("\n" + "=" * len(header))
    print(header)
    print("-" * len(header))

    for method, items in by_method.items():
        n = len(items)
        correct = sum(1 for r in items if r.get("correct"))
        acc = correct / n if n > 0 else 0
        avg_tokens = sum(r.get("total_tokens", 0) for r in items) / n if n > 0 else 0
        avg_turns = sum(r.get("turns", 0) for r in items) / n if n > 0 else 0
        total_tool_calls = sum(len(r.get("tool_calls", [])) for r in items)
        total_cost = sum(r.get("cost_usd", 0) for r in items)

        print(f"{method:<20} | {acc:>7.1%} | {avg_tokens:>10,.0f} | {avg_turns:>9.1f} | {total_tool_calls:>10} | ${total_cost:>6.2f}")

        summary[method] = {
            "n_questions": n,
            "n_correct": correct,
            "accuracy": round(acc, 4),
            "avg_tokens": round(avg_tokens, 1),
            "avg_turns": round(avg_turns, 2),
            "total_tool_calls": total_tool_calls,
            "total_cost_usd": round(total_cost, 4),
        }

    print("=" * len(header))
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="CFA Agent Evaluation")
    parser.add_argument("--dataset", type=str, default="challenge",
                        choices=["challenge", "easy", "both"],
                        help="Which dataset to evaluate on.")
    parser.add_argument("--limit", type=int, default=0,
                        help="Max questions per dataset (0 = all).")
    parser.add_argument("--methods", nargs="+", default=["zero_shot", "cot", "cot_verify", "structured"],
                        choices=list(METHODS.keys()),
                        help="Methods to run.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL,
                        help=f"OpenAI model to use (default: {DEFAULT_MODEL}).")
    parser.add_argument("--output", type=str, default="",
                        help="Output JSON path (default: auto-generated).")
    args = parser.parse_args()

    # Validate API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set. Export it or add to .env file.")
        sys.exit(1)

    # Load data
    print(f"Loading dataset: {args.dataset}" + (f" (limit={args.limit})" if args.limit else ""))
    questions = load_dataset(args.dataset, args.limit)
    print(f"Loaded {len(questions)} questions")

    # Run evaluation
    print(f"Methods: {', '.join(args.methods)}")
    print(f"Model: {args.model}")
    t0 = time.time()
    results = evaluate(questions, args.methods, args.model)
    total_elapsed = time.time() - t0

    # Summary
    summary = print_summary(results)
    print(f"\nTotal wall time: {total_elapsed:.1f}s")

    # Save results
    output_dir = PROJECT_ROOT / "experiments" / "cfa_agent" / "results"
    output_dir.mkdir(exist_ok=True)
    if args.output:
        output_path = Path(args.output)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"eval_{args.dataset}_{ts}.json"

    output_data = {
        "metadata": {
            "dataset": args.dataset,
            "limit": args.limit,
            "methods": args.methods,
            "model": args.model,
            "n_questions": len(questions),
            "total_elapsed_seconds": round(total_elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        },
        "summary": summary,
        "results": results,
    }

    # Clean tool_calls for JSON serialization (remove non-serializable items)
    for r in output_data["results"]:
        if "tool_calls" in r:
            cleaned = []
            for tc in r["tool_calls"]:
                cleaned.append({
                    "turn": tc.get("turn"),
                    "tool": tc.get("tool"),
                    "args": tc.get("args"),
                    "result": tc.get("result"),
                })
            r["tool_calls"] = cleaned

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2, default=str)

    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
