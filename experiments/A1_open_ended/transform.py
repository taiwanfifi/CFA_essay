"""Transform MCQ questions into open-ended format for A1 benchmark."""

import json
import re
from typing import Any, Dict, Optional

from experiments.shared.llm_client import LLMClient
from .config import GOLD_ANSWER_SYSTEM, GOLD_ANSWER_USER


def strip_choices_and_instruction(query: str) -> str:
    """Remove MCQ choices and instruction prefix from a CFA query.

    Returns the bare question stem suitable for open-ended answering.
    """
    text = query

    # Remove instruction prefix
    prefix_pattern = (
        r"Read the questions and answers carefully, and choose the one "
        r"you think is appropriate among the three options A, B and C\.\s*"
    )
    text = re.sub(prefix_pattern, "", text, flags=re.IGNORECASE)

    # Remove ",CHOICES: A: ... Answer:" block
    text = re.sub(r",?\s*CHOICES\s*:.*$", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Remove trailing "Answer:" prompt
    text = re.sub(r"\s*Answer\s*:\s*$", "", text, flags=re.IGNORECASE)

    # Remove Q: prefix
    text = re.sub(r"^Q\s*:\s*", "", text.strip())

    return text.strip()


def extract_answer_text_from_query(query: str, answer_letter: str) -> str:
    """Extract the text of a specific answer choice from the query."""
    # Find CHOICES section
    choices_match = re.search(r"CHOICES\s*:\s*(.*?)(?:\s*Answer:|$)", query, re.DOTALL)
    if not choices_match:
        return answer_letter

    choices_text = choices_match.group(1)

    # Extract the specific answer's text
    # Pattern: "A: some text." or "A: some text,"
    pattern = rf"{answer_letter}\s*:\s*(.+?)(?:\.\s*[BC]\s*:|$)"
    m = re.search(pattern, choices_text, re.DOTALL)
    if m:
        return m.group(1).strip().rstrip(".,")

    return answer_letter


def generate_gold_answer(
    question: dict,
    client: LLMClient,
) -> Dict[str, Any]:
    """Generate a structured gold answer for an open-ended version of an MCQ.

    Uses LLM to convert the MCQ correct answer into a complete open-ended answer.
    """
    answer_letter = question["answer"]
    answer_text = extract_answer_text_from_query(question["query"], answer_letter)
    question_stem = strip_choices_and_instruction(question["query"])

    messages = [
        {"role": "system", "content": GOLD_ANSWER_SYSTEM},
        {"role": "user", "content": GOLD_ANSWER_USER.format(
            question=question_stem,
            answer_letter=answer_letter,
            answer_text=answer_text,
        )},
    ]

    response = client.chat(messages, temperature=0.0, max_tokens=500)

    try:
        gold = json.loads(response.content)
    except json.JSONDecodeError:
        gold = {
            "numerical_answer": None,
            "unit": "",
            "concept": answer_text,
            "solution_summary": response.content[:300],
        }

    gold["answer_letter"] = answer_letter
    gold["answer_text"] = answer_text
    return gold
