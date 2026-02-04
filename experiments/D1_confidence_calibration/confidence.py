"""Four confidence estimation methods for LLM calibration."""

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .config import SELF_CONSISTENCY_K, SC_TEMPERATURE, VALID_ANSWERS
from .llm_client import LLMClient, LLMResponse


@dataclass
class ConfidenceResult:
    """Result from a confidence estimation method."""

    method: str
    answer: Optional[str]
    confidence: float
    correct: Optional[bool] = None  # set after comparing to ground truth
    raw_response: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Answer extraction (reuses 5-level regex chain from cfa_agent/agent.py)
# ---------------------------------------------------------------------------

def extract_answer(text: str) -> Optional[str]:
    """Extract A/B/C answer from model response using a 5-level regex chain."""
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
    # 4. Standalone letter at end
    m = re.search(r"\b([A-C])\s*\.?\s*$", text.strip())
    if m:
        return m.group(1).upper()
    # 5. First standalone A/B/C anywhere
    m = re.search(r"\b([A-C])\b", text)
    if m:
        return m.group(1).upper()
    return None


def extract_confidence_number(text: str) -> Optional[float]:
    """Parse a confidence value from model output.

    Handles formats:
    - "Confidence: 85%"
    - "85% confident"
    - "0.85"
    - "85/100"
    - "My confidence is 85"
    """
    if not text:
        return None

    # Pattern 1: "Confidence: 85%" or "confidence level: 85%"
    m = re.search(r"confidence\s*(?:level)?\s*[:=]\s*(\d{1,3})(?:\s*%)?", text, re.IGNORECASE)
    if m:
        val = int(m.group(1))
        return val / 100.0 if val > 1 else float(val)

    # Pattern 2: "85% confident" or "85 percent"
    m = re.search(r"(\d{1,3})\s*(?:%|percent)\s*confident", text, re.IGNORECASE)
    if m:
        return int(m.group(1)) / 100.0

    # Pattern 3: "X/100"
    m = re.search(r"(\d{1,3})\s*/\s*100", text)
    if m:
        return int(m.group(1)) / 100.0

    # Pattern 4: decimal between 0 and 1 (e.g. "0.85")
    m = re.search(r"\b(0\.\d+)\b", text)
    if m:
        return float(m.group(1))

    # Pattern 5: standalone percentage anywhere (e.g. "85%")
    m = re.search(r"(\d{1,3})\s*%", text)
    if m:
        val = int(m.group(1))
        if 0 <= val <= 100:
            return val / 100.0

    # Pattern 6: bare number in confidence context (last resort)
    m = re.search(r"confidence.*?(\d{1,3})\b", text, re.IGNORECASE)
    if m:
        val = int(m.group(1))
        if 0 <= val <= 100:
            return val / 100.0

    return None


# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

VERBALIZED_SYSTEM = """You are a CFA exam expert. Answer the multiple-choice question below.

After your analysis:
1. State your final answer as: ANSWER: X (where X is A, B, or C)
2. State your confidence as: Confidence: N% (where N is 0-100)

Be honest about your confidence. If you are uncertain, say so with a lower percentage.
Do not default to round numbers unless you genuinely feel that level of confidence."""

LOGIT_SYSTEM = """You are a CFA exam expert. Read the question carefully and output ONLY the letter of the correct answer: A, B, or C.
Do not explain. Output a single letter."""


# ---------------------------------------------------------------------------
# Method 1: Verbalized confidence
# ---------------------------------------------------------------------------

def verbalized_confidence(
    client: LLMClient,
    question: str,
) -> ConfidenceResult:
    """Ask model to self-rate confidence 0-100%."""
    messages = [
        {"role": "system", "content": VERBALIZED_SYSTEM},
        {"role": "user", "content": question},
    ]
    resp = client.chat(messages, temperature=0.0, max_tokens=2000)
    answer = extract_answer(resp.content)
    confidence = extract_confidence_number(resp.content)

    if confidence is None:
        confidence = 0.5  # fallback
        parse_failed = True
    else:
        confidence = max(0.0, min(1.0, confidence))
        parse_failed = False

    return ConfidenceResult(
        method="verbalized",
        answer=answer,
        confidence=confidence,
        raw_response=resp.content,
        metadata={
            "parse_failed": parse_failed,
            "prompt_tokens": resp.prompt_tokens,
            "completion_tokens": resp.completion_tokens,
            "elapsed": resp.elapsed,
            "model": client.name,
        },
    )


# ---------------------------------------------------------------------------
# Method 2: Self-consistency (majority vote)
# ---------------------------------------------------------------------------

def self_consistency(
    client: LLMClient,
    question: str,
    k: int = SELF_CONSISTENCY_K,
) -> ConfidenceResult:
    """Sample k responses at temperature=0.7, confidence = majority ratio."""
    messages = [
        {"role": "system", "content": VERBALIZED_SYSTEM},
        {"role": "user", "content": question},
    ]

    answers: List[Optional[str]] = []
    total_prompt = 0
    total_completion = 0
    total_elapsed = 0.0

    for _ in range(k):
        resp = client.chat(messages, temperature=SC_TEMPERATURE, max_tokens=2000)
        ans = extract_answer(resp.content)
        answers.append(ans)
        total_prompt += resp.prompt_tokens
        total_completion += resp.completion_tokens
        total_elapsed += resp.elapsed

    # Count valid answers only
    valid = [a for a in answers if a in VALID_ANSWERS]
    if not valid:
        return ConfidenceResult(
            method="self_consistency",
            answer=None,
            confidence=0.0,
            metadata={
                "k": k,
                "answers": answers,
                "prompt_tokens": total_prompt,
                "completion_tokens": total_completion,
                "elapsed": round(total_elapsed, 2),
                "model": client.name,
            },
        )

    counter = Counter(valid)
    majority_answer, majority_count = counter.most_common(1)[0]
    confidence = majority_count / k  # ratio out of all k samples

    return ConfidenceResult(
        method="self_consistency",
        answer=majority_answer,
        confidence=round(confidence, 4),
        metadata={
            "k": k,
            "answers": answers,
            "vote_distribution": dict(counter),
            "prompt_tokens": total_prompt,
            "completion_tokens": total_completion,
            "elapsed": round(total_elapsed, 2),
            "model": client.name,
        },
    )


# ---------------------------------------------------------------------------
# Method 3: Logit-based confidence (Ollama only)
# ---------------------------------------------------------------------------

def logit_confidence(
    client: LLMClient,
    question: str,
) -> ConfidenceResult:
    """Extract P(answer token) from logprobs. Ollama models only."""
    if not client.supports_logprobs:
        return ConfidenceResult(
            method="logit",
            answer=None,
            confidence=0.0,
            metadata={"error": "Model does not support logprobs", "model": client.name},
        )

    messages = [
        {"role": "system", "content": LOGIT_SYSTEM},
        {"role": "user", "content": question},
    ]
    resp = client.chat_with_logprobs(messages, temperature=0.0, max_tokens=10)

    # Extract answer from content
    content = resp.content.strip()
    answer = _extract_bare_letter(content)
    if answer is None:
        answer = extract_answer(content)

    # Extract logprob for the answer token
    confidence = 0.0
    token_info = None

    if resp.logprobs:
        for entry in resp.logprobs:
            token_text = entry.get("token", "").strip().upper()
            if token_text in VALID_ANSWERS:
                confidence = entry.get("prob", 0.0)
                token_info = entry
                # Use the logprob answer if content parsing was ambiguous
                if answer is None:
                    answer = token_text
                break

    return ConfidenceResult(
        method="logit",
        answer=answer,
        confidence=round(confidence, 6),
        raw_response=content,
        metadata={
            "logprobs": resp.logprobs,
            "matched_token": token_info,
            "prompt_tokens": resp.prompt_tokens,
            "completion_tokens": resp.completion_tokens,
            "elapsed": resp.elapsed,
            "model": client.name,
        },
    )


def _extract_bare_letter(text: str) -> Optional[str]:
    """Extract a bare A/B/C from very short output (logit prompt)."""
    cleaned = text.strip().upper().rstrip(".")
    if cleaned in VALID_ANSWERS:
        return cleaned
    # Handle " A" or "A\n" etc.
    for char in cleaned:
        if char in ("A", "B", "C"):
            return char
    return None


# ---------------------------------------------------------------------------
# Method 4: Ensemble disagreement
# ---------------------------------------------------------------------------

def ensemble_disagreement(
    clients: Dict[str, LLMClient],
    question: str,
) -> ConfidenceResult:
    """Run all models, confidence = agreement ratio among voters."""
    messages = [
        {"role": "system", "content": VERBALIZED_SYSTEM},
        {"role": "user", "content": question},
    ]

    per_model: Dict[str, Dict[str, Any]] = {}
    answers: List[Optional[str]] = []

    for model_name, client in clients.items():
        resp = client.chat(messages, temperature=0.0, max_tokens=2000)
        ans = extract_answer(resp.content)
        answers.append(ans)
        per_model[model_name] = {
            "answer": ans,
            "confidence": extract_confidence_number(resp.content),
            "prompt_tokens": resp.prompt_tokens,
            "completion_tokens": resp.completion_tokens,
            "elapsed": resp.elapsed,
        }

    # Compute agreement
    valid = [a for a in answers if a in VALID_ANSWERS]
    if not valid:
        return ConfidenceResult(
            method="ensemble",
            answer=None,
            confidence=0.0,
            metadata={"per_model": per_model},
        )

    counter = Counter(valid)
    majority_answer, majority_count = counter.most_common(1)[0]
    confidence = majority_count / len(clients)  # ratio out of all models

    return ConfidenceResult(
        method="ensemble",
        answer=majority_answer,
        confidence=round(confidence, 4),
        metadata={
            "per_model": per_model,
            "vote_distribution": dict(counter),
            "n_models": len(clients),
        },
    )
