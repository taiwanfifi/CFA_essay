"""Calibration metrics: ECE, MCE, Brier Score, AUROC, coverage-accuracy."""

import math
from typing import Any, Dict, List, Optional, Tuple

from .config import CALIBRATION_BINS


def compute_ece(
    confidences: List[float],
    correctness: List[bool],
    n_bins: int = CALIBRATION_BINS,
) -> Tuple[float, List[Dict[str, Any]]]:
    """Compute Expected Calibration Error.

    Returns (ece_value, bin_details) where bin_details is a list of dicts
    with keys: bin_lower, bin_upper, avg_confidence, avg_accuracy, count, gap.
    """
    if not confidences:
        return 0.0, []

    n = len(confidences)
    bin_details = []
    weighted_error = 0.0

    for i in range(n_bins):
        bin_lower = i / n_bins
        bin_upper = (i + 1) / n_bins

        # Collect samples in this bin
        indices = [
            j for j in range(n)
            if (bin_lower <= confidences[j] < bin_upper)
            or (i == n_bins - 1 and confidences[j] == bin_upper)
        ]

        count = len(indices)
        if count == 0:
            bin_details.append({
                "bin_lower": round(bin_lower, 2),
                "bin_upper": round(bin_upper, 2),
                "avg_confidence": 0.0,
                "avg_accuracy": 0.0,
                "count": 0,
                "gap": 0.0,
            })
            continue

        avg_conf = sum(confidences[j] for j in indices) / count
        avg_acc = sum(1 for j in indices if correctness[j]) / count
        gap = abs(avg_acc - avg_conf)

        weighted_error += (count / n) * gap

        bin_details.append({
            "bin_lower": round(bin_lower, 2),
            "bin_upper": round(bin_upper, 2),
            "avg_confidence": round(avg_conf, 4),
            "avg_accuracy": round(avg_acc, 4),
            "count": count,
            "gap": round(gap, 4),
        })

    return round(weighted_error, 6), bin_details


def compute_mce(
    confidences: List[float],
    correctness: List[bool],
    n_bins: int = CALIBRATION_BINS,
) -> float:
    """Compute Maximum Calibration Error (worst-bin gap)."""
    _, bin_details = compute_ece(confidences, correctness, n_bins)
    gaps = [b["gap"] for b in bin_details if b["count"] > 0]
    return round(max(gaps), 6) if gaps else 0.0


def compute_brier_score(
    confidences: List[float],
    correctness: List[bool],
) -> float:
    """Compute Brier Score = mean((confidence - correct)^2).

    Lower is better. 0.0 = perfect, 0.25 = random baseline for binary.
    """
    if not confidences:
        return 0.0
    n = len(confidences)
    total = sum((c - (1.0 if correct else 0.0)) ** 2
                for c, correct in zip(confidences, correctness))
    return round(total / n, 6)


def compute_auroc(
    confidences: List[float],
    correctness: List[bool],
) -> Optional[float]:
    """Compute Area Under ROC Curve for confidence as a correctness predictor.

    Returns None if all labels are the same (AUROC undefined).
    Uses the trapezoidal rule on sorted thresholds.
    """
    n = len(confidences)
    if n == 0:
        return None

    n_pos = sum(1 for c in correctness if c)
    n_neg = n - n_pos

    if n_pos == 0 or n_neg == 0:
        return None

    # Sort by confidence descending
    pairs = sorted(zip(confidences, correctness), key=lambda x: -x[0])

    tp = 0
    fp = 0
    auc = 0.0
    prev_fpr = 0.0
    prev_tpr = 0.0

    for conf, correct in pairs:
        if correct:
            tp += 1
        else:
            fp += 1
        tpr = tp / n_pos
        fpr = fp / n_neg
        # Trapezoidal rule
        auc += (fpr - prev_fpr) * (tpr + prev_tpr) / 2
        prev_fpr = fpr
        prev_tpr = tpr

    return round(auc, 6)


def compute_coverage_accuracy_curve(
    confidences: List[float],
    correctness: List[bool],
    thresholds: Optional[List[float]] = None,
) -> List[Dict[str, Any]]:
    """Compute coverage-accuracy at various confidence thresholds.

    For each threshold t, coverage = fraction of items with confidence >= t,
    accuracy = fraction correct among those items.

    Returns list of {threshold, coverage, accuracy, n_covered}.
    """
    if thresholds is None:
        thresholds = [round(i * 0.05, 2) for i in range(21)]  # 0.0 to 1.0

    n = len(confidences)
    if n == 0:
        return [{"threshold": t, "coverage": 0.0, "accuracy": 0.0, "n_covered": 0}
                for t in thresholds]

    results = []
    for t in thresholds:
        covered = [(c, correct) for c, correct in zip(confidences, correctness) if c >= t]
        n_covered = len(covered)
        coverage = n_covered / n
        accuracy = (sum(1 for _, correct in covered if correct) / n_covered) if n_covered > 0 else 0.0

        results.append({
            "threshold": round(t, 2),
            "coverage": round(coverage, 4),
            "accuracy": round(accuracy, 4),
            "n_covered": n_covered,
        })

    return results


def compute_all_metrics(
    confidences: List[float],
    correctness: List[bool],
    n_bins: int = CALIBRATION_BINS,
) -> Dict[str, Any]:
    """Compute all calibration metrics in a single call.

    Returns a JSON-serializable dict with all metrics.
    """
    ece, bin_details = compute_ece(confidences, correctness, n_bins)
    mce = compute_mce(confidences, correctness, n_bins)
    brier = compute_brier_score(confidences, correctness)
    auroc = compute_auroc(confidences, correctness)
    coverage_curve = compute_coverage_accuracy_curve(confidences, correctness)

    n = len(confidences)
    n_correct = sum(1 for c in correctness if c)
    accuracy = n_correct / n if n > 0 else 0.0
    avg_confidence = sum(confidences) / n if n > 0 else 0.0

    return {
        "n": n,
        "accuracy": round(accuracy, 4),
        "avg_confidence": round(avg_confidence, 4),
        "ece": ece,
        "mce": mce,
        "brier_score": brier,
        "auroc": auroc,
        "overconfidence_gap": round(avg_confidence - accuracy, 4),
        "bins": bin_details,
        "coverage_accuracy_curve": coverage_curve,
    }
