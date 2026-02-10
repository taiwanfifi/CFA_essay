"""Bias scorer using LLM-as-judge to quantify behavioral bias in responses."""

import json
from typing import Any, Dict, Optional

from experiments.shared.llm_client import LLMClient
from .config import SCORE_SYSTEM, SCORE_USER


def score_bias(
    scenario: dict,
    model_response: str,
    client: Optional[LLMClient] = None,
) -> Dict[str, Any]:
    """Score a model response for behavioral bias.

    Args:
        scenario: Scenario dict with bias_version, rational_answer, biased_answer.
        model_response: The model's full response text.
        client: LLMClient for scoring (defaults to gpt-4o-mini).

    Returns:
        {
            "bias_score": float (0=rational, 1=biased),
            "chosen_option": str,
            "reasoning": str,
        }
    """
    if client is None:
        from experiments.shared.config import MODEL_REGISTRY
        client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    messages = [
        {"role": "system", "content": SCORE_SYSTEM},
        {"role": "user", "content": SCORE_USER.format(
            bias_type=scenario["bias_type"],
            scenario=scenario["bias_version"],
            response=model_response[:1500],
            rational_answer=scenario["rational_answer"],
            biased_answer=scenario["biased_answer"],
        )},
    ]

    response = client.chat(messages, temperature=0.0, max_tokens=300)

    content = response.content.strip()
    # Handle markdown code blocks wrapping JSON
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    try:
        parsed = json.loads(content)
        score = float(parsed.get("bias_score", 0.5))
        score = max(0.0, min(1.0, score))  # Clamp to [0, 1]
        return {
            "bias_score": round(score, 3),
            "chosen_option": parsed.get("chosen_option", ""),
            "reasoning": parsed.get("reasoning", ""),
        }
    except (json.JSONDecodeError, ValueError):
        # Try to extract JSON object from response
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                parsed = json.loads(content[start:end])
                score = float(parsed.get("bias_score", 0.5))
                score = max(0.0, min(1.0, score))
                return {
                    "bias_score": round(score, 3),
                    "chosen_option": parsed.get("chosen_option", ""),
                    "reasoning": parsed.get("reasoning", ""),
                }
            except (json.JSONDecodeError, ValueError):
                pass
        return {
            "bias_score": 0.5,
            "chosen_option": "unknown",
            "reasoning": response.content[:200],
        }


def compute_debiasing_effect(
    bias_score: float,
    neutral_score: float,
) -> float:
    """Compute how much the neutral framing reduces bias.

    Returns value in [-1, 1]:
    - Positive: neutral framing reduces bias (good)
    - Zero: no effect
    - Negative: neutral framing increases bias (unlikely but possible)
    """
    return round(bias_score - neutral_score, 3)
