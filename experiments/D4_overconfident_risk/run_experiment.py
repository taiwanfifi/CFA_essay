"""D4 Overconfident Risk: Classify high-confidence errors by financial risk.

Usage:
    python -m experiments.D4_overconfident_risk.run_experiment \
        --input experiments/D1_confidence_calibration/results/run_*/results.json \
        --confidence-threshold 0.8
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.llm_client import LLMClient

from .config import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    RISK_CLASSIFY_SYSTEM,
    RISK_CLASSIFY_USER,
)
from .filter import (
    load_d1_results,
    filter_overconfident_errors,
    detect_collective_hallucination,
)

RESULTS_DIR = Path(__file__).parent / "results"


def classify_risk(client: LLMClient, entry: dict) -> dict:
    """Use LLM to classify the financial risk of an overconfident error."""
    messages = [
        {"role": "system", "content": RISK_CLASSIFY_SYSTEM},
        {"role": "user", "content": RISK_CLASSIFY_USER.format(
            question=entry.get("question", "")[:1000],
            correct_answer=entry.get("correct_answer", ""),
            model_answer=entry.get("model_answer", ""),
            confidence=entry.get("confidence", 0),
            reasoning=entry.get("reasoning", "")[:500],
        )},
    ]
    response = client.chat(messages, temperature=0.0, max_tokens=400)

    try:
        parsed = json.loads(response.content)
        return {
            "risk_severity": parsed.get("risk_severity", "unknown"),
            "risk_category": parsed.get("risk_category", ""),
            "real_world_impact": parsed.get("real_world_impact", ""),
            "error_mechanism": parsed.get("error_mechanism", ""),
        }
    except json.JSONDecodeError:
        return {
            "risk_severity": "unknown",
            "risk_category": "",
            "real_world_impact": response.content[:200],
            "error_mechanism": "",
        }


def run(args):
    """Main experiment runner."""
    # Load D1 results
    try:
        d1_results = load_d1_results(args.input)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Run D1 calibration experiment first to generate results.")
        sys.exit(1)

    print(f"D4 Overconfident Risk Analysis")
    print(f"  D1 results loaded: {len(d1_results)} entries from {len(args.input)} pattern(s)")
    print(f"  Confidence threshold: {args.confidence_threshold:.0%}")
    print()

    # Filter overconfident errors
    overconfident = filter_overconfident_errors(
        d1_results, confidence_threshold=args.confidence_threshold,
    )
    print(f"  Overconfident errors found: {len(overconfident)}")

    if not overconfident:
        print("  No overconfident errors found. Try lowering --confidence-threshold.")
        return

    # Classify risk for each error
    classifier = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])
    classified = []

    limit = args.limit if args.limit > 0 else len(overconfident)
    for i, entry in enumerate(overconfident[:limit]):
        print(f"  [{i+1}/{min(limit, len(overconfident))}] "
              f"{entry['question_id']} (conf={entry['confidence']:.0%})...", end=" ")

        risk = classify_risk(classifier, entry)
        entry["risk_classification"] = risk
        classified.append(entry)
        print(f"→ {risk['risk_severity']}")

    # Detect collective hallucinations
    collective = detect_collective_hallucination(overconfident)

    # Compute summary
    severity_counts = {}
    for entry in classified:
        sev = entry["risk_classification"]["risk_severity"]
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    summary = {
        "total_d1_results": len(d1_results),
        "total_overconfident_errors": len(overconfident),
        "classified_count": len(classified),
        "severity_distribution": severity_counts,
        "avg_confidence": round(
            sum(e["confidence"] for e in overconfident) / len(overconfident), 4
        ),
        "collective_hallucinations": len(collective),
    }

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = RESULTS_DIR / f"run_{timestamp}"
    output_dir.mkdir()

    output = {
        "metadata": {
            "experiment": "D4_overconfident_risk",
            "confidence_threshold": args.confidence_threshold,
            "n_classified": len(classified),
            "timestamp": timestamp,
        },
        "summary": summary,
        "classified_errors": classified,
        "collective_hallucinations": collective,
    }

    output_path = output_dir / "results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"  Total D1 results:         {len(d1_results)}")
    print(f"  Overconfident errors:      {len(overconfident)}")
    print(f"  Avg confidence (wrong):    {summary['avg_confidence']:.1%}")
    print(f"  Severity distribution:")
    for sev, count in sorted(severity_counts.items()):
        print(f"    {sev}: {count}")
    print(f"  Collective hallucinations: {len(collective)} questions")
    print(f"  Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="D4: Overconfident Risk Analysis")
    parser.add_argument(
        "--input", required=True, nargs="+",
        help="D1 result JSON file(s) or glob pattern(s)",
    )
    parser.add_argument(
        "--confidence-threshold", type=float,
        default=DEFAULT_CONFIDENCE_THRESHOLD,
        help=f"Min confidence for overconfident error (default: {DEFAULT_CONFIDENCE_THRESHOLD})",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Max errors to classify (0=all)",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
