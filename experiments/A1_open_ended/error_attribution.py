"""Error attribution for Level C (incorrect) answers."""

import json
from typing import Any, Dict, Optional

from experiments.shared.llm_client import LLMClient
from .config import ERROR_CATEGORIES


ATTRIBUTION_SYSTEM = """You are an expert CFA exam grader analyzing why a student got a question wrong.

Classify the primary error into one of these categories:
{categories}

Respond in JSON:
{{
    "error_category": "<category>",
    "explanation": "brief explanation of what went wrong",
    "could_be_fixed_with_tools": true/false
}}"""

ATTRIBUTION_USER = """Question: {question}

Gold answer: {gold_answer}

Student's (incorrect) answer:
{student_answer}

What type of error did the student make?"""


def attribute_error(
    question_text: str,
    student_response: str,
    gold_answer: str,
    client: Optional[LLMClient] = None,
) -> Dict[str, Any]:
    """Classify the type of error in an incorrect response.

    Args:
        question_text: The question.
        student_response: The model's incorrect response.
        gold_answer: The correct answer text.
        client: LLMClient for classification (defaults to gpt-4o-mini).

    Returns:
        {"error_category": str, "explanation": str, "could_be_fixed_with_tools": bool}
    """
    if client is None:
        from experiments.shared.config import MODEL_REGISTRY
        client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    categories_str = "\n".join(f"- {cat}" for cat in ERROR_CATEGORIES)

    messages = [
        {"role": "system", "content": ATTRIBUTION_SYSTEM.format(categories=categories_str)},
        {"role": "user", "content": ATTRIBUTION_USER.format(
            question=question_text,
            gold_answer=gold_answer,
            student_answer=student_response[:1000],
        )},
    ]

    response = client.chat(messages, temperature=0.0, max_tokens=300)

    try:
        parsed = json.loads(response.content)
        category = parsed.get("error_category", "unknown")
        if category not in ERROR_CATEGORIES:
            category = "unknown"
        return {
            "error_category": category,
            "explanation": parsed.get("explanation", ""),
            "could_be_fixed_with_tools": parsed.get("could_be_fixed_with_tools", False),
        }
    except json.JSONDecodeError:
        return {
            "error_category": "unknown",
            "explanation": response.content[:200],
            "could_be_fixed_with_tools": False,
        }
