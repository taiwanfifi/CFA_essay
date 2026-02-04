"""Configuration for A1 open-ended benchmark experiment."""

# ---------------------------------------------------------------------------
# Evaluation levels
# ---------------------------------------------------------------------------

LEVEL_A = "exact"         # Within numerical tolerance or exact semantic match
LEVEL_B = "directional"   # Correct direction/approach but different assumptions
LEVEL_C = "incorrect"     # Wrong answer

# Numerical tolerance for Level A
NUMERICAL_TOLERANCE = 0.02  # ±2%

# Directional tolerance for Level B (same order of magnitude)
MAGNITUDE_TOLERANCE_RATIO = (0.1, 10)  # predicted/gold must be in this range

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

OPEN_ENDED_SYSTEM = (
    "You are a CFA exam expert. Solve the following problem step by step. "
    "Show all calculations, state all assumptions, and give your final "
    "answer clearly. Do NOT refer to multiple-choice options."
)

# ---------------------------------------------------------------------------
# Gold answer generation prompt (for converting MCQ gold → open-ended gold)
# ---------------------------------------------------------------------------

GOLD_ANSWER_SYSTEM = """You are a CFA exam expert. Given a CFA question and its correct MCQ answer, produce a complete gold-standard open-ended answer.

Include:
1. The final numerical value (if applicable) with units
2. The key concept or principle applied
3. Brief solution steps

Respond in JSON:
{
    "numerical_answer": <number or null>,
    "unit": "<string or empty>",
    "concept": "<key principle>",
    "solution_summary": "<brief steps>"
}"""

GOLD_ANSWER_USER = """Question: {question}

Correct MCQ answer: {answer_letter} — {answer_text}

Produce the gold-standard open-ended answer."""

# ---------------------------------------------------------------------------
# Error attribution categories
# ---------------------------------------------------------------------------

ERROR_CATEGORIES = [
    "formula_error",           # Used wrong formula
    "arithmetic_error",        # Right formula, wrong computation
    "assumption_error",        # Wrong compounding, timing, etc.
    "conceptual_error",        # Misunderstood the concept entirely
    "reading_error",           # Misread the question
    "unit_error",              # Wrong units or conversion
    "incomplete_reasoning",    # Stopped before reaching the answer
    "hallucination",           # Made up facts or numbers
]
