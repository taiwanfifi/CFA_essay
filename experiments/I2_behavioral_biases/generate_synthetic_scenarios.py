#!/usr/bin/env python3
"""Generate additional behavioral bias scenarios for I2 experiment.

Creates 15 new scenarios per bias type (90 total) using GPT-4o-mini,
in the same format as scenarios.py.

Usage:
    python -m experiments.I2_behavioral_biases.generate_synthetic_scenarios --n-per-type 15
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.llm_client import LLMClient

OUTPUT_DIR = Path(__file__).parent / "synthetic_scenarios"

BIAS_TYPES = {
    "loss_aversion": {
        "name": "Loss Aversion",
        "definition": "The tendency to prefer avoiding losses over acquiring equivalent gains. People feel losses roughly twice as strongly as gains.",
        "cfa_context": "Investment selection, portfolio rebalancing, risk tolerance assessment",
        "bias_direction": "Choose lower-EV option to avoid stated losses; hold losing positions; reject positive-EV gambles",
        "examples": [
            "Choosing guaranteed $7K over 80% chance of $10K with 20% chance of -$2K loss (EV=$7.6K)",
            "Refusing to sell a losing stock to avoid realizing the loss",
            "Rejecting a merger with positive NPV because of downside scenario emphasis",
            "Over-hedging a portfolio due to fear of mark-to-market losses",
            "Holding cash despite inflation erosion to avoid market volatility",
        ],
    },
    "anchoring": {
        "name": "Anchoring Bias",
        "definition": "Over-reliance on the first piece of information encountered (the 'anchor') when making decisions.",
        "cfa_context": "Valuation, price targets, earnings estimates, fair value assessment",
        "bias_direction": "Estimate biased toward the anchor value (historical price, purchase price, prior estimate) rather than fundamental analysis",
        "examples": [
            "Valuing stock near historical high of $150 despite deteriorating fundamentals suggesting $90",
            "Setting price target anchored to IPO price rather than DCF analysis",
            "PE fund valuation anchored to acquisition price despite EBITDA decline",
            "Earnings estimate anchored to last quarter despite structural market shift",
            "Real estate appraisal anchored to purchase price rather than current comparables",
        ],
    },
    "framing": {
        "name": "Framing Effect",
        "definition": "Making different decisions based on how the same information is presented (gain frame vs loss frame).",
        "cfa_context": "Risk communication, investment recommendations, performance reporting",
        "bias_direction": "Risk-averse in gain frames, risk-seeking in loss frames; different answer for mathematically equivalent scenarios",
        "examples": [
            "Preferring a fund with '90% chance of success' over one with '10% chance of failure'",
            "Different restructuring choice when framed as 'saving 200 jobs' vs 'losing 400 jobs'",
            "Portfolio viewed differently as '-5% quarterly' vs '+18% over 18 months'",
            "Insurance uptake differs with '10% mortality' vs '90% survival' framing",
            "Bond described as '4% real return' vs 'nominal return minus expected inflation'",
        ],
    },
    "recency": {
        "name": "Recency Bias",
        "definition": "Overweighting recent events and recent performance when making investment decisions, extrapolating short-term trends.",
        "cfa_context": "Asset allocation, sector rotation, manager selection, market timing",
        "bias_direction": "Extrapolate recent trends (performance chasing); overweight last few quarters; ignore long-term base rates",
        "examples": [
            "Increasing tech allocation to 70% after 5 quarters of outperformance",
            "Abandoning value strategy after 2 years of underperformance despite 50-year evidence",
            "Allocating 15% to crypto after +150% return, ignoring 80% drawdown history",
            "Firing a fund manager after 1 bad year despite 10-year alpha track record",
            "Eliminating small-caps due to 3-year underperformance despite 100-year premium",
        ],
    },
    "disposition_effect": {
        "name": "Disposition Effect",
        "definition": "The tendency to sell winning investments too early (to lock in gains) and hold losing investments too long (to avoid realizing losses).",
        "cfa_context": "Portfolio management, tax-loss harvesting, rebalancing decisions",
        "bias_direction": "Sell winners (lock in gains) and hold losers (avoid realizing losses), even when forward-looking analysis suggests the opposite",
        "examples": [
            "Selling a winning stock up 50% while holding a losing stock down 31%",
            "Tax-loss harvesting by selling the winner instead of the loser",
            "Rebalancing by trimming best performers rather than worst",
            "Reluctance to add to winning position ('it can't go higher')",
            "Averaging down on a deteriorating position to 'reduce cost basis'",
        ],
    },
    "overconfidence": {
        "name": "Overconfidence Bias",
        "definition": "Excessive confidence in one's own predictions, knowledge, or ability to pick investments. Manifests as overly narrow confidence intervals and underestimation of risk.",
        "cfa_context": "Forecasting, active management fees, concentration risk, trading frequency",
        "bias_direction": "Overly narrow confidence intervals; extreme predictions; excessive trading; concentrated portfolios; paying high fees for active management",
        "examples": [
            "Assigning >50% probability to a biotech stock tripling when base rate is 2%",
            "Expecting backtested strategy to deliver live performance near backtest",
            "Paying 1.5% fee + 20% carry despite 92% of active managers underperforming",
            "Concentrating 40% of portfolio in a single sector based on 'conviction'",
            "Trading weekly despite evidence that frequency destroys returns",
        ],
    },
}

GENERATION_PROMPT = """You are an expert in behavioral finance and CFA exam preparation. Generate {n} NOVEL paired investment scenarios to test for {bias_name} in LLM responses.

Definition: {definition}
CFA Context: {cfa_context}
Bias Direction: {bias_direction}

For each scenario, create:
1. A "bias_version": A realistic CFA-level investment scenario that frames the decision in a way that would trigger {bias_name}. Include specific dollar amounts, percentages, names, and financial context. The scenario should be a decision between two or more options.
2. A "neutral_version": The SAME decision reframed purely in quantitative terms (expected values, projected returns) that strips away the emotional/anchoring/framing elements.
3. A "rational_answer": The objectively correct answer based on expected value, risk-adjusted returns, or fundamental analysis (1 sentence).
4. A "biased_answer": What a biased agent influenced by {bias_name} would choose (1 sentence).

IMPORTANT RULES:
- Each scenario must be UNIQUE and test a DIFFERENT financial situation
- Use realistic CFA-level financial language and complexity
- The bias_version should be 3-6 sentences with specific numbers
- The neutral_version should be 2-3 sentences with clean quantitative framing
- Both versions must describe the SAME underlying decision
- Do NOT reuse scenarios from these examples: {example_list}

Return ONLY a JSON array. Each element must have exactly:
- "bias_version": string
- "neutral_version": string
- "rational_answer": string
- "biased_answer": string

Output ONLY the JSON array, no other text."""


def generate_scenarios_for_type(
    client: LLMClient,
    bias_type: str,
    bias_info: dict,
    n_per_type: int,
) -> list:
    """Generate synthetic bias scenarios for one bias type."""
    example_list = "\n".join(f"- {ex}" for ex in bias_info["examples"])

    prompt = GENERATION_PROMPT.format(
        n=n_per_type,
        bias_name=bias_info["name"],
        definition=bias_info["definition"],
        cfa_context=bias_info["cfa_context"],
        bias_direction=bias_info["bias_direction"],
        example_list=example_list,
    )

    messages = [
        {"role": "system", "content": "You are a behavioral finance expert. Output valid JSON only."},
        {"role": "user", "content": prompt},
    ]

    response = client.chat(messages, temperature=0.7, max_tokens=8000)
    content = response.content.strip()

    # Parse JSON from response (handle markdown code blocks)
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    try:
        scenarios = json.loads(content)
    except json.JSONDecodeError:
        start = content.find("[")
        end = content.rfind("]") + 1
        if start >= 0 and end > start:
            scenarios = json.loads(content[start:end])
        else:
            print(f"    WARN: Failed to parse JSON for {bias_type}")
            return []

    # Validate
    valid = []
    required_keys = {"bias_version", "neutral_version", "rational_answer", "biased_answer"}
    for s in scenarios:
        if not all(k in s for k in required_keys):
            continue
        valid.append(s)

    return valid


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic behavioral bias scenarios")
    parser.add_argument("--n-per-type", type=int, default=15,
                        help="Scenarios per bias type (default: 15)")
    parser.add_argument("--model", default="gpt-4o-mini",
                        help="Model for generation (default: gpt-4o-mini)")
    args = parser.parse_args()

    config = MODEL_REGISTRY[args.model]
    client = LLMClient(config)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Bias type code mapping (matches scenarios.py conventions)
    type_codes = {
        "loss_aversion": "la",
        "anchoring": "an",
        "framing": "fr",
        "recency": "re",
        "disposition_effect": "de",
        "overconfidence": "oc",
    }

    all_scenarios = []
    for bias_type, bias_info in BIAS_TYPES.items():
        print(f"  Generating {args.n_per_type} scenarios for {bias_info['name']}...")
        scenarios = generate_scenarios_for_type(client, bias_type, bias_info, args.n_per_type)
        print(f"    Got {len(scenarios)} valid scenarios")

        code = type_codes[bias_type]
        for i, s in enumerate(scenarios):
            s["id"] = f"{code}_synth_{i+1:02d}"
            s["bias_type"] = bias_type
            s["dataset"] = "synthetic_bias"

        all_scenarios.extend(scenarios)
        time.sleep(1)  # Rate limit

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"synthetic_bias_scenarios_{timestamp}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_scenarios, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Generated {len(all_scenarios)} synthetic bias scenarios")
    print(f"Saved to: {output_path}")

    from collections import Counter
    type_counts = Counter(s["bias_type"] for s in all_scenarios)
    for bt, count in sorted(type_counts.items()):
        print(f"  {bt}: {count}")


if __name__ == "__main__":
    main()
