#!/usr/bin/env python3
"""Run I2 behavioral biases experiment on synthetic scenarios.

Usage:
    python -m experiments.I2_behavioral_biases.run_synthetic \
        --scenarios experiments/I2_behavioral_biases/synthetic_scenarios/synthetic_bias_*.json \
        --model gpt-4o-mini
"""

import argparse
import glob
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.llm_client import LLMClient

from .config import BIAS_SYSTEM, NEUTRAL_SYSTEM
from .bias_scorer import score_bias, compute_debiasing_effect

RESULTS_DIR = Path(__file__).parent / "results"


def run(args):
    if args.model not in MODEL_REGISTRY:
        print(f"Unknown model: {args.model}")
        sys.exit(1)

    config = MODEL_REGISTRY[args.model]
    client = LLMClient(config)
    scorer_client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    # Load synthetic scenarios from JSON files
    scenarios = []
    for pattern in args.scenarios:
        for path in sorted(glob.glob(pattern)):
            with open(path) as f:
                items = json.load(f)
                scenarios.extend(items)
                print(f"  Loaded {len(items)} scenarios from {path}")

    if not scenarios:
        print("No scenarios found!")
        return

    print(f"\nI2 Behavioral Biases (Synthetic) — {args.model}")
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

        # Check for empty response
        if not bias_response.content or len(bias_response.content.strip()) < 10:
            print(f"EMPTY_BIAS", end=" ")
            bias_result = {"bias_score": 0.5, "chosen_option": "EMPTY", "reasoning": "empty response"}
        else:
            bias_result = score_bias(scenario, bias_response.content, scorer_client)

        # Run neutral version
        neutral_messages = [
            {"role": "system", "content": NEUTRAL_SYSTEM},
            {"role": "user", "content": scenario["neutral_version"]},
        ]
        neutral_response = client.chat(neutral_messages, temperature=0.0, max_tokens=1500)

        if not neutral_response.content or len(neutral_response.content.strip()) < 10:
            print(f"EMPTY_NEUTRAL", end=" ")
            neutral_result = {"bias_score": 0.5, "chosen_option": "EMPTY", "reasoning": "empty response"}
        else:
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
            "bias_response": bias_response.content[:500] if bias_response.content else "",
            "neutral_response": neutral_response.content[:500] if neutral_response.content else "",
            "bias_chosen": bias_result["chosen_option"],
            "neutral_chosen": neutral_result["chosen_option"],
            "bias_reasoning": bias_result["reasoning"],
            "bias_response_empty": not bias_response.content or len(bias_response.content.strip()) < 10,
            "neutral_response_empty": not neutral_response.content or len(neutral_response.content.strip()) < 10,
        }
        results.append(entry)

        print(f"bias={bias_result['bias_score']:.2f} "
              f"neutral={neutral_result['bias_score']:.2f} "
              f"debiasing={debiasing:+.2f}")

    # Summary
    n = len(results)
    n_empty_bias = sum(1 for r in results if r.get("bias_response_empty"))
    n_empty_neutral = sum(1 for r in results if r.get("neutral_response_empty"))

    avg_bias = sum(r["bias_version_score"] for r in results) / n if n else 0
    avg_neutral = sum(r["neutral_version_score"] for r in results) / n if n else 0
    avg_debiasing = sum(r["debiasing_effect"] for r in results) / n if n else 0

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
        "n_empty_bias": n_empty_bias,
        "n_empty_neutral": n_empty_neutral,
        "avg_bias_score": round(avg_bias, 3),
        "avg_neutral_score": round(avg_neutral, 3),
        "avg_debiasing_effect": round(avg_debiasing, 3),
        "by_bias_type": type_summary,
    }

    # Save
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = RESULTS_DIR / f"synthetic_{args.model}_{timestamp}"
    output_dir.mkdir()

    output = {
        "metadata": {
            "experiment": "I2_behavioral_biases_synthetic",
            "model": args.model,
            "dataset": "synthetic_bias",
            "n_scenarios": n,
            "timestamp": timestamp,
        },
        "summary": summary,
        "results": results,
    }

    output_path = output_dir / "results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"SUMMARY — {args.model} on {n} synthetic bias scenarios")
    print(f"{'='*60}")
    print(f"  Overall bias score:      {avg_bias:.3f}")
    print(f"  Neutral score:           {avg_neutral:.3f}")
    print(f"  Debiasing effect:        {avg_debiasing:+.3f}")
    if n_empty_bias or n_empty_neutral:
        print(f"  Empty responses:         {n_empty_bias} bias, {n_empty_neutral} neutral")
    print()
    print(f"  {'Bias Type':<22} {'Score':<8} {'Neutral':<8} {'Debiasing':<10} {'N':<4}")
    print(f"  {'-'*52}")
    for bt, ts in sorted(type_summary.items()):
        print(f"  {bt:<22} {ts['avg_bias_score']:<8.3f} "
              f"{ts['avg_neutral_score']:<8.3f} "
              f"{ts['avg_debiasing_effect']:<+10.3f} "
              f"{ts['n_scenarios']:<4}")
    print(f"\n  Results: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarios", nargs="+", required=True,
                        help="Glob patterns for scenario JSON files")
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
