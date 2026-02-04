"""Shared prompt utilities and answer extraction for CFA experiments."""

import re
from typing import Optional


# ---------------------------------------------------------------------------
# Answer extraction — MCQ
# ---------------------------------------------------------------------------

def extract_answer(text: str) -> Optional[str]:
    """Extract A/B/C answer from model response using a 5-layer regex chain.

    Tries progressively looser patterns:
    1. "ANSWER: X"
    2. "the answer is X"
    3. "answer is X"
    4. Standalone letter at end of text
    5. First A/B/C anywhere
    """
    if not text:
        return None
    text_upper = text.upper().strip()

    # Layer 1: explicit ANSWER: X
    m = re.search(r"ANSWER\s*:\s*([A-C])\b", text_upper)
    if m:
        return m.group(1)

    # Layer 2: "the answer is X"
    m = re.search(r"THE\s+ANSWER\s+IS\s+([A-C])\b", text_upper)
    if m:
        return m.group(1)

    # Layer 3: "answer is X"
    m = re.search(r"ANSWER\s+IS\s+([A-C])\b", text_upper)
    if m:
        return m.group(1)

    # Layer 4: standalone letter at end
    m = re.search(r"\b([A-C])\s*[.!]?\s*$", text_upper)
    if m:
        return m.group(1)

    # Layer 5: first A/B/C token
    m = re.search(r"\b([A-C])\b", text_upper)
    if m:
        return m.group(1)

    return None


# ---------------------------------------------------------------------------
# Answer extraction — numerical
# ---------------------------------------------------------------------------

def extract_numerical_answer(text: str) -> Optional[float]:
    """Extract a numerical answer from model response.

    Handles: $400,000 / 400000 / 400,000.00 / £400k / -3.5% etc.
    Returns the raw number (e.g. 400000.0), caller handles unit logic.
    """
    if not text:
        return None

    # Remove currency symbols and whitespace around numbers
    cleaned = re.sub(r"[£$€¥]", "", text)

    # Look for patterns like "the answer is 400,000" or "= 400,000"
    patterns = [
        r"(?:answer|result|value|equals?|is|≈|approximately)\s*[:=]?\s*([-+]?[\d,]+\.?\d*)",
        r"\*\*([-+]?[\d,]+\.?\d*)\*\*",  # **bold numbers**
        r"([-+]?[\d,]+\.?\d*)\s*(?:%|percent)",  # percentages
    ]

    for pattern in patterns:
        m = re.search(pattern, cleaned, re.IGNORECASE)
        if m:
            num_str = m.group(1).replace(",", "")
            try:
                return float(num_str)
            except ValueError:
                continue

    # Fallback: find the last number in the text (often the final answer)
    numbers = re.findall(r"[-+]?[\d,]+\.?\d*", cleaned)
    if numbers:
        num_str = numbers[-1].replace(",", "")
        try:
            return float(num_str)
        except ValueError:
            pass

    return None


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

MCQ_SYSTEM = (
    "You are a CFA exam expert. Read the question carefully, show your reasoning, "
    "then state your final answer as: ANSWER: X (where X is A, B, or C)."
)

MCQ_DIRECT_SYSTEM = (
    "You are a CFA exam expert. Read the question and respond with ONLY the letter "
    "of the correct answer (A, B, or C). Do not explain."
)

OPEN_ENDED_SYSTEM = (
    "You are a CFA exam expert. Solve the following problem step by step. "
    "Show all calculations and state your final numerical answer clearly."
)


def build_mcq_prompt(question: dict) -> list:
    """Build standard MCQ prompt messages from a question dict."""
    return [
        {"role": "system", "content": MCQ_SYSTEM},
        {"role": "user", "content": question["query"]},
    ]


def build_mcq_direct_prompt(question: dict) -> list:
    """Build direct MCQ prompt (letter only, no reasoning)."""
    return [
        {"role": "system", "content": MCQ_DIRECT_SYSTEM},
        {"role": "user", "content": question["query"]},
    ]


def build_open_ended_prompt(question_text: str) -> list:
    """Build open-ended prompt from question text (no choices)."""
    return [
        {"role": "system", "content": OPEN_ENDED_SYSTEM},
        {"role": "user", "content": question_text},
    ]
