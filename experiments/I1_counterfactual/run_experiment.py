"""I1 Counterfactual Testing: Detect memorization via numerical perturbation.

Usage:
    python -m experiments.I1_counterfactual.run_experiment \
        --dataset easy --limit 5 --model gpt-4o-mini --perturbation-levels 1
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.data_loader import load_dataset
from experiments.shared.llm_client import LLMClient
from experiments.shared.prompts import extract_answer, extract_numerical_answer
from experiments.shared.evaluation import tolerance_match

from .config import MCQ_SYSTEM, OPEN_SYSTEM
from .perturb import generate_perturbation

RESULTS_DIR = Path(__file__).parent / "results"


def answer_question(client: LLMClient, query: str, is_mcq: bool = True) -> dict:
    """Get the model's answer to a question."""
    system = MCQ_SYSTEM if is_mcq else OPEN_SYSTEM
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": query},
    ]
    response = client.chat(messages, temperature=0.0, max_tokens=2000)

    answer = extract_answer(response.content) if is_mcq else None
    numerical = extract_numerical_answer(response.content)

    return {
        "answer_letter": answer,
        "answer_numerical": numerical,
        "response": response.content[:500],
        "tokens": response.prompt_tokens + response.completion_tokens,
    }


def check_correct(model_result: dict, gold_answer: str) -> bool:
    """Check if the model's answer matches the gold answer."""
    # Letter match (MCQ)
    if model_result["answer_letter"] and model_result["answer_letter"] == gold_answer.strip().upper():
        return True

    # Numerical match
    gold_num = extract_numerical_answer(gold_answer)
    if model_result["answer_numerical"] is not None and gold_num is not None and gold_num != 0:
        return tolerance_match(model_result["answer_numerical"], gold_num, tol=0.05)

    return False


def run(args):
    """Main experiment runner."""
    if args.model not in MODEL_REGISTRY:
        print(f"Unknown model: {args.model}. Available: {list(MODEL_REGISTRY.keys())}")
        sys.exit(1)

    config = MODEL_REGISTRY[args.model]
    client = LLMClient(config)
    perturb_client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    levels = [int(x) for x in args.perturbation_levels]
    questions = load_dataset(args.dataset, args.limit)

    print(f"I1 Counterfactual Experiment")
    print(f"  Model: {args.model}")
    print(f"  Dataset: {args.dataset} ({len(questions)} questions)")
    print(f"  Perturbation levels: {levels}")
    print()

    results = []
    for i, q in enumerate(questions):
        print(f"  [{i+1}/{len(questions)}] {q['id']}...", end=" ", flush=True)

        # Answer original question
        orig_result = answer_question(client, q["query"])
        orig_correct = check_correct(orig_result, q["answer"])

        entry = {
            "question_id": q["id"],
            "correct_answer": q["answer"],
            "original": {
                "answer": orig_result["answer_letter"],
                "correct": orig_correct,
            },
            "perturbations": [],
        }

        status_parts = [f"orig={'✓' if orig_correct else '✗'}"]

        # Generate and test perturbations
        for level in levels:
            perturbation = generate_perturbation(q, level, perturb_client)

            if not perturbation["valid"]:
                entry["perturbations"].append({
                    "level": level,
                    "valid": False,
                    "reason": "generation_failed",
                })
                status_parts.append(f"L{level}=FAIL")
                continue

            # Answer perturbed question
            pert_result = answer_question(
                client, perturbation["perturbed_question"],
                is_mcq=bool(perturbation["perturbed_answer"].strip().upper() in "ABC"),
            )
            pert_correct = check_correct(pert_result, perturbation["perturbed_answer"])

            entry["perturbations"].append({
                "level": level,
                "valid": True,
                "perturbed_answer": perturbation["perturbed_answer"],
                "changes_made": perturbation["changes_made"],
                "model_answer": pert_result["answer_letter"] or str(pert_result["answer_numerical"]),
                "correct": pert_correct,
            })
            status_parts.append(f"L{level}={'✓' if pert_correct else '✗'}")

        results.append(entry)
        print(" ".join(status_parts))

    # Compute summary
    n = len(results)
    acc_original = sum(1 for r in results if r["original"]["correct"]) / n if n else 0

    level_summaries = {}
    for level in levels:
        valid_perts = []
        for r in results:
            for p in r["perturbations"]:
                if p.get("level") == level and p.get("valid"):
                    valid_perts.append(p)

        if valid_perts:
            acc_pert = sum(1 for p in valid_perts if p["correct"]) / len(valid_perts)
            level_summaries[str(level)] = {
                "n_valid": len(valid_perts),
                "accuracy": round(acc_pert, 4),
                "memorization_gap": round(acc_original - acc_pert, 4),
            }

    # Robust accuracy: correct on original AND all perturbations
    robust_count = 0
    for r in results:
        if not r["original"]["correct"]:
            continue
        all_pert_correct = all(
            p.get("correct", False)
            for p in r["perturbations"]
            if p.get("valid")
        )
        if all_pert_correct and r["perturbations"]:
            robust_count += 1
    robust_accuracy = robust_count / n if n else 0

    summary = {
        "accuracy_original": round(acc_original, 4),
        "perturbation_levels": level_summaries,
        "robust_accuracy": round(robust_accuracy, 4),
        "memorization_suspect": round(acc_original - robust_accuracy, 4),
    }

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = RESULTS_DIR / f"run_{timestamp}"
    output_dir.mkdir()

    output = {
        "metadata": {
            "experiment": "I1_counterfactual",
            "model": args.model,
            "dataset": args.dataset,
            "n_questions": n,
            "perturbation_levels": levels,
            "timestamp": timestamp,
        },
        "summary": summary,
        "results": results,
    }

    output_path = output_dir / "results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"  Original accuracy:    {acc_original:.1%}")
    for level, ls in level_summaries.items():
        print(f"  Level {level} accuracy:      {ls['accuracy']:.1%} "
              f"(gap={ls['memorization_gap']:+.1%}, n={ls['n_valid']})")
    print(f"  Robust accuracy:      {robust_accuracy:.1%}")
    print(f"  Memorization suspect: {acc_original - robust_accuracy:+.1%}")
    print(f"  Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="I1: Counterfactual Experiment")
    parser.add_argument("--dataset", default="easy", choices=["easy", "challenge", "both"])
    parser.add_argument("--limit", type=int, default=0, help="Max questions (0=all)")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to test")
    parser.add_argument(
        "--perturbation-levels", nargs="+", default=["1"],
        help="Perturbation levels to test (1, 2, 3)",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
