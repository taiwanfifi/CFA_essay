"""Post-hoc analysis for A1 open-ended benchmark results."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def load_results(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def level_distribution(data: Dict[str, Any]) -> None:
    """Print level A/B/C distribution."""
    summary = data.get("summary", {})
    dist = summary.get("level_distribution", {})
    rates = summary.get("level_rates", {})

    print(f"\nLevel Distribution")
    print(f"  Level A (Exact):       {dist.get('exact', 0)} ({rates.get('exact', 0):.1%})")
    print(f"  Level B (Directional): {dist.get('directional', 0)} ({rates.get('directional', 0):.1%})")
    print(f"  Level C (Incorrect):   {dist.get('incorrect', 0)} ({rates.get('incorrect', 0):.1%})")
    print(f"\n  Strict accuracy (A):   {summary.get('strict_accuracy', 0):.1%}")
    print(f"  Lenient accuracy (A+B): {summary.get('lenient_accuracy', 0):.1%}")


def error_analysis(data: Dict[str, Any]) -> None:
    """Analyze Level C errors by category."""
    results = data.get("results", [])
    errors = [r for r in results if r.get("level") == "incorrect"]

    if not errors:
        print("\nNo Level C errors to analyze.")
        return

    print(f"\nError Attribution (Level C, n={len(errors)})")
    cats = {}
    tool_fixable = 0
    for r in errors:
        attr = r.get("error_attribution", {})
        if attr:
            cat = attr.get("error_category", "unknown")
            cats[cat] = cats.get(cat, 0) + 1
            if attr.get("could_be_fixed_with_tools"):
                tool_fixable += 1

    for cat, count in sorted(cats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} ({count/len(errors):.0%})")

    print(f"\n  Tool-fixable errors: {tool_fixable}/{len(errors)} "
          f"({tool_fixable/len(errors):.0%})")


def auto_vs_judge_grading(data: Dict[str, Any]) -> None:
    """Show how many were auto-graded vs LLM-judged."""
    results = data.get("results", [])
    auto = sum(1 for r in results if r.get("evaluation", {}).get("auto_graded"))
    judge = len(results) - auto

    print(f"\nGrading Method")
    print(f"  Auto-graded (numerical): {auto}/{len(results)}")
    print(f"  LLM-judged (semantic):   {judge}/{len(results)}")


def compare_runs(run_paths: List[str]) -> None:
    """Compare across multiple models."""
    print(f"\n{'Model':<20} {'A(Exact)':<10} {'B(Dir.)':<10} {'C(Wrong)':<10} {'Strict':<8} {'Lenient':<8}")
    print("-" * 66)

    for path in run_paths:
        data = load_results(path)
        meta = data.get("metadata", {})
        summary = data.get("summary", {})
        model = meta.get("model", "?")
        rates = summary.get("level_rates", {})
        print(f"{model:<20} {rates.get('exact',0):<10.1%} {rates.get('directional',0):<10.1%} "
              f"{rates.get('incorrect',0):<10.1%} {summary.get('strict_accuracy',0):<8.1%} "
              f"{summary.get('lenient_accuracy',0):<8.1%}")


def main():
    parser = argparse.ArgumentParser(description="A1: Analyze open-ended benchmark results")
    parser.add_argument("--input", required=True, nargs="+", help="Result JSON file(s)")
    args = parser.parse_args()

    if len(args.input) == 1:
        data = load_results(args.input[0])
        level_distribution(data)
        error_analysis(data)
        auto_vs_judge_grading(data)
    else:
        compare_runs(args.input)


if __name__ == "__main__":
    main()
