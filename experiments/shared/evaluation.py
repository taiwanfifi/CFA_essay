"""Shared evaluation utilities: tolerance matching, LLM-as-judge, statistical tests."""

import json
import logging
import re
from typing import Any, Dict, List, Optional

from .config import MODEL_REGISTRY
from .llm_client import LLMClient

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tolerance matching for numerical answers
# ---------------------------------------------------------------------------

def tolerance_match(predicted: float, gold: float, tol: float = 0.02) -> bool:
    """Check if predicted value is within tolerance of gold value.

    Uses relative tolerance for values > 1, absolute tolerance otherwise.
    """
    if gold == 0:
        return abs(predicted) < tol
    if abs(gold) >= 1:
        return abs(predicted - gold) / abs(gold) <= tol
    return abs(predicted - gold) <= tol


def magnitude_match(predicted: float, gold: float) -> bool:
    """Check if predicted is within the same order of magnitude as gold."""
    if gold == 0 or predicted == 0:
        return abs(predicted - gold) < 1
    ratio = predicted / gold
    return 0.1 <= ratio <= 10


# ---------------------------------------------------------------------------
# LLM-as-Judge for semantic evaluation
# ---------------------------------------------------------------------------

JUDGE_SYSTEM = """You are an expert CFA exam grader. Compare the student's answer to the correct answer.

Evaluate whether the student's answer is:
- CORRECT: Matches the correct answer in substance (exact match or equivalent)
- PARTIALLY_CORRECT: Shows correct reasoning direction but has minor errors
- INCORRECT: Wrong answer or fundamentally flawed reasoning

Respond in JSON format:
{"verdict": "CORRECT|PARTIALLY_CORRECT|INCORRECT", "reasoning": "brief explanation"}"""

JUDGE_USER_TEMPLATE = """Question: {question}

Correct Answer: {gold_answer}

Student's Answer: {student_answer}

Evaluate the student's answer."""


def semantic_match_judge(
    question: str,
    student_answer: str,
    gold_answer: str,
    client: Optional[LLMClient] = None,
) -> Dict[str, Any]:
    """Use LLM-as-judge to evaluate a free-form answer.

    Args:
        question: The original question text.
        student_answer: The model's response.
        gold_answer: The correct/reference answer.
        client: LLMClient instance. If None, creates a gpt-4o-mini client.

    Returns:
        {"verdict": str, "reasoning": str, "raw_response": str}
    """
    if client is None:
        client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    messages = [
        {"role": "system", "content": JUDGE_SYSTEM},
        {"role": "user", "content": JUDGE_USER_TEMPLATE.format(
            question=question,
            gold_answer=gold_answer,
            student_answer=student_answer,
        )},
    ]

    response = client.chat(messages, temperature=0.0, max_tokens=300)

    try:
        parsed = json.loads(response.content)
        return {
            "verdict": parsed.get("verdict", "UNKNOWN"),
            "reasoning": parsed.get("reasoning", ""),
            "raw_response": response.content,
        }
    except json.JSONDecodeError:
        # Try to extract verdict from plain text
        text_upper = response.content.upper()
        if "CORRECT" in text_upper and "INCORRECT" not in text_upper:
            verdict = "CORRECT"
        elif "PARTIALLY" in text_upper:
            verdict = "PARTIALLY_CORRECT"
        elif "INCORRECT" in text_upper:
            verdict = "INCORRECT"
        else:
            verdict = "UNKNOWN"
        return {
            "verdict": verdict,
            "reasoning": response.content,
            "raw_response": response.content,
        }


# ---------------------------------------------------------------------------
# Statistical tests
# ---------------------------------------------------------------------------

def mcnemar_test(paired_results: List[Dict[str, bool]]) -> Dict[str, Any]:
    """McNemar's test for paired binary outcomes.

    Args:
        paired_results: List of {"condition_a": bool, "condition_b": bool}

    Returns:
        {"b": int, "c": int, "chi2": float, "p_value": float, "significant": bool}
        where b = A correct & B wrong, c = A wrong & B correct
    """
    b = sum(1 for r in paired_results if r["condition_a"] and not r["condition_b"])
    c = sum(1 for r in paired_results if not r["condition_a"] and r["condition_b"])

    if b + c == 0:
        return {"b": b, "c": c, "chi2": 0.0, "p_value": 1.0, "significant": False}

    # McNemar's chi-squared (with continuity correction)
    chi2 = (abs(b - c) - 1) ** 2 / (b + c) if (b + c) > 0 else 0.0

    # Approximate p-value from chi2(1) distribution
    # Using survival function approximation
    import math
    p_value = math.erfc(math.sqrt(chi2 / 2))

    return {
        "b": b,
        "c": c,
        "chi2": round(chi2, 4),
        "p_value": round(p_value, 4),
        "significant": p_value < 0.05,
    }
