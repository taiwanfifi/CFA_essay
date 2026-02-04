"""
CFA Multi-Turn Reasoning Agent — v2 (structural tool integration).

Design philosophy: "給 LLM 工具 ≠ LLM 會用工具"
Instead of passively offering tools (v1 agent_naive: tool_choice="auto", model ignored tools),
we structurally force tool usage where it helps via two new strategies:

Methods:
1. zero_shot       — single call, direct answer (baseline)
2. cot             — single call, chain-of-thought (baseline)
3. cot_verify      — CoT → tool-augmented verification pass
4. structured      — classify question → route to appropriate pipeline
5. agent_naive     — v1 multi-turn agent (kept for comparison)

The key insight from v1 experiments: gpt-4o-mini never voluntarily uses tools (8.9% usage on 90q).
v2 forces verification via tools AFTER the model reasons, rather than hoping it calls tools.
"""

import json
import os
import re
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

from .tools import TOOL_DISPATCH, TOOL_SCHEMAS, execute_tool

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_MODEL = os.getenv("CFA_AGENT_MODEL", "gpt-4o-mini")
MAX_TURNS = 8

# Pricing per 1M tokens
PRICING = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o-mini-2024-07-18": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-2024-08-06": {"input": 2.50, "output": 10.00},
}

client = OpenAI()


def _calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Estimate cost in USD."""
    prices = PRICING.get(model, PRICING["gpt-4o-mini"])
    return (prompt_tokens * prices["input"] + completion_tokens * prices["output"]) / 1_000_000


# ---------------------------------------------------------------------------
# Token tracker — accumulates usage across multiple API calls
# ---------------------------------------------------------------------------

class TokenTracker:
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def add(self, usage):
        self.prompt_tokens += usage.prompt_tokens
        self.completion_tokens += usage.completion_tokens

    @property
    def total_tokens(self):
        return self.prompt_tokens + self.completion_tokens

    def cost(self, model: str) -> float:
        return _calculate_cost(model, self.prompt_tokens, self.completion_tokens)


# ---------------------------------------------------------------------------
# Answer extraction
# ---------------------------------------------------------------------------

def extract_answer(text: str) -> Optional[str]:
    """Extract A/B/C answer from model response using a regex chain."""
    if not text:
        return None
    # 1. "ANSWER: X" pattern (most explicit)
    m = re.search(r"ANSWER\s*:\s*([A-C])\b", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # 2. "The answer is X"
    m = re.search(r"the\s+answer\s+is\s+([A-C])\b", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # 3. "answer is X" or "correct answer is X"
    m = re.search(r"(?:correct\s+)?answer\s+is\s+([A-C])\b", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # 4. Standalone letter at end (e.g. "... B." or "B")
    m = re.search(r"\b([A-C])\s*\.?\s*$", text.strip())
    if m:
        return m.group(1).upper()
    # 5. First standalone A/B/C
    m = re.search(r"\b([A-C])\b", text)
    if m:
        return m.group(1).upper()
    return None


# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

ZERO_SHOT_SYSTEM = """You are a CFA exam expert. Answer the multiple-choice question below.
Respond with ONLY the letter of the correct answer: A, B, or C.
Format: ANSWER: X"""

COT_SYSTEM = """You are a CFA exam expert. Answer the multiple-choice question using this structured approach:

1. **Identify**: What CFA topic and concept does this question test?
2. **Recall**: What formulas or principles apply?
3. **Extract**: What numerical data is given?
4. **Calculate**: Show your work step by step.
5. **Verify**: Double-check your answer against the choices.

After your analysis, state your final answer as: ANSWER: X (where X is A, B, or C)"""

# v2: Verification prompt — instructs model to re-check calculations WITH tools
VERIFY_WITH_TOOLS_SYSTEM = """You are a CFA exam verification expert with access to financial calculator tools.

You will be given a question and a proposed answer with reasoning. Your job is to VERIFY the answer by:

1. **Check reasoning**: Is the logic and approach correct?
2. **Re-compute every calculation**: For ANY numerical computation in the reasoning, you MUST use the appropriate calculator tool to independently verify the result. Do NOT trust the mental math — re-do it with tools.
3. **Check formula selection**: Was the correct formula used for this type of problem?
4. **Compare results**: If your tool-verified calculation differs from the proposed reasoning, the tool result is authoritative.

IMPORTANT:
- If the question involves ANY numbers or calculations, you MUST call at least one calculator tool.
- Use tvm_calculator for time-value-of-money (PV, FV, annuities).
- Use bond_calculator for bond pricing, duration, convexity, excess returns.
- Use statistics_calculator for portfolio return/risk, Sharpe ratios.
- Use economics_calculator for Taylor rule, CAPM, risk premiums.
- Use general_math for simple arithmetic verification.
- For purely conceptual/ethics questions with no calculations, you may verify reasoning directly.

After verification, state: ANSWER: X (where X is A, B, or C)
If you found an error, explain what was wrong and provide the corrected answer."""

# v2: Classification prompt — categorize question type
CLASSIFY_SYSTEM = """Classify this CFA exam question into exactly ONE category.

Reply with a single word only:
- CONCEPTUAL — if the question tests knowledge, definitions, ethics, standards, or qualitative judgment with no calculations needed
- CALCULATION — if the question requires numerical computation (formulas, arithmetic, financial math)
- MIXED — if the question combines conceptual knowledge with some numerical elements

Reply with ONLY one word: CONCEPTUAL, CALCULATION, or MIXED"""

# v2: Forced-calculation prompt — for questions classified as CALCULATION
CALCULATION_SYSTEM = """You are a CFA Level III exam expert. This question requires numerical calculation.

You MUST solve it using this approach:
1. **Identify** the specific formula or financial concept needed.
2. **Extract** ALL numerical data from the question.
3. **Calculate** using the calculator tools provided. Do NOT do mental math — use the tools for every computation.
4. **Map** your calculated result to the closest answer choice.

IMPORTANT: You MUST call at least one calculator tool. Use:
- tvm_calculator for PV, FV, annuity, rate-solving problems
- bond_calculator for bond pricing, YTM, duration, convexity, excess returns
- statistics_calculator for portfolio return/risk, Sharpe ratio, utility
- economics_calculator for Taylor rule, CAPM, risk premium buildup, Fisher effect
- general_math for any arithmetic that doesn't fit the specialized tools

After calculation, state your final answer as: ANSWER: X (where X is A, B, or C)"""

# v1 agent prompt (kept for agent_naive)
AGENT_NAIVE_SYSTEM = """You are a CFA Level III exam expert with access to financial calculator tools.

For each question, follow this approach:
1. **Identify** the CFA topic and key concepts being tested.
2. **Recall** relevant formulas and principles.
3. **Extract** all numerical data from the question.
4. **Calculate** using the appropriate calculator tool(s). Call tools for any non-trivial computation.
5. **Verify** your result makes sense before answering.

Guidelines:
- For quantitative questions: USE the calculator tools. Do not do mental math for financial calculations.
- For conceptual/ethics questions: Reason directly without tools.
- You may call multiple tools if needed (e.g., calculate portfolio return, then Sharpe ratio).
- After completing your analysis, state your final answer as: ANSWER: X (where X is A, B, or C)"""


# ---------------------------------------------------------------------------
# Shared helper: multi-turn tool loop
# ---------------------------------------------------------------------------

def _run_tool_loop(
    messages: List[dict],
    model: str,
    tracker: TokenTracker,
    max_turns: int = MAX_TURNS,
    tool_choice_first: str = "auto",
    tool_choice_rest: str = "auto",
) -> tuple:
    """Run a multi-turn tool-calling loop.

    Returns (final_content, all_tool_calls, turns_used).
    """
    all_tool_calls = []

    for turn in range(max_turns):
        tc = tool_choice_first if turn == 0 else tool_choice_rest

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice=tc,
            temperature=0,
            max_tokens=2000,
        )
        tracker.add(response.usage)
        choice = response.choices[0]

        # Handle tool calls
        if choice.message.tool_calls:
            messages.append(choice.message)
            for tool_call in choice.message.tool_calls:
                fn_name = tool_call.function.name
                try:
                    fn_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    fn_args = {}

                result = execute_tool(fn_name, fn_args)
                all_tool_calls.append({
                    "turn": turn + 1,
                    "tool": fn_name,
                    "args": fn_args,
                    "result": result,
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })
            continue

        # No tool calls — check for final answer
        content = choice.message.content or ""
        messages.append({"role": "assistant", "content": content})
        answer = extract_answer(content)

        if answer:
            return content, all_tool_calls, turn + 1

        # No answer found — nudge
        if turn < max_turns - 1:
            messages.append({
                "role": "user",
                "content": "Please state your final answer as: ANSWER: A, B, or C",
            })

    # Extract last assistant content
    final_content = ""
    for m in reversed(messages):
        if isinstance(m, dict) and m.get("role") == "assistant" and m.get("content"):
            final_content = m["content"]
            break
        elif hasattr(m, "content") and hasattr(m, "role") and m.role == "assistant" and m.content:
            final_content = m.content
            break

    return final_content, all_tool_calls, max_turns


# ---------------------------------------------------------------------------
# Shared helper: classify question type
# ---------------------------------------------------------------------------

def _classify_question(question: str, model: str, tracker: TokenTracker) -> str:
    """Classify question as CONCEPTUAL, CALCULATION, or MIXED."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": CLASSIFY_SYSTEM},
            {"role": "user", "content": question},
        ],
        temperature=0,
        max_tokens=10,
    )
    tracker.add(response.usage)
    raw = (response.choices[0].message.content or "").strip().upper()

    # Parse classification
    if "CALCULATION" in raw:
        return "CALCULATION"
    elif "CONCEPTUAL" in raw:
        return "CONCEPTUAL"
    elif "MIXED" in raw:
        return "MIXED"
    else:
        # Default to MIXED if unclear (will get verification)
        return "MIXED"


# ---------------------------------------------------------------------------
# Method 1: Zero-shot (unchanged)
# ---------------------------------------------------------------------------

def run_zero_shot(question: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """Single API call, direct answer."""
    t0 = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": ZERO_SHOT_SYSTEM},
            {"role": "user", "content": question},
        ],
        temperature=0,
        max_tokens=100,
    )
    elapsed = time.time() - t0
    msg = response.choices[0].message
    usage = response.usage

    return {
        "method": "zero_shot",
        "answer": extract_answer(msg.content),
        "reasoning": msg.content,
        "turns": 1,
        "tool_calls": [],
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "cost_usd": _calculate_cost(model, usage.prompt_tokens, usage.completion_tokens),
        "elapsed_seconds": round(elapsed, 2),
        "model": model,
    }


# ---------------------------------------------------------------------------
# Method 2: Chain-of-thought (unchanged)
# ---------------------------------------------------------------------------

def run_cot(question: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """Single API call with structured CoT prompt."""
    t0 = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": COT_SYSTEM},
            {"role": "user", "content": question},
        ],
        temperature=0,
        max_tokens=2000,
    )
    elapsed = time.time() - t0
    msg = response.choices[0].message
    usage = response.usage

    return {
        "method": "cot",
        "answer": extract_answer(msg.content),
        "reasoning": msg.content,
        "turns": 1,
        "tool_calls": [],
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "cost_usd": _calculate_cost(model, usage.prompt_tokens, usage.completion_tokens),
        "elapsed_seconds": round(elapsed, 2),
        "model": model,
    }


# ---------------------------------------------------------------------------
# Method 3: CoT + Tool-Augmented Verification (NEW in v2)
# ---------------------------------------------------------------------------

def run_cot_verify(question: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """CoT reasoning first, then tool-augmented verification pass.

    Strategy:
    1. Run standard CoT to get initial reasoning + answer
    2. Pass question + CoT reasoning to a verification agent WITH tools
    3. Verifier re-computes every calculation using tools
    4. If verifier disagrees, use verifier's answer (tool-checked)
    """
    t0 = time.time()
    tracker = TokenTracker()

    # --- Phase 1: CoT reasoning ---
    cot_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": COT_SYSTEM},
            {"role": "user", "content": question},
        ],
        temperature=0,
        max_tokens=2000,
    )
    tracker.add(cot_response.usage)
    cot_content = cot_response.choices[0].message.content or ""
    cot_answer = extract_answer(cot_content)

    # --- Phase 2: Tool-augmented verification ---
    verify_prompt = (
        f"## Original Question\n{question}\n\n"
        f"## Proposed Answer: {cot_answer}\n\n"
        f"## Reasoning\n{cot_content}\n\n"
        f"Please verify this answer. Re-compute every calculation using your calculator tools."
    )
    verify_messages: List[dict] = [
        {"role": "system", "content": VERIFY_WITH_TOOLS_SYSTEM},
        {"role": "user", "content": verify_prompt},
    ]

    verify_content, tool_calls, verify_turns = _run_tool_loop(
        verify_messages, model, tracker, max_turns=4,
        tool_choice_first="auto", tool_choice_rest="auto",
    )
    verified_answer = extract_answer(verify_content)

    elapsed = time.time() - t0
    final_answer = verified_answer or cot_answer

    return {
        "method": "cot_verify",
        "answer": final_answer,
        "reasoning": verify_content,
        "cot_answer": cot_answer,
        "cot_reasoning": cot_content,
        "answer_changed": (final_answer != cot_answer),
        "turns": 1 + verify_turns,  # 1 for CoT + N for verification
        "tool_calls": tool_calls,
        "prompt_tokens": tracker.prompt_tokens,
        "completion_tokens": tracker.completion_tokens,
        "total_tokens": tracker.total_tokens,
        "cost_usd": tracker.cost(model),
        "elapsed_seconds": round(elapsed, 2),
        "model": model,
    }


# ---------------------------------------------------------------------------
# Method 4: Structured routing (NEW in v2)
# ---------------------------------------------------------------------------

def run_structured(question: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """Classify question type, then route to the appropriate pipeline.

    Routing:
    - CONCEPTUAL → CoT only (tools won't help for ethics/theory)
    - CALCULATION → forced tool pipeline (tool_choice="required" turn 1, then "auto")
    - MIXED → CoT + tool-augmented verification (same as cot_verify)
    """
    t0 = time.time()
    tracker = TokenTracker()

    # --- Phase 0: Classify question ---
    q_type = _classify_question(question, model, tracker)

    if q_type == "CONCEPTUAL":
        # --- Conceptual: pure CoT, no tools ---
        cot_response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": COT_SYSTEM},
                {"role": "user", "content": question},
            ],
            temperature=0,
            max_tokens=2000,
        )
        tracker.add(cot_response.usage)
        content = cot_response.choices[0].message.content or ""
        answer = extract_answer(content)

        elapsed = time.time() - t0
        return {
            "method": "structured",
            "answer": answer,
            "reasoning": content,
            "routing": "conceptual → cot",
            "question_type": q_type,
            "turns": 2,  # 1 classify + 1 cot
            "tool_calls": [],
            "prompt_tokens": tracker.prompt_tokens,
            "completion_tokens": tracker.completion_tokens,
            "total_tokens": tracker.total_tokens,
            "cost_usd": tracker.cost(model),
            "elapsed_seconds": round(elapsed, 2),
            "model": model,
        }

    elif q_type == "CALCULATION":
        # --- Calculation: forced tool pipeline ---
        calc_messages: List[dict] = [
            {"role": "system", "content": CALCULATION_SYSTEM},
            {"role": "user", "content": question},
        ]

        content, tool_calls, loop_turns = _run_tool_loop(
            calc_messages, model, tracker, max_turns=6,
            tool_choice_first="required",  # Force at least one tool call
            tool_choice_rest="auto",
        )
        answer = extract_answer(content)

        elapsed = time.time() - t0
        return {
            "method": "structured",
            "answer": answer,
            "reasoning": content,
            "routing": "calculation → forced_tools",
            "question_type": q_type,
            "turns": 1 + loop_turns,  # 1 classify + N tool loop
            "tool_calls": tool_calls,
            "prompt_tokens": tracker.prompt_tokens,
            "completion_tokens": tracker.completion_tokens,
            "total_tokens": tracker.total_tokens,
            "cost_usd": tracker.cost(model),
            "elapsed_seconds": round(elapsed, 2),
            "model": model,
        }

    else:
        # --- Mixed: CoT + tool-augmented verification ---
        # Phase 1: CoT
        cot_response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": COT_SYSTEM},
                {"role": "user", "content": question},
            ],
            temperature=0,
            max_tokens=2000,
        )
        tracker.add(cot_response.usage)
        cot_content = cot_response.choices[0].message.content or ""
        cot_answer = extract_answer(cot_content)

        # Phase 2: Verify with tools
        verify_prompt = (
            f"## Original Question\n{question}\n\n"
            f"## Proposed Answer: {cot_answer}\n\n"
            f"## Reasoning\n{cot_content}\n\n"
            f"Please verify this answer. Re-compute every calculation using your calculator tools."
        )
        verify_messages: List[dict] = [
            {"role": "system", "content": VERIFY_WITH_TOOLS_SYSTEM},
            {"role": "user", "content": verify_prompt},
        ]
        verify_content, tool_calls, verify_turns = _run_tool_loop(
            verify_messages, model, tracker, max_turns=4,
            tool_choice_first="auto", tool_choice_rest="auto",
        )
        verified_answer = extract_answer(verify_content)
        final_answer = verified_answer or cot_answer

        elapsed = time.time() - t0
        return {
            "method": "structured",
            "answer": final_answer,
            "reasoning": verify_content,
            "cot_answer": cot_answer,
            "cot_reasoning": cot_content,
            "answer_changed": (final_answer != cot_answer),
            "routing": "mixed → cot_verify",
            "question_type": q_type,
            "turns": 2 + verify_turns,  # 1 classify + 1 cot + N verify
            "tool_calls": tool_calls,
            "prompt_tokens": tracker.prompt_tokens,
            "completion_tokens": tracker.completion_tokens,
            "total_tokens": tracker.total_tokens,
            "cost_usd": tracker.cost(model),
            "elapsed_seconds": round(elapsed, 2),
            "model": model,
        }


# ---------------------------------------------------------------------------
# Method 5: Agent naive (v1, kept for comparison)
# ---------------------------------------------------------------------------

def run_agent_naive(question: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """v1 multi-turn agent: tool_choice="auto", model decides when to use tools.

    Kept as a baseline to show that passive tool availability doesn't work.
    In 90q test: 51.1% accuracy, only 8.9% tool usage.
    """
    t0 = time.time()
    tracker = TokenTracker()
    messages: List[dict] = [
        {"role": "system", "content": AGENT_NAIVE_SYSTEM},
        {"role": "user", "content": question},
    ]

    content, tool_calls, turns = _run_tool_loop(
        messages, model, tracker, max_turns=MAX_TURNS,
        tool_choice_first="auto", tool_choice_rest="auto",
    )

    elapsed = time.time() - t0
    return {
        "method": "agent_naive",
        "answer": extract_answer(content),
        "reasoning": content,
        "turns": turns,
        "tool_calls": tool_calls,
        "prompt_tokens": tracker.prompt_tokens,
        "completion_tokens": tracker.completion_tokens,
        "total_tokens": tracker.total_tokens,
        "cost_usd": tracker.cost(model),
        "elapsed_seconds": round(elapsed, 2),
        "model": model,
    }


# ---------------------------------------------------------------------------
# Method registry
# ---------------------------------------------------------------------------

METHODS = {
    "zero_shot": run_zero_shot,
    "cot": run_cot,
    "cot_verify": run_cot_verify,
    "structured": run_structured,
    "agent_naive": run_agent_naive,
}
