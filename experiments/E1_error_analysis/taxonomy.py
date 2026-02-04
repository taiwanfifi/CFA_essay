"""
Error Taxonomy for CFA Exam Questions.

Two-dimensional classification:
1. Topic (WHAT domain): Ethics, Fixed Income, Derivatives, etc.
2. Error Type (HOW it failed): Conceptual, Calculation, Reasoning, etc.

Reference: CFA Institute curriculum topic areas
"""

from enum import Enum
from typing import Dict, List, Optional


# =============================================================================
# Dimension 1: CFA Topic Areas
# =============================================================================

class CFATopic(str, Enum):
    """CFA curriculum topic areas (Level I-III combined)."""
    ETHICS = "ethics"                         # Ethical and Professional Standards
    QUANT = "quantitative"                    # Quantitative Methods
    ECONOMICS = "economics"                   # Economics
    FINANCIAL_REPORTING = "financial_reporting"  # Financial Statement Analysis
    CORPORATE_FINANCE = "corporate_finance"   # Corporate Issuers
    EQUITY = "equity"                         # Equity Investments
    FIXED_INCOME = "fixed_income"             # Fixed Income
    DERIVATIVES = "derivatives"               # Derivatives
    ALTERNATIVES = "alternatives"             # Alternative Investments
    PORTFOLIO = "portfolio"                   # Portfolio Management
    WEALTH = "wealth_planning"                # Wealth Planning (Level III)
    UNKNOWN = "unknown"


# Keywords for topic classification (used by LLM classifier)
TOPIC_KEYWORDS: Dict[CFATopic, List[str]] = {
    CFATopic.ETHICS: [
        "CFA Institute", "Standards of Professional Conduct", "Code of Ethics",
        "fiduciary", "duty of loyalty", "conflict of interest", "disclosure",
        "material nonpublic information", "MNPI", "insider trading",
        "misrepresentation", "diligence", "reasonable basis",
    ],
    CFATopic.QUANT: [
        "probability", "statistics", "regression", "hypothesis test",
        "correlation", "standard deviation", "variance", "mean",
        "time series", "Monte Carlo", "sampling",
    ],
    CFATopic.ECONOMICS: [
        "GDP", "inflation", "monetary policy", "fiscal policy",
        "interest rate", "exchange rate", "Taylor rule", "central bank",
        "aggregate demand", "aggregate supply", "business cycle",
    ],
    CFATopic.FINANCIAL_REPORTING: [
        "balance sheet", "income statement", "cash flow statement",
        "IFRS", "GAAP", "revenue recognition", "depreciation",
        "inventory", "LIFO", "FIFO", "goodwill", "impairment",
    ],
    CFATopic.CORPORATE_FINANCE: [
        "capital budgeting", "NPV", "IRR", "WACC", "cost of capital",
        "capital structure", "dividend policy", "leverage",
        "merger", "acquisition", "corporate governance",
    ],
    CFATopic.EQUITY: [
        "stock", "equity valuation", "P/E ratio", "dividend discount",
        "free cash flow", "residual income", "market efficiency",
        "industry analysis", "company analysis",
    ],
    CFATopic.FIXED_INCOME: [
        "bond", "yield", "duration", "convexity", "coupon",
        "interest rate risk", "credit risk", "spread",
        "term structure", "yield curve", "OAS", "callable",
    ],
    CFATopic.DERIVATIVES: [
        "option", "futures", "forward", "swap",
        "put", "call", "strike price", "expiration",
        "Black-Scholes", "delta", "gamma", "hedging",
    ],
    CFATopic.ALTERNATIVES: [
        "hedge fund", "private equity", "real estate",
        "commodity", "infrastructure", "venture capital",
        "alternative investment", "illiquidity premium",
    ],
    CFATopic.PORTFOLIO: [
        "portfolio", "asset allocation", "diversification",
        "efficient frontier", "CAPM", "beta", "alpha",
        "Sharpe ratio", "risk-adjusted return", "rebalancing",
    ],
    CFATopic.WEALTH: [
        "wealth planning", "estate planning", "tax planning",
        "retirement", "insurance", "behavioral finance",
        "individual investor", "institutional investor",
    ],
}


# =============================================================================
# Dimension 2: Error Types
# =============================================================================

class ErrorType(str, Enum):
    """Types of errors LLMs make on financial questions."""

    # Conceptual errors (wrong understanding)
    CONCEPT_MISUNDERSTANDING = "concept_misunderstanding"
    # Misunderstands the financial concept being tested
    # Example: Confuses duration with maturity

    CONCEPT_INCOMPLETE = "concept_incomplete"
    # Knows the concept but misses key nuances
    # Example: Knows duration but forgets modified vs Macaulay

    # Calculation errors (wrong math)
    CALC_FORMULA_ERROR = "calc_formula_error"
    # Uses wrong formula
    # Example: Uses simple interest instead of compound

    CALC_ARITHMETIC_ERROR = "calc_arithmetic_error"
    # Right formula, wrong arithmetic
    # Example: 1.05^3 calculated as 1.15 instead of 1.157625

    CALC_UNIT_ERROR = "calc_unit_error"
    # Unit/scale confusion
    # Example: Confuses annual vs semi-annual, % vs decimal

    # Reasoning errors (wrong logic)
    REASONING_CHAIN_BREAK = "reasoning_chain_break"
    # Correct steps individually but wrong connection
    # Example: Calculates PV correctly but applies wrong interpretation

    REASONING_PREMISE_ERROR = "reasoning_premise_error"
    # Wrong assumption about what the question asks
    # Example: Assumes annual compounding when question says monthly

    REASONING_IRRELEVANT = "reasoning_irrelevant"
    # Focuses on irrelevant information
    # Example: Long discussion of unrelated concepts

    # Reading comprehension errors
    READING_MISPARSE = "reading_misparse"
    # Misreads numbers or key terms from question
    # Example: Reads 5% as 50%, or misses "NOT" in question

    READING_INCOMPLETE = "reading_incomplete"
    # Fails to use all given information
    # Example: Ignores a constraint mentioned in the scenario

    # Answer selection errors
    SELECTION_NEAR_MISS = "selection_near_miss"
    # Calculation close but picks wrong option
    # Example: Calculates $922 but picks $912

    SELECTION_RANDOM = "selection_random"
    # No clear reasoning, appears random
    # Example: Picks C with no justification

    # Ethics-specific errors
    ETHICS_STANDARD_CONFUSION = "ethics_standard_confusion"
    # Confuses which Standard applies
    # Example: Cites Standard III when Standard I applies

    ETHICS_NUANCE_MISS = "ethics_nuance_miss"
    # Gets the general principle but misses the specific rule
    # Example: Knows disclosure is needed but wrong timing

    # Meta errors
    NO_ANSWER = "no_answer"
    # Failed to provide an answer
    # Example: API error, timeout, or refusal

    UNKNOWN = "unknown"
    # Cannot classify


# Descriptions for LLM classifier
ERROR_TYPE_DESCRIPTIONS: Dict[ErrorType, str] = {
    ErrorType.CONCEPT_MISUNDERSTANDING: "Fundamentally misunderstands the financial concept (e.g., confuses duration with maturity)",
    ErrorType.CONCEPT_INCOMPLETE: "Understands the concept but misses important nuances or edge cases",
    ErrorType.CALC_FORMULA_ERROR: "Uses the wrong formula for the calculation",
    ErrorType.CALC_ARITHMETIC_ERROR: "Uses correct formula but makes arithmetic mistakes",
    ErrorType.CALC_UNIT_ERROR: "Confuses units, scales, or time periods (e.g., annual vs semi-annual)",
    ErrorType.REASONING_CHAIN_BREAK: "Individual steps are correct but logical connection fails",
    ErrorType.REASONING_PREMISE_ERROR: "Makes wrong assumptions about what the question is asking",
    ErrorType.REASONING_IRRELEVANT: "Focuses on irrelevant information or concepts",
    ErrorType.READING_MISPARSE: "Misreads numbers, terms, or key words from the question",
    ErrorType.READING_INCOMPLETE: "Fails to use all information given in the question",
    ErrorType.SELECTION_NEAR_MISS: "Calculation is close but selects wrong answer option",
    ErrorType.SELECTION_RANDOM: "No clear reasoning; answer appears arbitrary",
    ErrorType.ETHICS_STANDARD_CONFUSION: "Confuses which ethical standard or rule applies",
    ErrorType.ETHICS_NUANCE_MISS: "Gets the general ethical principle but misses specific requirements",
    ErrorType.NO_ANSWER: "Failed to provide any answer",
    ErrorType.UNKNOWN: "Error type cannot be determined",
}


# =============================================================================
# Dimension 3: Cognitive Stage (from B1 five-stage reasoning pipeline)
# =============================================================================

class CognitiveStage(str, Enum):
    """Stage in the reasoning pipeline where the error occurred."""

    IDENTIFY = "identify"
    # Stage 1: Identifying what concept/topic the question is testing
    # Error example: Question asks about Duration, model discusses Maturity

    RECALL = "recall"
    # Stage 2: Recalling the relevant formula or rule
    # Error example: Uses Macaulay Duration formula when Modified Duration is needed

    EXTRACT = "extract"
    # Stage 3: Extracting numerical data from the question
    # Error example: Question says "semi-annual" but model uses annual compounding

    CALCULATE = "calculate"
    # Stage 4: Performing the actual calculation
    # Error example: 1.05^10 computed incorrectly

    VERIFY = "verify"
    # Stage 5: Verifying the answer makes sense
    # Error example: Gets negative bond price but doesn't notice it's impossible

    UNKNOWN = "unknown"


COGNITIVE_STAGE_DESCRIPTIONS: Dict[CognitiveStage, str] = {
    CognitiveStage.IDENTIFY: "Failed to correctly identify what concept/topic the question is testing",
    CognitiveStage.RECALL: "Failed to recall the correct formula, rule, or principle",
    CognitiveStage.EXTRACT: "Failed to correctly extract data or constraints from the question",
    CognitiveStage.CALCULATE: "Made errors during the actual calculation step",
    CognitiveStage.VERIFY: "Failed to verify that the answer is reasonable or consistent",
    CognitiveStage.UNKNOWN: "Cannot determine which stage the error occurred",
}


# Mapping from Error Type to likely Cognitive Stage
ERROR_TO_STAGE_MAPPING: Dict[ErrorType, CognitiveStage] = {
    # Conceptual errors → usually Identify or Recall
    ErrorType.CONCEPT_MISUNDERSTANDING: CognitiveStage.IDENTIFY,
    ErrorType.CONCEPT_INCOMPLETE: CognitiveStage.RECALL,

    # Calculation errors → Calculate stage
    ErrorType.CALC_FORMULA_ERROR: CognitiveStage.RECALL,
    ErrorType.CALC_ARITHMETIC_ERROR: CognitiveStage.CALCULATE,
    ErrorType.CALC_UNIT_ERROR: CognitiveStage.EXTRACT,

    # Reasoning errors → various stages
    ErrorType.REASONING_CHAIN_BREAK: CognitiveStage.VERIFY,
    ErrorType.REASONING_PREMISE_ERROR: CognitiveStage.IDENTIFY,
    ErrorType.REASONING_IRRELEVANT: CognitiveStage.IDENTIFY,

    # Reading errors → Extract stage
    ErrorType.READING_MISPARSE: CognitiveStage.EXTRACT,
    ErrorType.READING_INCOMPLETE: CognitiveStage.EXTRACT,

    # Selection errors → Verify stage
    ErrorType.SELECTION_NEAR_MISS: CognitiveStage.VERIFY,
    ErrorType.SELECTION_RANDOM: CognitiveStage.UNKNOWN,

    # Ethics errors → Identify or Recall
    ErrorType.ETHICS_STANDARD_CONFUSION: CognitiveStage.RECALL,
    ErrorType.ETHICS_NUANCE_MISS: CognitiveStage.RECALL,

    # Meta
    ErrorType.NO_ANSWER: CognitiveStage.UNKNOWN,
    ErrorType.UNKNOWN: CognitiveStage.UNKNOWN,
}


# =============================================================================
# Error Classification Result
# =============================================================================

from dataclasses import dataclass, field


@dataclass
class ErrorClassification:
    """Classification result for a single error."""
    question_id: str
    topic: CFATopic
    error_type: ErrorType
    cognitive_stage: CognitiveStage  # NEW: which reasoning stage failed
    confidence: float  # 0-1, how confident the classifier is
    reasoning: str     # Explanation of why this classification
    model_answer: str  # What the model answered
    correct_answer: str  # What was correct
    model_reasoning: str  # Model's reasoning (if available)
    method: str = ""  # Which method produced this error (cot, agent, etc.)
