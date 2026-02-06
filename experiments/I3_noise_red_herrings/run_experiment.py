"""I3 Noise & Red Herrings: Measure LLM robustness to irrelevant information.

Usage:
    python -m experiments.I3_noise_red_herrings.run_experiment \
        --dataset easy --limit 5 --model gpt-4o-mini --noise-types N1
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.data_loader import load_dataset
from experiments.shared.llm_client import LLMClient
from experiments.shared.prompts import extract_answer

from .config import MCQ_SYSTEM, NOISE_TYPES
from .noise_injector import inject_noise, get_available_noise_types

RESULTS_DIR = Path(__file__).parent / "results"


def evaluate_question(client: LLMClient, query: str) -> dict:
    """Run a single question and extract the answer."""
    messages = [
        {"role": "system", "content": MCQ_SYSTEM},
        {"role": "user", "content": query},
    ]
    response = client.chat(messages, temperature=0.0, max_tokens=2000)
    answer = extract_answer(response.content)
    return {
        "answer": answer,
        "response": response.content[:500],
        "tokens": response.prompt_tokens + response.completion_tokens,
    }


def run(args):
    """Main experiment runner."""
    if args.model not in MODEL_REGISTRY:
        print(f"Unknown model: {args.model}. Available: {list(MODEL_REGISTRY.keys())}")
        sys.exit(1)

    config = MODEL_REGISTRY[args.model]
    client = LLMClient(config)

    noise_types = args.noise_types if args.noise_types else ["N1"]
    for nt in noise_types:
        if nt not in NOISE_TYPES:
            print(f"Unknown noise type: {nt}. Available: {list(NOISE_TYPES.keys())}")
            sys.exit(1)

    questions = load_dataset(args.dataset, args.limit)

    print(f"I3 Noise & Red Herrings Experiment")
    print(f"  Model: {args.model}")
    print(f"  Dataset: {args.dataset} ({len(questions)} questions)")
    print(f"  Noise types: {noise_types}")
    print(f"  Intensity: {args.intensity}")
    print()

    results = []
    for i, q in enumerate(questions):
        print(f"  [{i+1}/{len(questions)}] {q['id']}...", end=" ", flush=True)

        # Clean version
        clean_result = evaluate_question(client, q["query"])
        clean_correct = clean_result["answer"] == q["answer"]

        entry = {
            "question_id": q["id"],
            "correct_answer": q["answer"],
            "clean_answer": clean_result["answer"],
            "clean_correct": clean_correct,
            "noisy_results": {},
        }

        # Noisy versions
        status_parts = [f"clean={'✓' if clean_correct else '✗'}"]
        for nt in noise_types:
            noisy_query = inject_noise(
                q["query"],
                noise_type=nt,
                intensity=args.intensity,
                correct_answer=q["answer"],
                seed=hash(q["id"]) % 10000,
            )
            noisy_result = evaluate_question(client, noisy_query)
            noisy_correct = noisy_result["answer"] == q["answer"]

            entry["noisy_results"][nt] = {
                "answer": noisy_result["answer"],
                "correct": noisy_correct,
                "flipped": clean_correct and not noisy_correct,
            }
            status_parts.append(f"{nt}={'✓' if noisy_correct else '✗'}")

        results.append(entry)
        print(" ".join(status_parts))

    # Compute summary
    n = len(results)
    acc_clean = sum(1 for r in results if r["clean_correct"]) / n if n else 0

    noise_summary = {}
    for nt in noise_types:
        acc_noisy = sum(
            1 for r in results if r["noisy_results"][nt]["correct"]
        ) / n if n else 0
        n_flipped = sum(
            1 for r in results if r["noisy_results"][nt]["flipped"]
        )
        nsi = (acc_clean - acc_noisy) / acc_clean if acc_clean > 0 else 0

        noise_summary[nt] = {
            "noise_type_name": NOISE_TYPES[nt],
            "accuracy": round(acc_noisy, 4),
            "n_flipped": n_flipped,
            "nsi": round(nsi, 4),  # Noise Sensitivity Index
        }

    summary = {
        "accuracy_clean": round(acc_clean, 4),
        "noise_results": noise_summary,
        "intensity": args.intensity,
    }

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = RESULTS_DIR / f"run_{timestamp}"
    output_dir.mkdir()

    output = {
        "metadata": {
            "experiment": "I3_noise_red_herrings",
            "model": args.model,
            "dataset": args.dataset,
            "n_questions": n,
            "noise_types": noise_types,
            "intensity": args.intensity,
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
    print(f"  Clean accuracy:  {acc_clean:.1%}")
    for nt, ns in noise_summary.items():
        print(f"  {nt} ({ns['noise_type_name']}):")
        print(f"    Noisy accuracy:  {ns['accuracy']:.1%}")
        print(f"    Flipped:         {ns['n_flipped']}/{n}")
        print(f"    NSI:             {ns['nsi']:.3f}")
    print(f"  Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="I3: Noise & Red Herrings Experiment")
    parser.add_argument("--dataset", default="easy", choices=["easy", "challenge", "both"])
    parser.add_argument("--limit", type=int, default=0, help="Max questions (0=all)")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to test")
    parser.add_argument(
        "--noise-types", nargs="+", default=["N1"],
        help="Noise types to test (N1, N2, N3, N4)",
    )
    parser.add_argument("--intensity", type=int, default=2, help="Noise intensity (1-4)")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
