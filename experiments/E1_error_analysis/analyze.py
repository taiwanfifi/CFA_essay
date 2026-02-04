#!/usr/bin/env python3
"""
E1 Error Analysis Runner.

Analyzes errors from CFA agent experiments and produces:
1. Error classification by topic, type, and cognitive stage
2. Cross-tabulation matrices
3. Visualizations for paper

Usage:
    # Analyze single method
    python experiments/E1_error_analysis/analyze.py --input results.json --method cot

    # Analyze ALL methods in a results file
    python experiments/E1_error_analysis/analyze.py --input results.json --all-methods

    # Quick test with limit
    python experiments/E1_error_analysis/analyze.py --input results.json --all-methods --limit 5
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from experiments.E1_error_analysis.classifier import ErrorClassifier
from experiments.E1_error_analysis.taxonomy import CFATopic, ErrorType, CognitiveStage


# =============================================================================
# Analysis Functions
# =============================================================================

def extract_errors(
    results: List[Dict[str, Any]],
    method: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Extract only the incorrect answers from results."""
    errors = []
    for r in results:
        if method and r.get("method") != method:
            continue
        if not r.get("correct", False):
            errors.append(r)
    return errors


def build_crosstab(
    classifications: List[Any],
    dim1: str = "topic",
    dim2: str = "error_type",
) -> Dict[str, Dict[str, int]]:
    """Build cross-tabulation between any two dimensions."""
    crosstab: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for c in classifications:
        val1 = getattr(c, dim1)
        val2 = getattr(c, dim2)
        key1 = val1.value if hasattr(val1, 'value') else str(val1)
        key2 = val2.value if hasattr(val2, 'value') else str(val2)
        crosstab[key1][key2] += 1

    return dict(crosstab)


def print_summary(classifications: List[Any], title: str = "") -> Dict[str, Any]:
    """Print analysis summary and return summary dict."""
    n = len(classifications)
    if title:
        print(f"\n{'='*70}")
        print(f"{title} ({n} errors)")
        print(f"{'='*70}")
    else:
        print(f"\n{'='*70}")
        print(f"ERROR ANALYSIS SUMMARY ({n} errors)")
        print(f"{'='*70}")

    # Topic distribution
    print(f"\n--- By CFA Topic ---")
    topic_counts = Counter(c.topic.value for c in classifications)
    for topic, count in topic_counts.most_common():
        pct = count / n * 100
        print(f"  {topic:<25} {count:>3} ({pct:>5.1f}%)")

    # Error type distribution
    print(f"\n--- By Error Type ---")
    error_counts = Counter(c.error_type.value for c in classifications)
    for error, count in error_counts.most_common():
        pct = count / n * 100
        print(f"  {error:<30} {count:>3} ({pct:>5.1f}%)")

    # Cognitive stage distribution
    print(f"\n--- By Cognitive Stage ---")
    stage_counts = Counter(c.cognitive_stage.value for c in classifications)
    for stage, count in stage_counts.most_common():
        pct = count / n * 100
        print(f"  {stage:<15} {count:>3} ({pct:>5.1f}%)")

    # Method distribution (if multiple methods)
    methods = set(c.method for c in classifications if c.method)
    if len(methods) > 1:
        print(f"\n--- By Method ---")
        method_counts = Counter(c.method for c in classifications)
        for method, count in method_counts.most_common():
            pct = count / n * 100
            print(f"  {method:<20} {count:>3} ({pct:>5.1f}%)")

    # Cross-tabulation: Topic × Error Type
    print(f"\n--- Topic × Error Type (top 5 error types) ---")
    crosstab = build_crosstab(classifications, "topic", "error_type")

    # Get top 5 error types
    top_errors = [e for e, _ in error_counts.most_common(5)]
    all_topics = sorted(crosstab.keys())

    # Header
    header = f"{'Topic':<20}"
    for e in top_errors:
        header += f" {e[:12]:>12}"
    header += f" {'TOTAL':>8}"
    print(header)
    print("-" * len(header))

    # Rows
    for topic in all_topics:
        row = f"{topic:<20}"
        topic_total = 0
        for e in top_errors:
            count = crosstab[topic].get(e, 0)
            topic_total += count
            row += f" {count:>12}"
        # Add other error types not in top 5
        for e, cnt in crosstab[topic].items():
            if e not in top_errors:
                topic_total += cnt
        row += f" {topic_total:>8}"
        print(row)

    # Cross-tabulation: Topic × Cognitive Stage
    print(f"\n--- Topic × Cognitive Stage ---")
    crosstab_stage = build_crosstab(classifications, "topic", "cognitive_stage")

    all_stages = ["identify", "recall", "extract", "calculate", "verify", "unknown"]
    header2 = f"{'Topic':<20}"
    for s in all_stages:
        header2 += f" {s[:10]:>10}"
    print(header2)
    print("-" * len(header2))

    for topic in all_topics:
        row = f"{topic:<20}"
        for s in all_stages:
            count = crosstab_stage[topic].get(s, 0)
            row += f" {count:>10}"
        print(row)

    return {
        "n_errors": n,
        "by_topic": dict(topic_counts),
        "by_error_type": dict(error_counts),
        "by_cognitive_stage": dict(stage_counts),
        "crosstab_topic_error": crosstab,
        "crosstab_topic_stage": crosstab_stage,
    }


def save_results(
    classifications: List[Any],
    output_path: Path,
    metadata: Dict[str, Any],
    summary: Dict[str, Any],
) -> None:
    """Save classification results to JSON."""
    # Convert to serializable format
    results = []
    for c in classifications:
        results.append({
            "question_id": c.question_id,
            "method": c.method,
            "topic": c.topic.value,
            "error_type": c.error_type.value,
            "cognitive_stage": c.cognitive_stage.value,
            "confidence": c.confidence,
            "reasoning": c.reasoning,
            "model_answer": c.model_answer,
            "correct_answer": c.correct_answer,
        })

    output = {
        "metadata": metadata,
        "summary": summary,
        "classifications": results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to: {output_path}")


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="E1 Error Analysis")
    parser.add_argument("--input", type=str, required=True,
                        help="Path to experiment results JSON")
    parser.add_argument("--method", type=str, default=None,
                        help="Filter by single method (e.g., 'cot', 'agent_naive')")
    parser.add_argument("--all-methods", action="store_true",
                        help="Analyze all methods in the results file")
    parser.add_argument("--limit", type=int, default=0,
                        help="Max errors to classify per method (0 = all)")
    parser.add_argument("--model", type=str, default="gpt-4o-mini",
                        help="Model for classification")
    parser.add_argument("--output", type=str, default="",
                        help="Output path (default: auto-generated)")
    args = parser.parse_args()

    # Validate API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set")
        sys.exit(1)

    # Load experiment results
    input_path = Path(args.input)
    if not input_path.exists():
        # Try relative to project root
        input_path = PROJECT_ROOT / args.input
    if not input_path.exists():
        print(f"ERROR: Input file not found: {args.input}")
        sys.exit(1)

    print(f"Loading results from: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_results = data.get("results", [])

    # Determine which methods to analyze
    if args.all_methods:
        methods = sorted(set(r.get("method") for r in all_results if r.get("method")))
        print(f"Found methods: {methods}")
    elif args.method:
        methods = [args.method]
    else:
        # Default: analyze all methods
        methods = sorted(set(r.get("method") for r in all_results if r.get("method")))
        print(f"No method specified, analyzing all: {methods}")

    # Collect all errors
    all_errors = []
    for method in methods:
        method_errors = extract_errors(all_results, method)
        print(f"  {method}: {len(method_errors)} errors")
        if args.limit > 0:
            method_errors = method_errors[:args.limit]
        all_errors.extend(method_errors)

    print(f"\nTotal errors to analyze: {len(all_errors)}")

    if not all_errors:
        print("No errors to analyze!")
        return

    # Classify errors
    print(f"\nClassifying errors with {args.model}...")
    classifier = ErrorClassifier(model=args.model)
    classifications = classifier.classify_batch(all_errors, verbose=True)

    # Print summary
    summary = print_summary(classifications)

    # Also print per-method summary if multiple methods
    if len(methods) > 1:
        for method in methods:
            method_classifications = [c for c in classifications if c.method == method]
            if method_classifications:
                print_summary(method_classifications, title=f"Method: {method}")

    # Save results
    output_dir = PROJECT_ROOT / "experiments" / "E1_error_analysis" / "results"
    output_dir.mkdir(exist_ok=True)

    if args.output:
        output_path = Path(args.output)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        suffix = f"_{args.method}" if args.method else "_all_methods"
        output_path = output_dir / f"error_analysis{suffix}_{ts}.json"

    metadata = {
        "input_file": str(input_path),
        "methods_analyzed": methods,
        "n_errors_analyzed": len(classifications),
        "limit_per_method": args.limit if args.limit > 0 else "all",
        "classifier_model": args.model,
        "timestamp": datetime.now().isoformat(),
    }
    save_results(classifications, output_path, metadata, summary)


if __name__ == "__main__":
    main()
