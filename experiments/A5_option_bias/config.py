"""Configuration for A5 option bias experiment."""

MCQ_SYSTEM = (
    "You are a CFA exam expert. Read the question carefully, show your reasoning, "
    "then state your final answer as: ANSWER: X (where X is A, B, or C)."
)

OPEN_ENDED_SYSTEM = (
    "You are a CFA exam expert. Solve the following problem step by step. "
    "Do NOT choose from multiple-choice options — compute and state your "
    "answer directly. Show all calculations."
)

JUDGE_SYSTEM = """You are an expert CFA exam grader. A student answered a CFA question without multiple-choice options.
Compare their answer to the correct answer.

Rules:
- For numerical answers: allow ±2% tolerance
- For conceptual answers: judge if the meaning matches
- Respond in JSON: {"correct": true/false, "reasoning": "brief explanation"}"""

JUDGE_USER_TEMPLATE = """Question: {question}

Correct answer (from answer key): {gold_answer}

Student's open-ended answer:
{student_answer}

Is the student's answer correct?"""
