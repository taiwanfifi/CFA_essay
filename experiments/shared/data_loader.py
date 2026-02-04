"""
Shared data loader for CFA datasets.

Provides unified access to:
- CFA_Challenge (90 questions, hard)
- CFA_Easy (1,032 questions, standard)
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# Project root (two levels up from shared/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATASETS_DIR = PROJECT_ROOT / "datasets" / "FinEval"


def load_cfa_challenge(limit: int = 0) -> List[Dict[str, Any]]:
    """Load CFA-Challenge dataset (90 questions).

    Schema: {"query": str, "answer": str, "source": str}
    """
    path = DATASETS_DIR / "CFA_Challenge" / "data.json"
    if not path.exists():
        raise FileNotFoundError(f"CFA-Challenge data not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    items = []
    for i, entry in enumerate(raw):
        items.append({
            "id": f"challenge_{i}",
            "query": entry["query"],
            "answer": entry["answer"].strip().upper(),
            "source": entry.get("source", ""),
            "dataset": "CFA_Challenge",
        })
    if limit > 0:
        items = items[:limit]
    return items


def load_cfa_easy(limit: int = 0) -> List[Dict[str, Any]]:
    """Load CFA-Easy dataset (1,032 questions).

    Schema: {"query": str, "answer": str, "text": str, "choices": list, "gold": int}
    """
    path = DATASETS_DIR / "CFA_Easy" / "data.json"
    if not path.exists():
        raise FileNotFoundError(f"CFA-Easy data not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    items = []
    for i, entry in enumerate(raw):
        items.append({
            "id": f"easy_{i}",
            "query": entry["query"],
            "answer": entry["answer"].strip().upper(),
            "text": entry.get("text", ""),
            "choices": entry.get("choices", []),
            "dataset": "CFA_Easy",
        })
    if limit > 0:
        items = items[:limit]
    return items


def load_dataset(name: str, limit: int = 0) -> List[Dict[str, Any]]:
    """Load dataset by name.

    Args:
        name: "challenge", "easy", or "both"
        limit: Max questions per dataset (0 = all)
    """
    if name == "challenge":
        return load_cfa_challenge(limit)
    elif name == "easy":
        return load_cfa_easy(limit)
    elif name == "cra_bigdata":
        return load_cra_bigdata(limit)
    elif name == "both":
        challenge = load_cfa_challenge(limit)
        easy = load_cfa_easy(limit)
        return challenge + easy
    else:
        raise ValueError(
            f"Unknown dataset: {name}. "
            "Use 'challenge', 'easy', 'cra_bigdata', or 'both'."
        )


def load_cfa_easy_with_choices(limit: int = 0) -> List[Dict[str, Any]]:
    """Load CFA-Easy dataset preserving the raw choices text.

    Returns items with an additional 'choices_text' field containing
    the individual option strings (A: ..., B: ..., C: ...) parsed
    from the query.
    """
    items = load_cfa_easy(limit)
    for item in items:
        item["choices_text"] = _parse_choices_from_query(item["query"])
    return items


def load_cra_bigdata(limit: int = 0) -> List[Dict[str, Any]]:
    """Load CRA-Bigdata dataset (1,472 questions).

    Schema: {"id": str, "query": str, "answer": str, "text": str, "choices": list, "gold": int}
    """
    path = DATASETS_DIR / "CRA_Bigdata" / "data.json"
    if not path.exists():
        raise FileNotFoundError(f"CRA-Bigdata data not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    items = []
    for entry in raw:
        items.append({
            "id": entry.get("id", f"cra_{len(items)}"),
            "query": entry["query"],
            "answer": entry["answer"].strip(),
            "text": entry.get("text", ""),
            "choices": entry.get("choices", []),
            "dataset": "CRA_Bigdata",
        })
    if limit > 0:
        items = items[:limit]
    return items


def load_experiment_results(path: str) -> Dict[str, Any]:
    """Load experiment results JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_choices_from_query(query: str) -> List[str]:
    """Parse choice options from a CFA query string.

    Extracts text after 'CHOICES:' and splits on 'A:', 'B:', 'C:'.
    Returns list of choice strings e.g. ['7.5% compounded...', '7.7%...', '8.0%...']
    """
    import re
    # Find the CHOICES section
    m = re.search(r"CHOICES:\s*(.*?)(?:\s*Answer:|$)", query, re.DOTALL)
    if not m:
        return []
    choices_text = m.group(1).strip()
    # Split on A:, B:, C: patterns
    parts = re.split(r"[A-C]\s*:", choices_text)
    # First element is empty or pre-text, skip it
    choices = [p.strip().rstrip(".,") for p in parts[1:] if p.strip()]
    return choices
