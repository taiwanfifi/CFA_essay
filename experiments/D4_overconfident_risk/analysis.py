"""Post-hoc analysis for D4 overconfident risk results."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def load_results(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def risk_matrix(data: Dict[str, Any]) -> None:
    """Print risk matrix: severity × confidence band."""
    errors = data.get("classified_errors", [])
    if not errors:
        print("No classified errors found.")
        return

    # Confidence bands
    bands = {"90-100%": (0.9, 1.01), "80-90%": (0.8, 0.9), "70-80%": (0.7, 0.8)}
    severities = ["critical", "high", "medium", "low", "unknown"]

    matrix = {sev: {band: 0 for band in bands} for sev in severities}
    for entry in errors:
        conf = entry.get("confidence", 0)
        sev = entry.get("risk_classification", {}).get("risk_severity", "unknown")
        for band_name, (lo, hi) in bands.items():
            if lo <= conf < hi:
                matrix[sev][band_name] += 1
                break

    print(f"\nRisk Matrix (Severity × Confidence Band)")
    print(f"  {'Severity':<12}", end="")
    for band in bands:
        print(f" {band:<10}", end="")
    print()
    print(f"  {'-'*42}")
    for sev in severities:
        row = matrix[sev]
        if any(v > 0 for v in row.values()):
            print(f"  {sev:<12}", end="")
            for band in bands:
                print(f" {row[band]:<10}", end="")
            print()


def analyze_error_mechanisms(data: Dict[str, Any]) -> None:
    """Summarize error mechanisms from classified errors."""
    errors = data.get("classified_errors", [])
    mechanisms = {}
    for entry in errors:
        mech = entry.get("risk_classification", {}).get("error_mechanism", "unknown")
        if mech:
            # Truncate for display
            key = mech[:60]
            mechanisms[key] = mechanisms.get(key, 0) + 1

    print(f"\nError Mechanisms (top 10):")
    for mech, count in sorted(mechanisms.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  [{count}] {mech}")


def main():
    parser = argparse.ArgumentParser(description="D4: Analyze overconfident risk results")
    parser.add_argument("--input", required=True, help="Result JSON file")
    args = parser.parse_args()

    data = load_results(args.input)

    summary = data.get("summary", {})
    print(f"\nD4 Overconfident Risk Analysis")
    print(f"  Overconfident errors:      {summary.get('total_overconfident_errors', 0)}")
    print(f"  Classified:                {summary.get('classified_count', 0)}")
    print(f"  Avg confidence:            {summary.get('avg_confidence', 0):.1%}")
    print(f"  Collective hallucinations: {summary.get('collective_hallucinations', 0)}")

    print(f"\n  Severity distribution:")
    for sev, count in sorted(summary.get("severity_distribution", {}).items()):
        print(f"    {sev}: {count}")

    risk_matrix(data)
    analyze_error_mechanisms(data)

    # Collective hallucinations detail
    collective = data.get("collective_hallucinations", [])
    if collective:
        print(f"\nCollective Hallucinations ({len(collective)} questions):")
        for ch in collective[:5]:
            print(f"  {ch['question_id']}: {ch['n_models']} models, "
                  f"avg conf={ch['avg_confidence']:.1%}, "
                  f"models={ch['models']}")


if __name__ == "__main__":
    main()
