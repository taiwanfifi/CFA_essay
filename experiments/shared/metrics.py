"""
Shared evaluation metrics for CFA experiments.
"""

from typing import Any, Dict, List, Optional
from collections import Counter


def accuracy(results: List[Dict[str, Any]], key: str = "correct") -> float:
    """Calculate accuracy from results."""
    if not results:
        return 0.0
    return sum(1 for r in results if r.get(key)) / len(results)


def accuracy_by_group(
    results: List[Dict[str, Any]],
    group_key: str,
    correct_key: str = "correct"
) -> Dict[str, Dict[str, Any]]:
    """Calculate accuracy grouped by a key (e.g., topic, error_type).

    Returns:
        {group_value: {"n": count, "correct": correct_count, "accuracy": float}}
    """
    groups: Dict[str, List[Dict]] = {}
    for r in results:
        group = r.get(group_key, "unknown")
        groups.setdefault(group, []).append(r)

    summary = {}
    for group, items in groups.items():
        n = len(items)
        correct = sum(1 for r in items if r.get(correct_key))
        summary[group] = {
            "n": n,
            "correct": correct,
            "accuracy": correct / n if n > 0 else 0.0,
        }
    return summary


def confusion_matrix(
    results: List[Dict[str, Any]],
    pred_key: str = "answer",
    gold_key: str = "correct_answer"
) -> Dict[str, Dict[str, int]]:
    """Build confusion matrix from results.

    Returns:
        {gold_answer: {pred_answer: count}}
    """
    matrix: Dict[str, Dict[str, int]] = {}
    for r in results:
        gold = r.get(gold_key, "?")
        pred = r.get(pred_key, "?")
        if gold not in matrix:
            matrix[gold] = {}
        matrix[gold][pred] = matrix[gold].get(pred, 0) + 1
    return matrix


def error_rate_by_category(
    results: List[Dict[str, Any]],
    category_key: str,
    correct_key: str = "correct"
) -> List[Dict[str, Any]]:
    """Calculate error rates by category, sorted by error rate descending.

    Returns:
        [{"category": str, "n": int, "errors": int, "error_rate": float}, ...]
    """
    groups = accuracy_by_group(results, category_key, correct_key)

    ranked = []
    for cat, stats in groups.items():
        ranked.append({
            "category": cat,
            "n": stats["n"],
            "errors": stats["n"] - stats["correct"],
            "error_rate": 1.0 - stats["accuracy"],
        })

    return sorted(ranked, key=lambda x: x["error_rate"], reverse=True)
