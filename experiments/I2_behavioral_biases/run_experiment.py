"""I2 Behavioral Biases: Test LLMs for financial behavioral biases.

Usage:
    python -m experiments.I2_behavioral_biases.run_experiment \
        --bias-types loss_aversion anchoring --limit 5 --model gpt-4o-mini
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
from experiments.shared.llm_client import LLMClient

from .config import BIAS_SYSTEM, NEUTRAL_SYSTEM, BIAS_TYPES
from .scenarios import get_scenarios, get_available_bias_types
from .bias_scorer import score_bias, compute_debiasing_effect

RESULTS_DIR = Path(__file__).parent / "results"


def run(args):
    """Main experiment runner."""
    if args.model not in MODEL_REGISTRY:
        print(f"Unknown model: {args.model}. Available: {list(MODEL_REGISTRY.keys())}")
        sys.exit(1)

    config = MODEL_REGISTRY[args.model]
    client = LLMClient(config)
    scorer_client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    # Get scenarios
    bias_types = args.bias_types if args.bias_types else None
    scenarios = get_scenarios(bias_types=bias_types, limit=args.limit)

    if not scenarios:
        print(f"No scenarios found. Available bias types: {get_available_bias_types()}")
        sys.exit(1)

    print(f"I2 Behavioral Biases Experiment")
    print(f"  Model: {args.model}")
    print(f"  Bias types: {bias_types or 'all'}")
    print(f"  Scenarios: {len(scenarios)}")
    print(f"  Scorer: gpt-4o-mini")
    print()

    results = []
    for i, scenario in enumerate(scenarios):
        print(f"  [{i+1}/{len(scenarios)}] {scenario['id']} ({scenario['bias_type']})...",
              end=" ", flush=True)

        # Run bias-inducing version
        bias_messages = [
            {"role": "system", "content": BIAS_SYSTEM},
            {"role": "user", "content": scenario["bias_version"]},
        ]
        bias_response = client.chat(bias_messages, temperature=0.0, max_tokens=1500)

        # Score bias
        bias_result = score_bias(scenario, bias_response.content, scorer_client)

        # Run neutral version
        neutral_messages = [
            {"role": "system", "content": NEUTRAL_SYSTEM},
            {"role": "user", "content": scenario["neutral_version"]},
        ]
        neutral_response = client.chat(neutral_messages, temperature=0.0, max_tokens=1500)

        # Score neutral
        neutral_result = score_bias(scenario, neutral_response.content, scorer_client)

        debiasing = compute_debiasing_effect(
            bias_result["bias_score"], neutral_result["bias_score"]
        )

        entry = {
            "scenario_id": scenario["id"],
            "bias_type": scenario["bias_type"],
            "bias_version_score": bias_result["bias_score"],
            "neutral_version_score": neutral_result["bias_score"],
            "debiasing_effect": debiasing,
            "bias_response": bias_response.content[:500],
            "neutral_response": neutral_response.content[:500],
            "bias_chosen": bias_result["chosen_option"],
            "neutral_chosen": neutral_result["chosen_option"],
            "bias_reasoning": bias_result["reasoning"],
            "tokens": (
                bias_response.prompt_tokens + bias_response.completion_tokens +
                neutral_response.prompt_tokens + neutral_response.completion_tokens
            ),
        }
        results.append(entry)

        print(f"bias={bias_result['bias_score']:.2f} "
              f"neutral={neutral_result['bias_score']:.2f} "
              f"debiasing={debiasing:+.2f}")

    # Compute summary
    n = len(results)

    # Overall bias score
    avg_bias = sum(r["bias_version_score"] for r in results) / n if n else 0
    avg_neutral = sum(r["neutral_version_score"] for r in results) / n if n else 0
    avg_debiasing = sum(r["debiasing_effect"] for r in results) / n if n else 0

    # Per-bias-type breakdown
    type_summary = {}
    for bt in set(r["bias_type"] for r in results):
        bt_results = [r for r in results if r["bias_type"] == bt]
        bt_n = len(bt_results)
        type_summary[bt] = {
            "n_scenarios": bt_n,
            "avg_bias_score": round(
                sum(r["bias_version_score"] for r in bt_results) / bt_n, 3
            ),
            "avg_neutral_score": round(
                sum(r["neutral_version_score"] for r in bt_results) / bt_n, 3
            ),
            "avg_debiasing_effect": round(
                sum(r["debiasing_effect"] for r in bt_results) / bt_n, 3
            ),
        }

    summary = {
        "n_scenarios": n,
        "avg_bias_score": round(avg_bias, 3),
        "avg_neutral_score": round(avg_neutral, 3),
        "avg_debiasing_effect": round(avg_debiasing, 3),
        "by_bias_type": type_summary,
    }

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = RESULTS_DIR / f"run_{timestamp}"
    output_dir.mkdir()

    output = {
        "metadata": {
            "experiment": "I2_behavioral_biases",
            "model": args.model,
            "n_scenarios": n,
            "bias_types": list(set(r["bias_type"] for r in results)),
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
    print(f"  Overall bias score:      {avg_bias:.3f} (0=rational, 1=biased)")
    print(f"  Neutral score:           {avg_neutral:.3f}")
    print(f"  Debiasing effect:        {avg_debiasing:+.3f}")
    print()
    print(f"  {'Bias Type':<22} {'Score':<8} {'Neutral':<8} {'Debiasing':<10} {'N':<4}")
    print(f"  {'-'*52}")
    for bt, ts in sorted(type_summary.items()):
        print(f"  {bt:<22} {ts['avg_bias_score']:<8.3f} "
              f"{ts['avg_neutral_score']:<8.3f} "
              f"{ts['avg_debiasing_effect']:<+10.3f} "
              f"{ts['n_scenarios']:<4}")
    print(f"\n  Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="I2: Behavioral Biases Experiment")
    parser.add_argument(
        "--bias-types", nargs="+", default=None,
        help="Bias types to test (default: all). Options: " +
             ", ".join(get_available_bias_types()),
    )
    parser.add_argument("--limit", type=int, default=0,
                       help="Max scenarios per bias type (0=all)")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to test")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
