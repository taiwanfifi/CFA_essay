"""Post-hoc analysis for I3 noise experiment results."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def load_results(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def analyze_nsi_by_noise_type(data: Dict[str, Any]) -> None:
    """Print NSI breakdown by noise type."""
    summary = data.get("summary", {})
    noise_results = summary.get("noise_results", {})

    print(f"\nNoise Sensitivity Index (NSI) Analysis")
    print(f"  Clean accuracy: {summary.get('accuracy_clean', 0):.1%}")
    print(f"  Intensity: {summary.get('intensity', '?')}")
    print()
    print(f"  {'Type':<6} {'Name':<25} {'Acc':<8} {'NSI':<8} {'Flipped':<8}")
    print(f"  {'-'*55}")
    for nt, ns in noise_results.items():
        print(f"  {nt:<6} {ns['noise_type_name']:<25} "
              f"{ns['accuracy']:.1%}   {ns['nsi']:.3f}   {ns['n_flipped']}")


def find_most_vulnerable_questions(data: Dict[str, Any]) -> List[str]:
    """Find questions that flipped across the most noise types."""
    results = data.get("results", [])
    vuln = []
    for r in results:
        n_flipped = sum(
            1 for nt_result in r.get("noisy_results", {}).values()
            if nt_result.get("flipped")
        )
        if n_flipped > 0:
            vuln.append((r["question_id"], n_flipped))
    vuln.sort(key=lambda x: x[1], reverse=True)
    return vuln


def dose_response_analysis(run_paths: List[str]) -> None:
    """Compare NSI across runs with different intensities."""
    print(f"\nDose-Response Analysis")
    print(f"  {'Intensity':<10} {'Type':<6} {'NSI':<8} {'Acc(noisy)':<10}")
    print(f"  {'-'*35}")

    for path in sorted(run_paths):
        data = load_results(path)
        intensity = data.get("metadata", {}).get("intensity", "?")
        for nt, ns in data.get("summary", {}).get("noise_results", {}).items():
            print(f"  {intensity:<10} {nt:<6} {ns['nsi']:.3f}   {ns['accuracy']:.1%}")


def main():
    parser = argparse.ArgumentParser(description="I3: Analyze noise experiment results")
    parser.add_argument("--input", required=True, nargs="+", help="Result JSON file(s)")
    args = parser.parse_args()

    if len(args.input) == 1:
        data = load_results(args.input[0])
        analyze_nsi_by_noise_type(data)

        vuln = find_most_vulnerable_questions(data)
        if vuln:
            print(f"\n  Most vulnerable questions:")
            for qid, n_flipped in vuln[:10]:
                print(f"    {qid}: flipped in {n_flipped} noise type(s)")
    else:
        dose_response_analysis(args.input)


if __name__ == "__main__":
    main()
