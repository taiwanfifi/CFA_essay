#!/usr/bin/env python3
"""
D1+D4 Paper Analysis: Comprehensive calibration analysis and figure generation.
Processes existing D1 experiment results to produce publication-quality outputs.

Usage:
    python drafts/selected/D1_calibration/run_analysis.py
"""
import json
import os
import sys
import math
import warnings
from collections import defaultdict
from pathlib import Path

import numpy as np

# Suppress warnings for clean output
warnings.filterwarnings("ignore")

# ============================================================
# Configuration
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
D1_RESULTS_DIR = PROJECT_ROOT / "experiments" / "D1_confidence_calibration" / "results"
D4_RESULTS_DIR = PROJECT_ROOT / "experiments" / "D4_overconfident_risk" / "results"
OUTPUT_DIR = Path(__file__).resolve().parent
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"

FIGURES_DIR.mkdir(exist_ok=True)
TABLES_DIR.mkdir(exist_ok=True)

# Confidence threshold for "overconfident error"
OVERCONF_THRESHOLD = 0.80

# CFA topic keywords for classification
CFA_TOPIC_KEYWORDS = {
    "Ethics & Standards": [
        "ethics", "standard", "professional conduct", "fiduciary", "cfa institute",
        "misrepresentation", "diligence", "suitability", "priority of transactions",
        "confidentiality", "loyalty", "prudence", "duty", "compliance", "violation",
        "code of ethics", "soft dollar", "mosaic theory"
    ],
    "Quantitative Methods": [
        "probability", "regression", "hypothesis test", "confidence interval",
        "standard deviation", "variance", "correlation", "time series",
        "monte carlo", "sampling", "z-score", "t-test", "chi-square",
        "normal distribution", "bayes", "expected value", "covariance"
    ],
    "Economics": [
        "gdp", "inflation", "monetary policy", "fiscal policy", "exchange rate",
        "interest rate", "aggregate demand", "supply curve", "elasticity",
        "unemployment", "central bank", "business cycle", "trade deficit",
        "comparative advantage", "balance of payments"
    ],
    "Financial Reporting": [
        "financial statement", "balance sheet", "income statement", "cash flow",
        "depreciation", "amortization", "goodwill", "inventory", "revenue recognition",
        "deferred tax", "earnings per share", "eps", "gaap", "ifrs",
        "operating income", "net income", "retained earnings", "liabilities"
    ],
    "Corporate Finance": [
        "capital budgeting", "npv", "irr", "wacc", "cost of capital",
        "capital structure", "dividend", "share repurchase", "roe", "roa",
        "leverage", "merger", "acquisition", "corporate governance"
    ],
    "Equity": [
        "stock", "equity valuation", "p/e ratio", "price-to-book",
        "dividend discount", "free cash flow", "gordon growth",
        "market capitalization", "earnings growth", "equity risk premium"
    ],
    "Fixed Income": [
        "bond", "duration", "convexity", "yield", "coupon", "maturity",
        "credit spread", "treasury", "interest rate risk", "oas",
        "callable", "putable", "zero-coupon", "yield curve", "fixed income",
        "credit risk", "default", "recovery rate", "high-yield", "investment-grade"
    ],
    "Derivatives": [
        "option", "futures", "forward", "swap", "put", "call",
        "strike price", "expiration", "black-scholes", "delta", "gamma",
        "vega", "theta", "hedging", "collar", "straddle", "protective put"
    ],
    "Alternative Investments": [
        "private equity", "hedge fund", "real estate", "commodity",
        "venture capital", "buyout", "infrastructure", "reit"
    ],
    "Portfolio Management": [
        "portfolio", "asset allocation", "diversification", "efficient frontier",
        "capm", "beta", "alpha", "sharpe ratio", "information ratio",
        "tracking error", "benchmark", "rebalancing", "risk-return",
        "mean-variance", "strategic asset", "tactical asset"
    ],
}


def classify_topic(query_text: str) -> str:
    """Classify a CFA question into a topic based on keyword matching."""
    text_lower = query_text.lower()
    scores = {}
    for topic, keywords in CFA_TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[topic] = score
    if not scores:
        return "Other"
    return max(scores, key=scores.get)


# ============================================================
# Data Loading
# ============================================================
def load_all_d1_results():
    """Load all D1 result files and merge."""
    all_results = []
    all_metrics = {}
    metadata_list = []

    for run_dir in sorted(D1_RESULTS_DIR.iterdir()):
        results_file = run_dir / "results.json"
        if not results_file.exists():
            continue
        with open(results_file) as f:
            data = json.load(f)
        metadata_list.append(data.get("metadata", {}))
        for key, val in data.get("metrics", {}).items():
            all_metrics[key] = val
        for r in data.get("results", []):
            all_results.append(r)

    print(f"Loaded {len(all_results)} results from {len(metadata_list)} runs")
    print(f"Metrics keys: {list(all_metrics.keys())}")
    return all_results, all_metrics


def load_d4_results():
    """Load D4 overconfident risk results."""
    for run_dir in sorted(D4_RESULTS_DIR.iterdir()):
        results_file = run_dir / "results.json"
        if not results_file.exists():
            continue
        with open(results_file) as f:
            return json.load(f)
    return None


# ============================================================
# Calibration Metric Computation
# ============================================================
def compute_ece(confidences, correctness, n_bins=10):
    """Expected Calibration Error."""
    bins = [[] for _ in range(n_bins)]
    for conf, corr in zip(confidences, correctness):
        idx = min(int(conf * n_bins), n_bins - 1)
        bins[idx].append((conf, corr))

    ece = 0.0
    n = len(confidences)
    bin_details = []
    for i, b in enumerate(bins):
        if len(b) == 0:
            bin_details.append({
                "bin_lower": i / n_bins,
                "bin_upper": (i + 1) / n_bins,
                "avg_confidence": 0, "avg_accuracy": 0, "count": 0, "gap": 0
            })
            continue
        avg_conf = np.mean([x[0] for x in b])
        avg_acc = np.mean([x[1] for x in b])
        gap = abs(avg_acc - avg_conf)
        ece += (len(b) / n) * gap
        bin_details.append({
            "bin_lower": i / n_bins,
            "bin_upper": (i + 1) / n_bins,
            "avg_confidence": round(avg_conf, 4),
            "avg_accuracy": round(avg_acc, 4),
            "count": len(b),
            "gap": round(gap, 4)
        })
    return round(ece, 6), bin_details


def compute_brier(confidences, correctness):
    """Brier Score = MSE(confidence, correctness)."""
    return round(np.mean([(c - int(r))**2 for c, r in zip(confidences, correctness)]), 6)


def compute_auroc(confidences, correctness):
    """Area Under ROC Curve for confidence as correctness predictor."""
    pairs = list(zip(confidences, correctness))
    pos = [c for c, r in pairs if r]
    neg = [c for c, r in pairs if not r]
    if not pos or not neg:
        return None
    concordant = sum(1 for p in pos for n in neg if p > n)
    tied = sum(1 for p in pos for n in neg if p == n)
    total = len(pos) * len(neg)
    return round((concordant + 0.5 * tied) / total, 6)


def compute_coverage_accuracy(confidences, correctness, thresholds=None):
    """Coverage-accuracy tradeoff curve."""
    if thresholds is None:
        thresholds = [i * 0.05 for i in range(21)]
    curve = []
    n = len(confidences)
    for t in thresholds:
        covered = [(c, r) for c, r in zip(confidences, correctness) if c >= t]
        coverage = len(covered) / n if n > 0 else 0
        accuracy = np.mean([r for _, r in covered]) if covered else 0
        curve.append({
            "threshold": round(t, 2),
            "coverage": round(coverage, 4),
            "accuracy": round(accuracy, 4),
            "n_covered": len(covered)
        })
    return curve


def compute_all_metrics(confidences, correctness, n_bins=10):
    """Compute comprehensive calibration metrics."""
    ece, bins = compute_ece(confidences, correctness, n_bins)
    mce = max(b["gap"] for b in bins) if bins else 0
    brier = compute_brier(confidences, correctness)
    auroc = compute_auroc(confidences, correctness)
    avg_conf = round(np.mean(confidences), 4)
    accuracy = round(np.mean(correctness), 4)
    overconf_gap = round(avg_conf - accuracy, 4)
    cov_acc = compute_coverage_accuracy(confidences, correctness)

    return {
        "n": len(confidences),
        "accuracy": accuracy,
        "avg_confidence": avg_conf,
        "ece": ece,
        "mce": round(mce, 4),
        "brier_score": brier,
        "auroc": auroc,
        "overconfidence_gap": overconf_gap,
        "bins": bins,
        "coverage_accuracy_curve": cov_acc,
    }


# ============================================================
# Statistical Tests
# ============================================================
def binomial_test(k, n, p0=0.20):
    """One-sided binomial test: H0: p <= p0, H1: p > p0.
    Using normal approximation for large n."""
    p_hat = k / n
    se = math.sqrt(p0 * (1 - p0) / n)
    z = (p_hat - p0) / se
    # One-sided p-value (upper tail)
    from math import erfc
    p_value = 0.5 * erfc(z / math.sqrt(2))
    return {"p_hat": round(p_hat, 4), "z": round(z, 4), "p_value": round(p_value, 6),
            "significant_005": p_value < 0.05, "significant_001": p_value < 0.01}


def one_sample_t_test(values, mu0=0):
    """One-sample t-test: H0: mean = mu0."""
    n = len(values)
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    se = std / math.sqrt(n)
    t_stat = (mean - mu0) / se if se > 0 else float('inf')
    # Two-sided p-value approximation
    df = n - 1
    # Use normal approximation for large df
    from math import erfc
    p_value = erfc(abs(t_stat) / math.sqrt(2))
    return {"mean": round(mean, 4), "std": round(std, 4), "t_stat": round(t_stat, 4),
            "p_value": round(p_value, 6), "n": n,
            "significant_005": p_value < 0.05, "significant_001": p_value < 0.01}


def chi_squared_test_topics(topic_data):
    """Chi-squared test for independence between topic and overconfident error.
    topic_data: dict of {topic: {"overconf_errors": int, "total_errors": int, "total": int}}
    """
    topics = [t for t in topic_data if topic_data[t]["total"] >= 5]
    if len(topics) < 2:
        return {"chi2": 0, "p_value": 1.0, "df": 0, "significant": False}

    # 2xK contingency: (overconf error vs non-overconf-error) x topics
    observed = []
    for t in topics:
        oe = topic_data[t]["overconf_errors"]
        total_errors = topic_data[t]["total_errors"]
        non_oe = total_errors - oe
        observed.append([oe, non_oe])

    observed = np.array(observed, dtype=float)
    row_totals = observed.sum(axis=1)
    col_totals = observed.sum(axis=0)
    grand_total = observed.sum()

    if grand_total == 0:
        return {"chi2": 0, "p_value": 1.0, "df": 0, "significant": False}

    expected = np.outer(row_totals, col_totals) / grand_total
    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        chi2_cells = np.where(expected > 0, (observed - expected)**2 / expected, 0)
    chi2 = chi2_cells.sum()
    df = (len(topics) - 1) * 1  # (rows-1) * (cols-1), cols=2

    # Chi-squared p-value approximation using Wilson-Hilferty
    if df > 0:
        z = ((chi2 / df)**(1/3) - (1 - 2/(9*df))) / math.sqrt(2/(9*df))
        from math import erfc
        p_value = 0.5 * erfc(z / math.sqrt(2))
    else:
        p_value = 1.0

    return {"chi2": round(chi2, 4), "p_value": round(p_value, 6), "df": df,
            "topics": topics, "significant_005": p_value < 0.05}


# ============================================================
# Analysis Functions
# ============================================================
def analyze_by_model_method(results):
    """Group results by model|method and compute metrics."""
    groups = defaultdict(lambda: {"confidences": [], "correctness": []})
    for r in results:
        key = f"{r['model']}|{r['method']}"
        groups[key]["confidences"].append(r["confidence"])
        groups[key]["correctness"].append(r["correct"])

    metrics = {}
    for key, data in groups.items():
        metrics[key] = compute_all_metrics(
            data["confidences"], [int(c) for c in data["correctness"]]
        )
    return metrics


def analyze_overconfident_errors(results, threshold=OVERCONF_THRESHOLD):
    """Identify and analyze overconfident errors."""
    errors = [r for r in results if not r["correct"]]
    overconf_errors = [r for r in errors if r["confidence"] >= threshold]

    # Per-method analysis
    by_method = defaultdict(lambda: {"errors": 0, "overconf": 0, "total": 0})
    for r in results:
        key = f"{r['model']}|{r['method']}"
        by_method[key]["total"] += 1
        if not r["correct"]:
            by_method[key]["errors"] += 1
            if r["confidence"] >= threshold:
                by_method[key]["overconf"] += 1

    return {
        "total_results": len(results),
        "total_errors": len(errors),
        "overconf_errors": len(overconf_errors),
        "overconf_error_rate": round(len(overconf_errors) / len(results), 4) if results else 0,
        "overconf_among_errors": round(len(overconf_errors) / len(errors), 4) if errors else 0,
        "avg_overconf_confidence": round(
            np.mean([r["confidence"] for r in overconf_errors]), 4
        ) if overconf_errors else 0,
        "by_method": dict(by_method),
    }


def analyze_by_topic(results):
    """Classify questions by topic and compute per-topic metrics."""
    topic_results = defaultdict(lambda: {"confidences": [], "correctness": [], "questions": []})

    for r in results:
        query = r.get("raw_response", "") or r.get("question", "")
        # Use the question text embedded in metadata if available
        # Fall back to raw_response (which contains the question context)
        topic = classify_topic(query)
        topic_results[topic]["confidences"].append(r["confidence"])
        topic_results[topic]["correctness"].append(int(r["correct"]))
        topic_results[topic]["questions"].append(r["question_id"])

    topic_metrics = {}
    for topic, data in topic_results.items():
        if len(data["confidences"]) < 3:
            continue
        metrics = compute_all_metrics(data["confidences"], data["correctness"])
        # Add overconfident error analysis
        errors = [(c, cr) for c, cr in zip(data["confidences"], data["correctness"]) if not cr]
        overconf = [c for c, _ in errors if c >= OVERCONF_THRESHOLD]
        metrics["n_errors"] = len(errors)
        metrics["n_overconf_errors"] = len(overconf)
        metrics["overconf_error_rate"] = round(len(overconf) / len(data["confidences"]), 4) if data["confidences"] else 0
        topic_metrics[topic] = metrics

    return topic_metrics


def test_hypotheses(results, metrics_by_mm, topic_metrics):
    """Run formal statistical tests for all hypotheses."""
    tests = {}

    # H1: Systematic overconfidence (gap > 0)
    gaps = []
    for r in results:
        gaps.append(r["confidence"] - int(r["correct"]))
    tests["H1_overconfidence"] = one_sample_t_test(gaps, mu0=0)
    tests["H1_overconfidence"]["description"] = "One-sample t-test: mean(confidence - correctness) > 0"

    # H3: High-confidence error rate > 20%
    errors = [r for r in results if not r["correct"]]
    overconf_errors = [r for r in errors if r["confidence"] >= OVERCONF_THRESHOLD]
    # Among all results
    tests["H3_overconf_rate"] = binomial_test(len(overconf_errors), len(results), p0=0.20)
    tests["H3_overconf_rate"]["description"] = f"Binomial test: P(overconf error) > 0.20, observed {len(overconf_errors)}/{len(results)}"

    # H3 alternative: among errors only
    tests["H3_among_errors"] = binomial_test(len(overconf_errors), len(errors), p0=0.50)
    tests["H3_among_errors"]["description"] = f"Among errors: P(overconf | error) > 0.50, observed {len(overconf_errors)}/{len(errors)}"

    # H4: Topic-dependent miscalibration
    topic_data = {}
    for topic, m in topic_metrics.items():
        topic_data[topic] = {
            "overconf_errors": m["n_overconf_errors"],
            "total_errors": m["n_errors"],
            "total": m["n"]
        }
    tests["H4_topic_independence"] = chi_squared_test_topics(topic_data)
    tests["H4_topic_independence"]["description"] = "Chi-squared test: overconf error rate independent of topic"

    return tests


# ============================================================
# Figure Generation
# ============================================================
def generate_figures(metrics_by_mm, results, topic_metrics):
    """Generate all publication-quality figures."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyBboxPatch
        plt.rcParams.update({
            "font.family": "serif",
            "font.size": 11,
            "axes.labelsize": 12,
            "axes.titlesize": 13,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "figure.dpi": 300,
        })
    except ImportError:
        print("WARNING: matplotlib not installed. Skipping figure generation.")
        print("Install with: pip install matplotlib")
        return False

    # --- Figure 1: Reliability Diagrams (multi-panel) ---
    fig, axes = plt.subplots(1, len(metrics_by_mm), figsize=(5 * len(metrics_by_mm), 4.5), squeeze=False)
    for idx, (key, m) in enumerate(sorted(metrics_by_mm.items())):
        ax = axes[0][idx]
        bins = m["bins"]
        bin_centers = [(b["bin_lower"] + b["bin_upper"]) / 2 for b in bins if b["count"] > 0]
        accuracies = [b["avg_accuracy"] for b in bins if b["count"] > 0]
        counts = [b["count"] for b in bins if b["count"] > 0]

        # Perfect calibration line
        ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfect calibration")
        # Bar chart of accuracy per bin
        bin_width = 0.08
        ax.bar(bin_centers, accuracies, width=bin_width, alpha=0.7, color="#4C72B0",
               edgecolor="white", label=f"Accuracy (ECE={m['ece']:.3f})")

        # Overconfidence shading
        for bc, acc in zip(bin_centers, accuracies):
            if bc > acc:
                ax.fill_between([bc - bin_width/2, bc + bin_width/2], acc, bc,
                               alpha=0.15, color="red")

        model_name, method = key.split("|")
        ax.set_title(f"{model_name}\n({method})", fontsize=11)
        ax.set_xlabel("Confidence")
        ax.set_ylabel("Accuracy")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.legend(loc="upper left", fontsize=8)
        ax.set_aspect("equal")

    plt.suptitle("Reliability Diagrams: LLM Calibration on CFA Questions", fontsize=13, y=1.02)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig1_reliability_diagrams.pdf", bbox_inches="tight", dpi=300)
    fig.savefig(FIGURES_DIR / "fig1_reliability_diagrams.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("  Figure 1: Reliability diagrams saved")

    # --- Figure 2: ECE Comparison Bar Chart ---
    fig, ax = plt.subplots(figsize=(7, 4))
    keys = sorted(metrics_by_mm.keys())
    ece_vals = [metrics_by_mm[k]["ece"] for k in keys]
    colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]
    labels = [k.replace("|", "\n") for k in keys]

    bars = ax.bar(range(len(keys)), ece_vals, color=colors[:len(keys)], edgecolor="white", width=0.6)
    for bar, val in zip(bars, ece_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f"{val:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Expected Calibration Error (ECE)")
    ax.set_title("Calibration Quality Comparison Across Models and Methods")
    ax.axhline(y=0.15, color="green", linestyle=":", alpha=0.7, label="Proposed Tier 1 threshold (0.15)")
    ax.axhline(y=0.25, color="orange", linestyle=":", alpha=0.7, label="Proposed Tier 2 threshold (0.25)")
    ax.legend(fontsize=8)
    ax.set_ylim(0, max(ece_vals) * 1.3)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig2_ece_comparison.pdf", bbox_inches="tight", dpi=300)
    fig.savefig(FIGURES_DIR / "fig2_ece_comparison.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("  Figure 2: ECE comparison saved")

    # --- Figure 3: Coverage-Accuracy Tradeoff ---
    fig, ax = plt.subplots(figsize=(7, 5))
    linestyles = ["-", "--", "-.", ":"]
    for idx, (key, m) in enumerate(sorted(metrics_by_mm.items())):
        curve = m["coverage_accuracy_curve"]
        coverages = [p["coverage"] for p in curve]
        accuracies = [p["accuracy"] for p in curve]
        ax.plot(coverages, accuracies,
                linestyle=linestyles[idx % len(linestyles)],
                marker="o", markersize=3,
                label=key.replace("|", " / "), linewidth=1.5)

    ax.axhline(y=0.70, color="red", linestyle=":", alpha=0.6, label="CFA passing threshold (70%)")
    ax.set_xlabel("Coverage (fraction of questions answered)")
    ax.set_ylabel("Accuracy (among answered questions)")
    ax.set_title("Coverage-Accuracy Tradeoff: Selective Prediction")
    ax.legend(fontsize=8, loc="lower left")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0.3, 1.0)
    ax.invert_xaxis()
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig3_coverage_accuracy.pdf", bbox_inches="tight", dpi=300)
    fig.savefig(FIGURES_DIR / "fig3_coverage_accuracy.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("  Figure 3: Coverage-accuracy tradeoff saved")

    # --- Figure 4: Overconfidence Gap Visualization ---
    fig, ax = plt.subplots(figsize=(7, 4))
    keys = sorted(metrics_by_mm.keys())
    accs = [metrics_by_mm[k]["accuracy"] for k in keys]
    confs = [metrics_by_mm[k]["avg_confidence"] for k in keys]
    gaps = [metrics_by_mm[k]["overconfidence_gap"] for k in keys]
    labels = [k.replace("|", "\n") for k in keys]

    x = range(len(keys))
    width = 0.35
    bars1 = ax.bar([i - width/2 for i in x], accs, width, label="Actual Accuracy", color="#55A868", alpha=0.8)
    bars2 = ax.bar([i + width/2 for i in x], confs, width, label="Average Confidence", color="#C44E52", alpha=0.8)

    for i, gap in enumerate(gaps):
        ax.annotate(f"Gap: {gap:+.1%}",
                    xy=(i, max(accs[i], confs[i]) + 0.02),
                    ha="center", fontsize=9, fontweight="bold", color="darkred")

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Proportion")
    ax.set_title("Overconfidence Gap: Expressed Confidence vs. Actual Accuracy")
    ax.legend()
    ax.set_ylim(0, 1.1)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig4_overconfidence_gap.pdf", bbox_inches="tight", dpi=300)
    fig.savefig(FIGURES_DIR / "fig4_overconfidence_gap.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("  Figure 4: Overconfidence gap saved")

    # --- Figure 5: Topic-level Heatmap ---
    if topic_metrics:
        topics = sorted(topic_metrics.keys(), key=lambda t: topic_metrics[t].get("overconf_error_rate", 0), reverse=True)
        # Filter to topics with >= 5 samples
        topics = [t for t in topics if topic_metrics[t]["n"] >= 5]

        if topics:
            fig, axes = plt.subplots(1, 3, figsize=(14, max(4, len(topics) * 0.5)))

            # ECE by topic
            ax = axes[0]
            ece_vals = [topic_metrics[t]["ece"] for t in topics]
            colors_ece = ["#C44E52" if v > 0.3 else "#DD8452" if v > 0.2 else "#55A868" for v in ece_vals]
            ax.barh(range(len(topics)), ece_vals, color=colors_ece, edgecolor="white")
            ax.set_yticks(range(len(topics)))
            ax.set_yticklabels(topics, fontsize=9)
            ax.set_xlabel("ECE")
            ax.set_title("ECE by Topic")
            ax.invert_yaxis()

            # Overconfident error rate by topic
            ax = axes[1]
            oe_rates = [topic_metrics[t]["overconf_error_rate"] for t in topics]
            colors_oe = ["#C44E52" if v > 0.3 else "#DD8452" if v > 0.2 else "#55A868" for v in oe_rates]
            ax.barh(range(len(topics)), oe_rates, color=colors_oe, edgecolor="white")
            ax.set_yticks(range(len(topics)))
            ax.set_yticklabels(["" for _ in topics])
            ax.set_xlabel("Overconfident Error Rate")
            ax.set_title("Overconf. Error Rate by Topic")
            ax.invert_yaxis()

            # Sample size by topic
            ax = axes[2]
            ns = [topic_metrics[t]["n"] for t in topics]
            ax.barh(range(len(topics)), ns, color="#4C72B0", edgecolor="white", alpha=0.7)
            ax.set_yticks(range(len(topics)))
            ax.set_yticklabels(["" for _ in topics])
            ax.set_xlabel("N (questions)")
            ax.set_title("Sample Size")
            ax.invert_yaxis()

            plt.suptitle("Topic-Level Calibration Analysis", fontsize=13)
            plt.tight_layout()
            fig.savefig(FIGURES_DIR / "fig5_topic_analysis.pdf", bbox_inches="tight", dpi=300)
            fig.savefig(FIGURES_DIR / "fig5_topic_analysis.png", bbox_inches="tight", dpi=300)
            plt.close()
            print("  Figure 5: Topic-level analysis saved")

    # --- Figure 6: Confidence Distribution Histogram ---
    fig, axes = plt.subplots(1, len(metrics_by_mm), figsize=(5 * len(metrics_by_mm), 4), squeeze=False)
    for idx, (key, m) in enumerate(sorted(metrics_by_mm.items())):
        ax = axes[0][idx]
        # Get confidence values for this model|method
        mm_results = [r for r in results if f"{r['model']}|{r['method']}" == key]
        correct_confs = [r["confidence"] for r in mm_results if r["correct"]]
        incorrect_confs = [r["confidence"] for r in mm_results if not r["correct"]]

        bins_edges = np.arange(0, 1.05, 0.1)
        ax.hist(correct_confs, bins=bins_edges, alpha=0.6, color="#55A868", label="Correct", edgecolor="white")
        ax.hist(incorrect_confs, bins=bins_edges, alpha=0.6, color="#C44E52", label="Incorrect", edgecolor="white")
        ax.set_xlabel("Confidence")
        ax.set_ylabel("Count")
        model_name, method = key.split("|")
        ax.set_title(f"{model_name} ({method})")
        ax.legend(fontsize=8)

    plt.suptitle("Confidence Score Distribution by Correctness", fontsize=13, y=1.02)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig6_confidence_distribution.pdf", bbox_inches="tight", dpi=300)
    fig.savefig(FIGURES_DIR / "fig6_confidence_distribution.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("  Figure 6: Confidence distribution saved")

    return True


# ============================================================
# Table Generation (LaTeX)
# ============================================================
def generate_tables(metrics_by_mm, overconf_analysis, topic_metrics, hypothesis_tests):
    """Generate LaTeX tables for the paper."""

    # Table 1: Overall Calibration Metrics
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Calibration Metrics by Model and Confidence Estimation Method}",
        r"\label{tab:calibration}",
        r"\begin{tabular}{llccccccc}",
        r"\toprule",
        r"\textbf{Model} & \textbf{Method} & \textbf{N} & \textbf{Acc.} & \textbf{Avg Conf.} & \textbf{ECE} & \textbf{Brier} & \textbf{AUROC} & \textbf{OC Gap} \\",
        r"\midrule",
    ]
    for key in sorted(metrics_by_mm.keys()):
        m = metrics_by_mm[key]
        model, method = key.split("|")
        auroc_str = f"{m['auroc']:.3f}" if m['auroc'] is not None else "---"
        lines.append(
            f"{model} & {method} & {m['n']} & {m['accuracy']:.3f} & {m['avg_confidence']:.3f} "
            f"& {m['ece']:.3f} & {m['brier_score']:.3f} & {auroc_str} & {m['overconfidence_gap']:+.3f} \\\\"
        )
    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\begin{tablenotes}",
        r"\small",
        r"\item ECE = Expected Calibration Error; Brier = Brier Score; AUROC = Area Under ROC Curve;",
        r"\item OC Gap = Overconfidence Gap (Avg Confidence $-$ Accuracy). Positive values indicate overconfidence.",
        r"\end{tablenotes}",
        r"\end{table}",
    ])
    with open(TABLES_DIR / "table1_calibration.tex", "w") as f:
        f.write("\n".join(lines))
    print("  Table 1: Calibration metrics saved")

    # Table 2: Overconfident Error Analysis
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Overconfident Error Analysis (Confidence $\geq$ 80\%)}",
        r"\label{tab:overconf}",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"\textbf{Model | Method} & \textbf{Total} & \textbf{Errors} & \textbf{OC Errors} & \textbf{OC Rate} \\",
        r"\midrule",
    ]
    for key in sorted(overconf_analysis["by_method"].keys()):
        d = overconf_analysis["by_method"][key]
        rate = d["overconf"] / d["total"] if d["total"] > 0 else 0
        lines.append(f"{key} & {d['total']} & {d['errors']} & {d['overconf']} & {rate:.1%} \\\\")
    lines.extend([
        r"\midrule",
        f"\\textbf{{Overall}} & {overconf_analysis['total_results']} & {overconf_analysis['total_errors']} "
        f"& {overconf_analysis['overconf_errors']} & {overconf_analysis['overconf_error_rate']:.1%} \\\\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ])
    with open(TABLES_DIR / "table2_overconfident.tex", "w") as f:
        f.write("\n".join(lines))
    print("  Table 2: Overconfident error analysis saved")

    # Table 3: Topic-Level Calibration
    if topic_metrics:
        topics = sorted(topic_metrics.keys(), key=lambda t: topic_metrics[t].get("overconf_error_rate", 0), reverse=True)
        topics = [t for t in topics if topic_metrics[t]["n"] >= 5]
        lines = [
            r"\begin{table}[htbp]",
            r"\centering",
            r"\caption{Calibration Metrics by CFA Topic}",
            r"\label{tab:topic}",
            r"\begin{tabular}{lccccc}",
            r"\toprule",
            r"\textbf{CFA Topic} & \textbf{N} & \textbf{Acc.} & \textbf{ECE} & \textbf{OC Errors} & \textbf{OC Rate} \\",
            r"\midrule",
        ]
        for topic in topics:
            m = topic_metrics[topic]
            lines.append(
                f"{topic} & {m['n']} & {m['accuracy']:.3f} & {m['ece']:.3f} "
                f"& {m['n_overconf_errors']} & {m['overconf_error_rate']:.1%} \\\\"
            )
        lines.extend([
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
        ])
        with open(TABLES_DIR / "table3_topic.tex", "w") as f:
            f.write("\n".join(lines))
        print("  Table 3: Topic-level calibration saved")

    # Table 4: Hypothesis Test Results
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Statistical Tests for Research Hypotheses}",
        r"\label{tab:hypotheses}",
        r"\begin{tabular}{lllc}",
        r"\toprule",
        r"\textbf{Hypothesis} & \textbf{Test} & \textbf{Statistic} & \textbf{$p$-value} \\",
        r"\midrule",
    ]
    for h_key, h_data in hypothesis_tests.items():
        desc = h_data.get("description", h_key)
        if "t_stat" in h_data:
            stat_str = f"$t = {h_data['t_stat']:.2f}$"
        elif "z" in h_data:
            stat_str = f"$z = {h_data['z']:.2f}$"
        elif "chi2" in h_data:
            stat_str = f"$\\chi^2 = {h_data['chi2']:.2f}$"
        else:
            stat_str = "---"

        p_val = h_data.get("p_value", 1.0)
        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else ""
        p_str = f"{p_val:.4f}{sig}" if p_val >= 0.0001 else f"$<0.0001${sig}"
        lines.append(f"{h_key} & {desc[:50]}... & {stat_str} & {p_str} \\\\")

    lines.extend([
        r"\bottomrule",
        r"\multicolumn{4}{l}{\small $^{***}p<0.001$; $^{**}p<0.01$; $^{*}p<0.05$} \\",
        r"\end{tabular}",
        r"\end{table}",
    ])
    with open(TABLES_DIR / "table4_hypotheses.tex", "w") as f:
        f.write("\n".join(lines))
    print("  Table 4: Hypothesis tests saved")


# ============================================================
# Main
# ============================================================
def main():
    print("=" * 70)
    print("D1+D4 Calibration & Risk Analysis")
    print("=" * 70)

    # Load data
    print("\n[1/6] Loading experiment results...")
    results, existing_metrics = load_all_d1_results()
    d4_data = load_d4_results()

    if not results:
        print("ERROR: No D1 results found. Run the D1 experiment first.")
        sys.exit(1)

    # Compute metrics by model|method
    print("\n[2/6] Computing calibration metrics...")
    metrics_by_mm = analyze_by_model_method(results)
    for key, m in sorted(metrics_by_mm.items()):
        print(f"  {key}: N={m['n']}, Acc={m['accuracy']:.3f}, ECE={m['ece']:.3f}, "
              f"AUROC={m['auroc']}, OC Gap={m['overconfidence_gap']:+.3f}")

    # Overconfident error analysis
    print("\n[3/6] Analyzing overconfident errors...")
    overconf = analyze_overconfident_errors(results)
    print(f"  Total: {overconf['total_results']} results, {overconf['total_errors']} errors, "
          f"{overconf['overconf_errors']} overconfident errors ({overconf['overconf_error_rate']:.1%})")
    print(f"  Among errors: {overconf['overconf_among_errors']:.1%} are overconfident")
    print(f"  Avg confidence of overconfident errors: {overconf['avg_overconf_confidence']:.1%}")

    # Topic analysis
    print("\n[4/6] Topic-level analysis...")
    topic_metrics = analyze_by_topic(results)
    for topic in sorted(topic_metrics.keys(), key=lambda t: topic_metrics[t].get("overconf_error_rate", 0), reverse=True):
        m = topic_metrics[topic]
        print(f"  {topic}: N={m['n']}, Acc={m['accuracy']:.3f}, ECE={m['ece']:.3f}, "
              f"OC Errors={m['n_overconf_errors']}/{m['n']} ({m['overconf_error_rate']:.1%})")

    # Hypothesis testing
    print("\n[5/6] Running hypothesis tests...")
    tests = test_hypotheses(results, metrics_by_mm, topic_metrics)
    for h_key, h_data in tests.items():
        sig = "SIGNIFICANT" if h_data.get("significant_005") or h_data.get("significant") else "not significant"
        p_val = h_data.get("p_value", 1.0)
        print(f"  {h_key}: p={p_val:.6f} ({sig})")

    # Generate figures
    print("\n[6/6] Generating figures and tables...")
    fig_success = generate_figures(metrics_by_mm, results, topic_metrics)
    generate_tables(metrics_by_mm, overconf, topic_metrics, tests)

    # Save comprehensive analysis results
    analysis_output = {
        "metadata": {
            "total_results": len(results),
            "models_methods": list(metrics_by_mm.keys()),
            "n_topics": len(topic_metrics),
        },
        "metrics_by_model_method": {k: {kk: vv for kk, vv in v.items() if kk != "bins" and kk != "coverage_accuracy_curve"}
                                     for k, v in metrics_by_mm.items()},
        "overconfident_error_analysis": overconf,
        "topic_metrics": {k: {kk: vv for kk, vv in v.items() if kk != "bins" and kk != "coverage_accuracy_curve"}
                          for k, v in topic_metrics.items()},
        "hypothesis_tests": tests,
    }

    with open(OUTPUT_DIR / "analysis_results.json", "w") as f:
        json.dump(analysis_output, f, indent=2, default=str)
    print(f"\nAnalysis results saved to {OUTPUT_DIR / 'analysis_results.json'}")

    # Summary
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"\nKey Findings:")
    print(f"  1. Overconfidence gap: {list(metrics_by_mm.values())[0]['overconfidence_gap']:+.1%} (H1)")
    print(f"  2. Overconfident error rate: {overconf['overconf_error_rate']:.1%} of all results (H3)")
    print(f"  3. Among errors, {overconf['overconf_among_errors']:.1%} are high-confidence (H3)")
    best_ece = min(metrics_by_mm.items(), key=lambda x: x[1]["ece"])
    worst_ece = max(metrics_by_mm.items(), key=lambda x: x[1]["ece"])
    print(f"  4. Best ECE: {best_ece[0]} = {best_ece[1]['ece']:.3f}")
    print(f"  5. Worst ECE: {worst_ece[0]} = {worst_ece[1]['ece']:.3f}")

    if fig_success:
        print(f"\nFigures saved to: {FIGURES_DIR}")
    print(f"Tables saved to: {TABLES_DIR}")

    return analysis_output


if __name__ == "__main__":
    main()
