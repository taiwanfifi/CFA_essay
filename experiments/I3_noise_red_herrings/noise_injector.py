"""Noise injection engine for I3 experiment.

Four noise types:
  N1 — Irrelevant data injection (random facts spliced into question)
  N2 — Plausible financial distractors (related-sounding but irrelevant)
  N3 — Verbose padding (wordy preamble/postamble)
  N4 — Contradictory hints (subtly misleading cues)
"""

import random
from typing import List

from .config import N1_SNIPPETS, N2_SNIPPETS, N3_TEMPLATES, N4_TEMPLATES


def inject_noise(
    query: str,
    noise_type: str,
    intensity: int = 2,
    correct_answer: str = "",
    seed: int = 42,
) -> str:
    """Inject noise into a CFA question.

    Args:
        query: Original question text.
        noise_type: One of "N1", "N2", "N3", "N4".
        intensity: Number of noise snippets to inject (1-4).
        correct_answer: The correct answer letter (needed for N4).
        seed: Random seed for reproducibility.

    Returns:
        Modified question with noise injected.
    """
    rng = random.Random(seed)
    intensity = max(1, min(intensity, 4))

    if noise_type == "N1":
        return _inject_n1(query, intensity, rng)
    elif noise_type == "N2":
        return _inject_n2(query, intensity, rng)
    elif noise_type == "N3":
        return _inject_n3(query, intensity, rng)
    elif noise_type == "N4":
        return _inject_n4(query, correct_answer, intensity, rng)
    else:
        raise ValueError(f"Unknown noise type: {noise_type}. Use N1, N2, N3, or N4.")


def _find_injection_point(query: str) -> int:
    """Find a natural injection point in the middle of the question."""
    # Try to inject before the last sentence (before "The PV..." or similar)
    sentences = query.split(".")
    if len(sentences) >= 3:
        # Insert before the last substantive sentence
        rejoin = ".".join(sentences[:-2]) + "."
        return len(rejoin)

    # Fallback: insert at roughly the middle
    mid = len(query) // 2
    # Find the nearest period or comma
    for offset in range(20):
        for pos in [mid + offset, mid - offset]:
            if 0 <= pos < len(query) and query[pos] in ".,:;":
                return pos + 1
    return mid


def _inject_n1(query: str, intensity: int, rng: random.Random) -> str:
    """N1: Inject irrelevant data snippets."""
    snippets = rng.sample(N1_SNIPPETS, min(intensity, len(N1_SNIPPETS)))
    noise_block = " ".join(snippets)
    pos = _find_injection_point(query)
    return query[:pos] + " " + noise_block + " " + query[pos:]


def _inject_n2(query: str, intensity: int, rng: random.Random) -> str:
    """N2: Inject plausible financial distractors."""
    snippets = rng.sample(N2_SNIPPETS, min(intensity, len(N2_SNIPPETS)))
    noise_block = " ".join(snippets)
    pos = _find_injection_point(query)
    return query[:pos] + " " + noise_block + " " + query[pos:]


def _inject_n3(query: str, intensity: int, rng: random.Random) -> str:
    """N3: Add verbose padding as preamble."""
    templates = rng.sample(N3_TEMPLATES, min(intensity, len(N3_TEMPLATES)))
    preamble = " ".join(templates)
    return preamble + "\n\n" + query


def _inject_n4(query: str, correct_answer: str, intensity: int, rng: random.Random) -> str:
    """N4: Insert contradictory hints pointing to wrong answers."""
    wrong_answers = [a for a in ["A", "B", "C"] if a != correct_answer.upper()]
    hints = []
    for i in range(min(intensity, len(N4_TEMPLATES))):
        wrong = rng.choice(wrong_answers)
        template = N4_TEMPLATES[i % len(N4_TEMPLATES)]
        hints.append(template.format(wrong_answer=wrong))

    hint_block = " ".join(hints)
    return query + "\n\n" + hint_block


def get_available_noise_types() -> List[str]:
    """Return list of available noise type codes."""
    return ["N1", "N2", "N3", "N4"]
