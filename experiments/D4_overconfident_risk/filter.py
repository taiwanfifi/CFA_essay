"""Filter overconfident errors from D1 calibration results."""

import json
import glob
from pathlib import Path
from typing import Any, Dict, List


def load_d1_results(input_paths: List[str]) -> List[Dict[str, Any]]:
    """Load and merge D1 calibration results from one or more files.

    Handles glob patterns in paths.
    """
    all_results = []
    expanded_paths = []
    for pattern in input_paths:
        expanded_paths.extend(glob.glob(pattern))

    if not expanded_paths:
        raise FileNotFoundError(
            f"No D1 result files found matching: {input_paths}"
        )

    for path in expanded_paths:
        with open(path, "r") as f:
            data = json.load(f)
        results = data.get("results", [])
        metadata = data.get("metadata", {})
        # Tag each result with its source
        for r in results:
            r["_source_file"] = path
            r["_model"] = metadata.get("model", "unknown")
        all_results.extend(results)

    return all_results


def filter_overconfident_errors(
    results: List[Dict[str, Any]],
    confidence_threshold: float = 0.8,
) -> List[Dict[str, Any]]:
    """Filter for high-confidence incorrect answers.

    Looks for results where:
    - correct == False
    - confidence >= threshold (from any method)

    Returns filtered results sorted by confidence (descending).
    """
    overconfident = []

    for r in results:
        if r.get("correct", True):
            continue  # Skip correct answers

        # Check confidence from different methods
        confidence = _get_max_confidence(r)
        if confidence is None or confidence < confidence_threshold:
            continue

        overconfident.append({
            "question_id": r.get("question_id", r.get("id", "?")),
            "question": r.get("question", r.get("query", "")),
            "correct_answer": r.get("correct_answer", r.get("gold_answer", "")),
            "model_answer": r.get("answer", r.get("model_answer", "")),
            "confidence": confidence,
            "confidence_method": r.get("method", "unknown"),
            "reasoning": r.get("reasoning", r.get("response", "")),
            "model": r.get("_model", "unknown"),
            "source_file": r.get("_source_file", ""),
        })

    overconfident.sort(key=lambda x: x["confidence"], reverse=True)
    return overconfident


def _get_max_confidence(result: Dict[str, Any]) -> float | None:
    """Extract the highest confidence value from a D1 result entry.

    D1 results may store confidence in different fields depending on the method.
    """
    candidates = []

    # Direct confidence field
    if "confidence" in result and result["confidence"] is not None:
        try:
            candidates.append(float(result["confidence"]))
        except (ValueError, TypeError):
            pass

    # Verbalized confidence
    if "verbalized_confidence" in result:
        try:
            candidates.append(float(result["verbalized_confidence"]))
        except (ValueError, TypeError):
            pass

    # Self-consistency confidence
    if "sc_confidence" in result:
        try:
            candidates.append(float(result["sc_confidence"]))
        except (ValueError, TypeError):
            pass

    # Logit confidence
    if "logit_confidence" in result:
        try:
            candidates.append(float(result["logit_confidence"]))
        except (ValueError, TypeError):
            pass

    return max(candidates) if candidates else None


def detect_collective_hallucination(
    overconfident_errors: List[Dict[str, Any]],
    min_models: int = 2,
) -> List[Dict[str, Any]]:
    """Find questions where multiple models are overconfident AND wrong.

    These are "collective hallucinations" — especially dangerous because
    ensemble or voting methods would also fail.
    """
    # Group by question_id
    by_question: Dict[str, List[Dict]] = {}
    for entry in overconfident_errors:
        qid = entry["question_id"]
        by_question.setdefault(qid, []).append(entry)

    collective = []
    for qid, entries in by_question.items():
        models = set(e["model"] for e in entries)
        if len(models) >= min_models:
            collective.append({
                "question_id": qid,
                "n_models": len(models),
                "models": list(models),
                "avg_confidence": sum(e["confidence"] for e in entries) / len(entries),
                "entries": entries,
            })

    collective.sort(key=lambda x: x["n_models"], reverse=True)
    return collective
