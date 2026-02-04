"""Three-level evaluator for open-ended CFA answers.

Level A (Exact): Within numerical tolerance or exact semantic match
Level B (Directional): Correct direction/approach, minor deviation
Level C (Incorrect): Wrong answer
"""

import json
from typing import Any, Dict, Optional

from experiments.shared.llm_client import LLMClient
from experiments.shared.prompts import extract_numerical_answer
from experiments.shared.evaluation import tolerance_match, magnitude_match
from .config import NUMERICAL_TOLERANCE, LEVEL_A, LEVEL_B, LEVEL_C


JUDGE_SYSTEM = """You are an expert CFA exam grader evaluating an open-ended answer.

Classify the student's answer into one of three levels:
- **Level A (Exact)**: Answer matches the gold standard within tolerance. Correct method AND correct result.
- **Level B (Directional)**: Shows correct understanding and direction but arrives at a slightly different value due to different (but defensible) assumptions, rounding, or methodology.
- **Level C (Incorrect)**: Wrong answer, wrong method, or fundamentally flawed reasoning.

Respond in JSON:
{
    "level": "A|B|C",
    "reasoning": "brief explanation",
    "student_value": <extracted number or null>,
    "gold_value": <expected number or null>
}"""

JUDGE_USER = """Question: {question}

Gold standard answer: {gold_answer}
Gold numerical value: {gold_numerical}

Student's answer:
{student_answer}

Classify this answer (Level A, B, or C)."""


def evaluate_response(
    question_text: str,
    student_response: str,
    gold_answer: Dict[str, Any],
    judge_client: Optional[LLMClient] = None,
) -> Dict[str, Any]:
    """Evaluate a student response using three-level grading.

    First tries automatic numerical matching, then falls back to LLM judge.

    Args:
        question_text: The open-ended question text.
        student_response: The model's full response.
        gold_answer: Dict with 'numerical_answer', 'answer_text', etc.
        judge_client: LLMClient for LLM-as-judge (gpt-4o-mini).

    Returns:
        {"level": str, "reasoning": str, "auto_graded": bool, ...}
    """
    gold_num = gold_answer.get("numerical_answer")
    student_num = extract_numerical_answer(student_response)

    # --- Automatic grading for numerical answers ---
    if gold_num is not None and student_num is not None:
        gold_num = float(gold_num)

        # Level A: within tolerance
        if tolerance_match(student_num, gold_num, tol=NUMERICAL_TOLERANCE):
            return {
                "level": LEVEL_A,
                "reasoning": (
                    f"Numerical match: student={student_num}, "
                    f"gold={gold_num}, within {NUMERICAL_TOLERANCE:.0%} tolerance"
                ),
                "auto_graded": True,
                "student_value": student_num,
                "gold_value": gold_num,
            }

        # Level B: same magnitude, correct direction
        if magnitude_match(student_num, gold_num):
            return {
                "level": LEVEL_B,
                "reasoning": (
                    f"Same magnitude: student={student_num}, gold={gold_num}, "
                    f"ratio={student_num/gold_num:.3f}"
                ),
                "auto_graded": True,
                "student_value": student_num,
                "gold_value": gold_num,
            }

        # Level C: wrong magnitude
        return {
            "level": LEVEL_C,
            "reasoning": (
                f"Wrong magnitude: student={student_num}, gold={gold_num}"
            ),
            "auto_graded": True,
            "student_value": student_num,
            "gold_value": gold_num,
        }

    # --- LLM judge for non-numerical answers ---
    if judge_client is None:
        from experiments.shared.config import MODEL_REGISTRY
        judge_client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    gold_text = gold_answer.get("answer_text", "")
    gold_num_str = str(gold_num) if gold_num is not None else "N/A"

    messages = [
        {"role": "system", "content": JUDGE_SYSTEM},
        {"role": "user", "content": JUDGE_USER.format(
            question=question_text,
            gold_answer=gold_text,
            gold_numerical=gold_num_str,
            student_answer=student_response[:1000],
        )},
    ]

    response = judge_client.chat(messages, temperature=0.0, max_tokens=300)

    try:
        parsed = json.loads(response.content)
        level = parsed.get("level", "C").upper()
        if level not in ("A", "B", "C"):
            level = "C"
        return {
            "level": {"A": LEVEL_A, "B": LEVEL_B, "C": LEVEL_C}[level],
            "reasoning": parsed.get("reasoning", ""),
            "auto_graded": False,
            "student_value": parsed.get("student_value"),
            "gold_value": parsed.get("gold_value"),
        }
    except json.JSONDecodeError:
        # Best-effort extraction
        text = response.content.upper()
        if "LEVEL A" in text:
            level = LEVEL_A
        elif "LEVEL B" in text:
            level = LEVEL_B
        else:
            level = LEVEL_C
        return {
            "level": level,
            "reasoning": response.content[:200],
            "auto_graded": False,
            "student_value": student_num,
            "gold_value": gold_num,
        }
