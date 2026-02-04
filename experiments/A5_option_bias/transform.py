"""Transform MCQ questions into open-ended format by removing choices."""

import re
from typing import Optional


def strip_choices(query: str) -> str:
    """Remove MCQ choices from a CFA query string.

    Handles formats like:
    - ",CHOICES: A: ... B: ... C: ... Answer:"
    - "A. ... B. ... C. ..."

    Returns the question stem without choices or answer prompt.
    """
    # Remove the instruction prefix if present
    text = query
    prefix_pattern = (
        r"Read the questions and answers carefully, and choose the one "
        r"you think is appropriate among the three options A, B and C\.\s*"
    )
    text = re.sub(prefix_pattern, "", text, flags=re.IGNORECASE)

    # Remove ",CHOICES: A: ... Answer:" block
    text = re.sub(r",?\s*CHOICES\s*:.*$", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Remove trailing "Answer:" prompt
    text = re.sub(r"\s*Answer\s*:\s*$", "", text, flags=re.IGNORECASE)

    # Remove standalone choice lines (A: ..., B: ..., C: ...)
    text = re.sub(r"\n\s*[A-C]\s*[:.)]\s*[^\n]+", "", text)

    # Remove Q: prefix if present
    text = re.sub(r"^Q\s*:\s*", "", text.strip())

    return text.strip()


def get_gold_answer_text(question: dict) -> str:
    """Get the text of the correct answer choice.

    Args:
        question: Dict with 'answer' (letter) and 'query' (full question text).

    Returns:
        The text of the correct option, or just the letter if parsing fails.
    """
    answer_letter = question.get("answer", "").strip().upper()
    query = question.get("query", "")

    # Fallback: try CHOICES section
    choices_match = re.search(r"CHOICES\s*:\s*(.*?)(?:\s*Answer:|$)", query, re.DOTALL)
    if choices_match:
        choices_text = choices_match.group(1)
        # Split on letter prefixes: "A: ...,B: ...,C: ..."
        parts = re.split(r"(?:^|,)\s*([A-C])\s*:\s*", choices_text)
        # parts looks like ['', 'A', 'text...', 'B', 'text...', 'C', 'text...']
        for j in range(1, len(parts) - 1, 2):
            if parts[j] == answer_letter:
                return parts[j + 1].strip().rstrip(".,")

    # Try "A: text" or "A. text" pattern directly
    pattern = rf"{re.escape(answer_letter)}\s*[:.)]\s*(.+?)(?:\s*[,.]?\s*[BC]\s*[:.)]|\s*Answer:|$)"
    m = re.search(pattern, query)
    if m:
        return m.group(1).strip().rstrip(".,")

    return answer_letter
