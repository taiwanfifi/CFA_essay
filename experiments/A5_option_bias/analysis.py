"""Post-hoc analysis for A5 option bias results."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from experiments.shared.evaluation import mcnemar_test


def load_results(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def analyze_bias_patterns(results: List[Dict]) -> Dict[str, Any]:
    """Analyze patterns in option-biased questions."""
    biased = [r for r in results if r.get("option_biased")]
    not_biased = [r for r in results if not r.get("option_biased")]

    # Breakdown by correct answer letter
    bias_by_answer = {}
    for r in biased:
        letter = r.get("correct_answer", "?")
        bias_by_answer[letter] = bias_by_answer.get(letter, 0) + 1

    return {
        "n_biased": len(biased),
        "n_total": len(results),
        "bias_rate": round(len(biased) / len(results), 4) if results else 0,
        "bias_by_correct_answer": bias_by_answer,
        "biased_question_ids": [r["question_id"] for r in biased],
    }


def compare_runs(run_paths: List[str]) -> None:
    """Compare option bias across multiple runs (e.g., different models)."""
    print(f"\n{'Model':<20} {'Acc(MCQ)':<10} {'Acc(Open)':<10} {'Bias':<8} {'Biased/N':<10} {'p-value':<8}")
    print("-" * 66)

    for path in run_paths:
        data = load_results(path)
        meta = data.get("metadata", {})
        summary = data.get("summary", {})
        model = meta.get("model", "?")
        acc_w = summary.get("accuracy_with_options", 0)
        acc_wo = summary.get("accuracy_without_options", 0)
        bias = summary.get("option_bias", 0)
        n_biased = summary.get("n_biased_questions", 0)
        n = meta.get("n_questions", 0)
        p_val = summary.get("mcnemar_test", {}).get("p_value", 1.0)

        print(f"{model:<20} {acc_w:<10.1%} {acc_wo:<10.1%} {bias:<+8.1%} {n_biased}/{n:<7} {p_val:<8.4f}")


def main():
    parser = argparse.ArgumentParser(description="A5: Analyze option bias results")
    parser.add_argument("--input", required=True, nargs="+", help="Result JSON file(s)")
    args = parser.parse_args()

    if len(args.input) == 1:
        data = load_results(args.input[0])
        results = data.get("results", [])
        analysis = analyze_bias_patterns(results)

        print(f"\nOption Bias Analysis")
        print(f"  Total questions:   {analysis['n_total']}")
        print(f"  Biased questions:  {analysis['n_biased']}")
        print(f"  Bias rate:         {analysis['bias_rate']:.1%}")
        print(f"\n  Bias by correct answer:")
        for letter, count in sorted(analysis["bias_by_correct_answer"].items()):
            print(f"    {letter}: {count}")
        print(f"\n  Biased question IDs: {analysis['biased_question_ids']}")
    else:
        compare_runs(args.input)


if __name__ == "__main__":
    main()
