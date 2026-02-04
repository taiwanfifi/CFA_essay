"""Post-hoc analysis for I2 behavioral biases results."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def load_results(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def bias_radar_data(data: Dict[str, Any]) -> None:
    """Print bias scores by type (data for radar chart visualization)."""
    summary = data.get("summary", {})
    by_type = summary.get("by_bias_type", {})

    print(f"\nBias Radar (scores by type)")
    print(f"  0.0 = fully rational, 1.0 = fully biased")
    print()
    print(f"  {'Bias Type':<22} {'Bias Score':<12} {'Neutral':<12} {'Debiasing':<12}")
    print(f"  {'-'*58}")
    for bt, ts in sorted(by_type.items(), key=lambda x: x[1]["avg_bias_score"], reverse=True):
        print(f"  {bt:<22} {ts['avg_bias_score']:<12.3f} "
              f"{ts['avg_neutral_score']:<12.3f} "
              f"{ts['avg_debiasing_effect']:<+12.3f}")


def most_biased_scenarios(data: Dict[str, Any]) -> None:
    """Find scenarios where the model showed strongest bias."""
    results = data.get("results", [])
    sorted_results = sorted(results, key=lambda x: x.get("bias_version_score", 0), reverse=True)

    print(f"\nMost Biased Scenarios (top 5)")
    for r in sorted_results[:5]:
        print(f"  {r['scenario_id']} ({r['bias_type']}): "
              f"score={r['bias_version_score']:.2f} | "
              f"chose: {r.get('bias_chosen', '?')}")


def debiasing_analysis(data: Dict[str, Any]) -> None:
    """Analyze effectiveness of neutral framing as debiasing."""
    results = data.get("results", [])

    effective = sum(1 for r in results if r.get("debiasing_effect", 0) > 0.1)
    no_effect = sum(1 for r in results if abs(r.get("debiasing_effect", 0)) <= 0.1)
    backfired = sum(1 for r in results if r.get("debiasing_effect", 0) < -0.1)

    print(f"\nDebiasing Effectiveness (neutral framing)")
    print(f"  Effective (bias reduced >0.1):  {effective}/{len(results)}")
    print(f"  No effect (|change| ≤ 0.1):     {no_effect}/{len(results)}")
    print(f"  Backfired (bias increased):      {backfired}/{len(results)}")


def compare_models(run_paths: List[str]) -> None:
    """Compare bias across models."""
    print(f"\n{'Model':<20} {'Avg Bias':<10} {'Avg Neutral':<12} {'Debiasing':<10}")
    print("-" * 52)

    for path in run_paths:
        data = load_results(path)
        model = data.get("metadata", {}).get("model", "?")
        summary = data.get("summary", {})
        print(f"{model:<20} {summary.get('avg_bias_score', 0):<10.3f} "
              f"{summary.get('avg_neutral_score', 0):<12.3f} "
              f"{summary.get('avg_debiasing_effect', 0):<+10.3f}")


def main():
    parser = argparse.ArgumentParser(description="I2: Analyze behavioral bias results")
    parser.add_argument("--input", required=True, nargs="+", help="Result JSON file(s)")
    args = parser.parse_args()

    if len(args.input) == 1:
        data = load_results(args.input[0])
        bias_radar_data(data)
        most_biased_scenarios(data)
        debiasing_analysis(data)
    else:
        compare_models(args.input)


if __name__ == "__main__":
    main()
