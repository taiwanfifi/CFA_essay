"""Configuration for D4 overconfident risk experiment."""

# ---------------------------------------------------------------------------
# Confidence thresholds
# ---------------------------------------------------------------------------

DEFAULT_CONFIDENCE_THRESHOLD = 0.8  # Minimum confidence to flag as "overconfident error"
HIGH_CONFIDENCE_THRESHOLD = 0.9     # Very high confidence (most dangerous)

# ---------------------------------------------------------------------------
# Risk severity categories
# ---------------------------------------------------------------------------

RISK_SEVERITY = {
    "critical": {
        "description": "Could cause significant financial loss or regulatory violation",
        "examples": [
            "Wrong portfolio allocation leading to excess risk",
            "Incorrect derivative pricing",
            "Misapplied ethics standard leading to compliance breach",
        ],
    },
    "high": {
        "description": "Could mislead investment decisions",
        "examples": [
            "Wrong bond valuation",
            "Incorrect cost of capital calculation",
            "Misidentified risk factor",
        ],
    },
    "medium": {
        "description": "Conceptual error that could propagate in analysis",
        "examples": [
            "Confused financial ratios",
            "Wrong economic indicator interpretation",
        ],
    },
    "low": {
        "description": "Minor error unlikely to cause real harm",
        "examples": [
            "Rounding error",
            "Minor definitional confusion",
        ],
    },
}

# ---------------------------------------------------------------------------
# CFA Ethics Standard mapping (for ethics-related errors)
# ---------------------------------------------------------------------------

CFA_ETHICS_STANDARDS = {
    "I": "Professionalism",
    "II": "Integrity of Capital Markets",
    "III": "Duties to Clients",
    "IV": "Duties to Employers",
    "V": "Investment Analysis",
    "VI": "Conflicts of Interest",
    "VII": "Responsibilities as CFA Member",
}

# ---------------------------------------------------------------------------
# Risk classification prompt
# ---------------------------------------------------------------------------

RISK_CLASSIFY_SYSTEM = """You are a CFA exam expert and financial risk analyst. You are reviewing cases where an AI model answered a CFA question INCORRECTLY but with HIGH CONFIDENCE.

For each case, classify:
1. **risk_severity**: critical / high / medium / low
2. **risk_category**: What type of financial risk does this error pose?
3. **real_world_impact**: How could this error harm an investor or firm in practice?
4. **error_mechanism**: Why did the model get this wrong?

Respond in JSON format:
{
    "risk_severity": "critical|high|medium|low",
    "risk_category": "string",
    "real_world_impact": "string",
    "error_mechanism": "string"
}"""

RISK_CLASSIFY_USER = """Question: {question}

Correct Answer: {correct_answer}
Model's Answer: {model_answer}
Model's Confidence: {confidence:.0%}
Model's Reasoning: {reasoning}

Classify the risk of this overconfident error."""
