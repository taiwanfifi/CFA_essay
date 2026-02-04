"""Configuration for I1 counterfactual experiment."""

# ---------------------------------------------------------------------------
# Perturbation levels
# ---------------------------------------------------------------------------

# Level 1: Change one numerical parameter (e.g., interest rate 5% → 7%)
# Level 2: Change two parameters (e.g., rate + maturity)
# Level 3: Change the question structure (e.g., find rate instead of PV)

PERTURBATION_LEVELS = {
    1: "single_parameter",   # Change one number
    2: "dual_parameter",     # Change two numbers
    3: "structural",         # Change what's being asked
}

# ---------------------------------------------------------------------------
# Perturbation generation prompt
# ---------------------------------------------------------------------------

PERTURB_SYSTEM = """You are a CFA exam question designer. Given an original CFA question and its answer, create a PERTURBED version.

Rules:
1. Change ONLY the specified numerical parameter(s)
2. Keep the same solution method and concept
3. Calculate the NEW correct answer using the same approach
4. Ensure the perturbed question is mathematically valid
5. The perturbed answer should be different from the original

Respond in JSON:
{
    "perturbed_question": "full question text with changed values",
    "perturbed_answer": "the new correct answer (letter for MCQ, or number)",
    "changes_made": ["list of what was changed"],
    "solution_steps": "brief calculation showing the new answer"
}"""

PERTURB_LEVEL1_USER = """Original question:
{question}

Original correct answer: {answer}

PERTURBATION INSTRUCTION: Change the interest rate or primary numerical value to a different but reasonable value. Keep everything else the same. Calculate the new correct answer."""

PERTURB_LEVEL2_USER = """Original question:
{question}

Original correct answer: {answer}

PERTURBATION INSTRUCTION: Change TWO numerical parameters (e.g., interest rate AND time period, or payment amount AND rate). Keep the same solution method. Calculate the new correct answer."""

PERTURB_LEVEL3_USER = """Original question:
{question}

Original correct answer: {answer}

PERTURBATION INSTRUCTION: Change what the question asks for (e.g., if it asks for PV, ask for the interest rate instead; if it asks for bond price, ask for YTM). Keep the same scenario but change the unknown variable. Calculate the new correct answer."""

PERTURB_USER_TEMPLATES = {
    1: PERTURB_LEVEL1_USER,
    2: PERTURB_LEVEL2_USER,
    3: PERTURB_LEVEL3_USER,
}

# ---------------------------------------------------------------------------
# MCQ prompt for answering perturbed questions
# ---------------------------------------------------------------------------

MCQ_SYSTEM = (
    "You are a CFA exam expert. Read the question carefully, show your reasoning, "
    "then state your final answer as: ANSWER: X (where X is A, B, or C)."
)

OPEN_SYSTEM = (
    "You are a CFA exam expert. Solve the following problem step by step. "
    "Show all calculations and state your final numerical answer clearly."
)
