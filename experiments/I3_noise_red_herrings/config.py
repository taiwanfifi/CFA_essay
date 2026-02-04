"""Configuration for I3 noise and red herring experiment."""

# ---------------------------------------------------------------------------
# Noise types
# ---------------------------------------------------------------------------

NOISE_TYPES = {
    "N1": "irrelevant_data",       # Inject unrelated numerical facts
    "N2": "plausible_distractor",  # Add financially plausible but irrelevant info
    "N3": "verbose_context",       # Pad with wordy but vacuous context
    "N4": "contradictory_hint",    # Insert a misleading (but subtly wrong) hint
}

# ---------------------------------------------------------------------------
# N1: Irrelevant data snippets (inserted into question body)
# ---------------------------------------------------------------------------

N1_SNIPPETS = [
    "The issuing company has 12,500 employees and was founded in 1987.",
    "Its current ESG rating is BBB+ from MSCI.",
    "The company's headquarters are located in Zurich, Switzerland.",
    "Last quarter's marketing expenditure was $14.2 million.",
    "The CEO holds an MBA from Wharton and has 22 years of industry experience.",
    "The firm's Glassdoor rating is 3.8 out of 5.0.",
    "Annual R&D spending represents 6.3% of total revenue.",
    "The company operates in 34 countries across 5 continents.",
    "Its stock ticker changed from XYZ to XYZN in 2019.",
    "The board of directors comprises 11 members, 4 of whom are independent.",
    "The company's carbon footprint was 245,000 metric tons CO2e last year.",
    "Employee turnover rate stands at 12.7% annually.",
]

# ---------------------------------------------------------------------------
# N2: Plausible financial distractors
# ---------------------------------------------------------------------------

N2_SNIPPETS = [
    "Note that the risk-free rate has recently shifted by 15 basis points due to monetary policy changes.",
    "The company's beta was recently revised from 1.2 to 1.15 by Bloomberg.",
    "Market consensus expects a 25 bps rate cut at the next FOMC meeting.",
    "The firm's credit spread widened by 30 bps in the last quarter.",
    "Analysts project a P/E ratio compression from 18x to 15x over the next year.",
    "The VIX index is currently at 22.4, suggesting elevated market uncertainty.",
    "The yield curve inverted briefly last month before returning to normal.",
    "Foreign exchange reserves increased by $2.1 billion in Q3.",
]

# ---------------------------------------------------------------------------
# N3: Verbose padding templates
# ---------------------------------------------------------------------------

N3_TEMPLATES = [
    (
        "It is worth noting that in the broader context of financial markets, "
        "which have experienced considerable volatility in recent periods due to "
        "a variety of macroeconomic factors including but not limited to inflationary "
        "pressures and geopolitical tensions, the following question should be "
        "considered carefully."
    ),
    (
        "Before proceeding with the analysis, one should acknowledge that "
        "financial theory provides multiple frameworks for approaching such "
        "problems, and while the specific methodology may vary depending on "
        "the assumptions made, the fundamental principles remain consistent "
        "across different analytical approaches."
    ),
]

# ---------------------------------------------------------------------------
# N4: Contradictory hint templates
# ---------------------------------------------------------------------------

N4_TEMPLATES = [
    "Hint: Many students incorrectly choose {wrong_answer} here, but think carefully.",
    "Note: A common approach would suggest {wrong_answer}, but consider all factors.",
    "Remember: The intuitive answer might be {wrong_answer}, which is a frequent trap.",
]

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

MCQ_SYSTEM = (
    "You are a CFA exam expert. Read the question carefully, show your reasoning, "
    "then state your final answer as: ANSWER: X (where X is A, B, or C)."
)
