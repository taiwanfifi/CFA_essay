"""Post-hoc analysis for I1 counterfactual results."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def load_results(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def memorization_analysis(data: Dict[str, Any]) -> None:
    """Analyze memorization patterns."""
    summary = data.get("summary", {})
    results = data.get("results", [])

    print(f"\nMemorization Analysis")
    print(f"  Original accuracy:    {summary.get('accuracy_original', 0):.1%}")
    print(f"  Robust accuracy:      {summary.get('robust_accuracy', 0):.1%}")
    print(f"  Memorization suspect: {summary.get('memorization_suspect', 0):+.1%}")

    for level, ls in summary.get("perturbation_levels", {}).items():
        print(f"\n  Level {level}:")
        print(f"    Valid perturbations: {ls.get('n_valid', 0)}")
        print(f"    Accuracy:            {ls.get('accuracy', 0):.1%}")
        print(f"    Memorization gap:    {ls.get('memorization_gap', 0):+.1%}")


def find_memorized_questions(data: Dict[str, Any]) -> List[str]:
    """Find questions where original was correct but perturbation was wrong.

    These are memorization suspects.
    """
    suspects = []
    for r in data.get("results", []):
        if not r.get("original", {}).get("correct"):
            continue
        for p in r.get("perturbations", []):
            if p.get("valid") and not p.get("correct"):
                suspects.append(r["question_id"])
                break

    return suspects


def consistency_analysis(data: Dict[str, Any]) -> None:
    """Analyze answer consistency across original and perturbations."""
    results = data.get("results", [])

    categories = {
        "robust_correct": 0,     # Correct on all
        "memorized": 0,          # Original correct, perturbed wrong
        "robust_incorrect": 0,   # Wrong on all
        "improved": 0,           # Original wrong, perturbed correct
    }

    for r in results:
        orig = r.get("original", {}).get("correct", False)
        perts = r.get("perturbations", [])
        valid_perts = [p for p in perts if p.get("valid")]

        if not valid_perts:
            continue

        any_pert_correct = any(p.get("correct") for p in valid_perts)
        all_pert_correct = all(p.get("correct") for p in valid_perts)

        if orig and all_pert_correct:
            categories["robust_correct"] += 1
        elif orig and not all_pert_correct:
            categories["memorized"] += 1
        elif not orig and any_pert_correct:
            categories["improved"] += 1
        else:
            categories["robust_incorrect"] += 1

    total = sum(categories.values())
    print(f"\nConsistency Analysis (n={total})")
    for cat, count in categories.items():
        rate = count / total if total else 0
        print(f"  {cat:<20}: {count} ({rate:.1%})")


def main():
    parser = argparse.ArgumentParser(description="I1: Analyze counterfactual results")
    parser.add_argument("--input", required=True, nargs="+", help="Result JSON file(s)")
    args = parser.parse_args()

    for path in args.input:
        data = load_results(path)
        model = data.get("metadata", {}).get("model", "?")
        print(f"\n{'='*60}")
        print(f"Model: {model}")
        print(f"{'='*60}")

        memorization_analysis(data)
        consistency_analysis(data)

        suspects = find_memorized_questions(data)
        if suspects:
            print(f"\n  Memorization suspects ({len(suspects)} questions):")
            for qid in suspects[:10]:
                print(f"    {qid}")


if __name__ == "__main__":
    main()
