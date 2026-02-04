"""Visualization: reliability diagrams, coverage-accuracy curves, histograms."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def plot_reliability_diagram(
    bin_details: List[Dict[str, Any]],
    ece: float,
    title: str = "Reliability Diagram",
    output_path: Optional[str] = None,
) -> str:
    """Plot a reliability diagram with gap shading.

    Red bars = overconfident (confidence > accuracy).
    Green bars = underconfident (accuracy > confidence).
    """
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    bins_with_data = [b for b in bin_details if b["count"] > 0]
    if not bins_with_data:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=14)
        ax.set_title(title)
        path = _save_fig(fig, output_path, "reliability_diagram.png")
        plt.close(fig)
        return path

    # Perfect calibration line
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Perfect calibration")

    # Bars
    width = 1.0 / len(bin_details)
    for b in bin_details:
        x = (b["bin_lower"] + b["bin_upper"]) / 2
        acc = b["avg_accuracy"]
        conf = b["avg_confidence"]
        count = b["count"]

        if count == 0:
            continue

        # Accuracy bar
        ax.bar(x, acc, width=width * 0.85, color="#4C72B0", alpha=0.8, edgecolor="white")

        # Gap shading
        if conf > acc:
            # Overconfident: red
            ax.bar(x, conf - acc, bottom=acc, width=width * 0.85,
                   color="#C44E52", alpha=0.35, edgecolor="none")
        elif acc > conf:
            # Underconfident: green
            ax.bar(x, acc - conf, bottom=conf, width=width * 0.85,
                   color="#55A868", alpha=0.35, edgecolor="none")

    # Annotations
    ax.set_xlabel("Confidence", fontsize=12)
    ax.set_ylabel("Accuracy", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Legend
    acc_patch = mpatches.Patch(color="#4C72B0", alpha=0.8, label="Accuracy")
    over_patch = mpatches.Patch(color="#C44E52", alpha=0.35, label="Overconfident gap")
    under_patch = mpatches.Patch(color="#55A868", alpha=0.35, label="Underconfident gap")
    ax.legend(handles=[acc_patch, over_patch, under_patch], loc="upper left", fontsize=10)

    # ECE text box
    textstr = f"ECE = {ece:.4f}"
    props = dict(boxstyle="round", facecolor="wheat", alpha=0.8)
    ax.text(0.95, 0.05, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment="bottom", horizontalalignment="right", bbox=props)

    # Sample count annotation on each bar
    for b in bin_details:
        if b["count"] > 0:
            x = (b["bin_lower"] + b["bin_upper"]) / 2
            ax.text(x, b["avg_accuracy"] + 0.02, str(b["count"]),
                    ha="center", va="bottom", fontsize=8, color="gray")

    plt.tight_layout()
    path = _save_fig(fig, output_path, "reliability_diagram.png")
    plt.close(fig)
    return path


def plot_coverage_accuracy_curve(
    curves: Dict[str, List[Dict[str, Any]]],
    title: str = "Coverage-Accuracy Curve",
    output_path: Optional[str] = None,
) -> str:
    """Plot coverage-accuracy curves for multiple methods on one figure.

    Args:
        curves: dict mapping method_name -> list of {threshold, coverage, accuracy}.
    """
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    colors = ["#4C72B0", "#C44E52", "#55A868", "#8172B2", "#CCB974", "#64B5CD"]

    for idx, (method, points) in enumerate(curves.items()):
        coverages = [p["coverage"] for p in points]
        accuracies = [p["accuracy"] for p in points]
        color = colors[idx % len(colors)]
        ax.plot(coverages, accuracies, "-o", label=method, color=color,
                markersize=3, linewidth=1.5)

    ax.set_xlabel("Coverage (fraction of questions answered)", fontsize=12)
    ax.set_ylabel("Accuracy (on answered questions)", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = _save_fig(fig, output_path, "coverage_accuracy.png")
    plt.close(fig)
    return path


def plot_confidence_histogram(
    confidences: List[float],
    title: str = "Confidence Distribution",
    output_path: Optional[str] = None,
) -> str:
    """Plot histogram of confidence values (diagnose spike problem)."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    ax.hist(confidences, bins=20, range=(0, 1), color="#4C72B0", alpha=0.8,
            edgecolor="white")

    mean_conf = np.mean(confidences) if confidences else 0
    ax.axvline(mean_conf, color="#C44E52", linestyle="--", linewidth=1.5,
               label=f"Mean = {mean_conf:.2f}")

    ax.set_xlabel("Confidence", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=10)
    ax.set_xlim(0, 1)

    plt.tight_layout()
    path = _save_fig(fig, output_path, "confidence_histogram.png")
    plt.close(fig)
    return path


def _save_fig(fig, output_path: Optional[str], default_name: str) -> str:
    """Save figure to output_path or default location."""
    if output_path:
        path = output_path
    else:
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(exist_ok=True)
        path = str(results_dir / default_name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    return path
