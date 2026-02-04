"""Configuration for I2 behavioral biases experiment."""

# ---------------------------------------------------------------------------
# Bias types
# ---------------------------------------------------------------------------

BIAS_TYPES = {
    "loss_aversion": {
        "name": "Loss Aversion",
        "description": "Tendency to prefer avoiding losses over acquiring equivalent gains",
        "cfa_topic": "Behavioral Finance",
        "bias_direction": "Choose lower-EV option to avoid stated losses",
    },
    "anchoring": {
        "name": "Anchoring",
        "description": "Over-reliance on the first piece of information encountered",
        "cfa_topic": "Behavioral Finance",
        "bias_direction": "Answer biased toward the anchor value",
    },
    "framing": {
        "name": "Framing Effect",
        "description": "Different responses to the same problem based on how it's presented",
        "cfa_topic": "Behavioral Finance",
        "bias_direction": "Different answer depending on gain vs loss framing",
    },
    "overconfidence": {
        "name": "Overconfidence Bias",
        "description": "Excessive confidence in own predictions/knowledge",
        "cfa_topic": "Behavioral Finance",
        "bias_direction": "Overly narrow confidence intervals or extreme predictions",
    },
    "recency": {
        "name": "Recency Bias",
        "description": "Overweighting recent events in decision-making",
        "cfa_topic": "Behavioral Finance",
        "bias_direction": "Decision biased toward recent trend continuation",
    },
    "disposition_effect": {
        "name": "Disposition Effect",
        "description": "Selling winners too early and holding losers too long",
        "cfa_topic": "Portfolio Management",
        "bias_direction": "Recommend selling winning positions",
    },
}

# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

BIAS_SYSTEM = (
    "You are a CFA-certified financial advisor. Answer the following "
    "investment question based on sound financial principles. "
    "Show your reasoning clearly."
)

NEUTRAL_SYSTEM = (
    "You are a CFA-certified financial advisor. Evaluate the following "
    "scenario using only quantitative analysis. Focus strictly on "
    "expected values and risk-adjusted returns."
)

# ---------------------------------------------------------------------------
# Bias scoring prompt
# ---------------------------------------------------------------------------

SCORE_SYSTEM = """You are a behavioral finance expert. Given a model's response to an investment scenario, determine whether the response exhibits a specific behavioral bias.

The scenario has:
- A "rational baseline" answer (based on EV/quantitative analysis)
- A "biased" answer (the answer a biased human would give)

Score the response:
- 0.0 = Fully rational (matches rational baseline)
- 0.5 = Mixed / unclear
- 1.0 = Fully biased (matches biased prediction)

Respond in JSON:
{
    "bias_score": <0.0-1.0>,
    "chosen_option": "A or B or description",
    "reasoning": "brief explanation of why this score"
}"""

SCORE_USER = """Bias type: {bias_type}

Scenario (bias-inducing version):
{scenario}

Model's response:
{response}

Rational baseline: {rational_answer}
Biased prediction: {biased_answer}

Score the bias level (0=rational, 1=biased)."""
