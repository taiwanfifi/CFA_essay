"""GPT-4o driven perturbation generator for counterfactual questions."""

import json
import re
from typing import Any, Dict, Optional

from experiments.shared.llm_client import LLMClient
from .config import PERTURB_SYSTEM, PERTURB_USER_TEMPLATES


def generate_perturbation(
    question: dict,
    level: int,
    client: LLMClient,
) -> Dict[str, Any]:
    """Generate a perturbed version of a CFA question.

    Args:
        question: Original question dict with 'query' and 'answer'.
        level: Perturbation level (1, 2, or 3).
        client: LLMClient for generation (typically gpt-4o-mini or gpt-4o).

    Returns:
        {
            "perturbed_question": str,
            "perturbed_answer": str,
            "changes_made": list,
            "solution_steps": str,
            "level": int,
            "valid": bool,
        }
    """
    template = PERTURB_USER_TEMPLATES.get(level, PERTURB_USER_TEMPLATES[1])

    messages = [
        {"role": "system", "content": PERTURB_SYSTEM},
        {"role": "user", "content": template.format(
            question=question["query"],
            answer=question["answer"],
        )},
    ]

    response = client.chat(messages, temperature=0.3, max_tokens=1500)

    try:
        parsed = json.loads(response.content)
        perturbed_q = parsed.get("perturbed_question", "")
        perturbed_a = str(parsed.get("perturbed_answer", ""))

        # Validate: perturbed question should differ from original
        valid = (
            len(perturbed_q) > 20
            and perturbed_q != question["query"]
            and len(perturbed_a) > 0
        )

        return {
            "perturbed_question": perturbed_q,
            "perturbed_answer": perturbed_a,
            "changes_made": parsed.get("changes_made", []),
            "solution_steps": parsed.get("solution_steps", ""),
            "level": level,
            "valid": valid,
        }
    except json.JSONDecodeError:
        # Try to extract from raw text
        return {
            "perturbed_question": response.content[:500],
            "perturbed_answer": "",
            "changes_made": [],
            "solution_steps": "",
            "level": level,
            "valid": False,
        }


def validate_perturbation(
    original: dict,
    perturbation: dict,
    client: LLMClient,
) -> Dict[str, Any]:
    """Validate that a perturbation is correct using a verification LLM call.

    Asks the model to solve the perturbed question and checks against the
    perturbed answer.
    """
    messages = [
        {"role": "system", "content": (
            "You are a CFA exam expert. Solve this problem step by step. "
            "State your final answer clearly."
        )},
        {"role": "user", "content": perturbation["perturbed_question"]},
    ]

    response = client.chat(messages, temperature=0.0, max_tokens=1000)

    from experiments.shared.prompts import extract_numerical_answer, extract_answer

    # Try to verify
    expected = perturbation["perturbed_answer"]
    model_answer = response.content

    # Check letter match for MCQ
    extracted_letter = extract_answer(model_answer)
    if extracted_letter and extracted_letter == expected.strip().upper():
        return {"verified": True, "method": "letter_match"}

    # Check numerical match
    from experiments.shared.evaluation import tolerance_match
    model_num = extract_numerical_answer(model_answer)
    expected_num = extract_numerical_answer(expected)
    if model_num is not None and expected_num is not None and expected_num != 0:
        if tolerance_match(model_num, expected_num, tol=0.05):
            return {"verified": True, "method": "numerical_match"}

    return {"verified": False, "method": "no_match", "model_answer": model_answer[:200]}
