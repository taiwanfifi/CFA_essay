"""
LLM-based Error Classifier.

Uses GPT-4o to classify errors into the taxonomy defined in taxonomy.py.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

from .taxonomy import (
    CFATopic,
    ErrorType,
    CognitiveStage,
    ErrorClassification,
    TOPIC_KEYWORDS,
    ERROR_TYPE_DESCRIPTIONS,
    ERROR_TO_STAGE_MAPPING,
)


# =============================================================================
# Classification Prompts
# =============================================================================

TOPIC_CLASSIFY_SYSTEM = """You are a CFA exam topic classifier. Given a question, classify it into ONE of these topics:

- ethics: Ethical and Professional Standards, Code of Ethics, Standards of Professional Conduct
- quantitative: Statistics, probability, regression, hypothesis testing
- economics: Macroeconomics, monetary policy, fiscal policy, exchange rates
- financial_reporting: Financial statements, IFRS/GAAP, accounting
- corporate_finance: Capital budgeting, NPV, IRR, WACC, capital structure
- equity: Stock valuation, P/E, dividend discount, market efficiency
- fixed_income: Bonds, yield, duration, convexity, credit risk
- derivatives: Options, futures, forwards, swaps
- alternatives: Hedge funds, private equity, real estate, commodities
- portfolio: Asset allocation, CAPM, Sharpe ratio, diversification
- wealth_planning: Estate planning, retirement, behavioral finance

Respond with ONLY the topic name (lowercase, use underscore for multi-word topics).
"""

ERROR_CLASSIFY_SYSTEM = """You are an expert at analyzing LLM reasoning errors on CFA exam questions.

Given:
1. The question
2. The correct answer
3. The model's answer (wrong)
4. The model's reasoning

Classify the PRIMARY error type into ONE of these categories:

CONCEPTUAL ERRORS:
- concept_misunderstanding: Fundamentally misunderstands the financial concept
- concept_incomplete: Understands concept but misses important nuances

CALCULATION ERRORS:
- calc_formula_error: Uses the wrong formula
- calc_arithmetic_error: Right formula, wrong arithmetic
- calc_unit_error: Confuses units/scales (annual vs semi-annual, % vs decimal)

REASONING ERRORS:
- reasoning_chain_break: Correct steps but wrong logical connection
- reasoning_premise_error: Wrong assumptions about what's being asked
- reasoning_irrelevant: Focuses on irrelevant information

READING ERRORS:
- reading_misparse: Misreads numbers or key terms
- reading_incomplete: Doesn't use all given information

SELECTION ERRORS:
- selection_near_miss: Calculation close but picks wrong option
- selection_random: No clear reasoning, appears arbitrary

ETHICS-SPECIFIC:
- ethics_standard_confusion: Confuses which Standard applies
- ethics_nuance_miss: Gets general principle but misses specific rule

Respond in JSON format:
{
    "error_type": "the_error_type",
    "confidence": 0.8,
    "reasoning": "Brief explanation of why this classification"
}
"""


# =============================================================================
# Classifier Class
# =============================================================================

class ErrorClassifier:
    """Classifies errors using LLM."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def classify_topic(self, question: str) -> CFATopic:
        """Classify question into CFA topic."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": TOPIC_CLASSIFY_SYSTEM},
                {"role": "user", "content": question[:4000]},  # Truncate if too long
            ],
            temperature=0,
            max_tokens=50,
        )
        topic_str = response.choices[0].message.content.strip().lower()

        # Map to enum
        for topic in CFATopic:
            if topic.value == topic_str:
                return topic
        return CFATopic.UNKNOWN

    def classify_error(
        self,
        question: str,
        correct_answer: str,
        model_answer: str,
        model_reasoning: str,
    ) -> Dict[str, Any]:
        """Classify the type of error made."""
        user_prompt = f"""Question:
{question[:3000]}

Correct Answer: {correct_answer}
Model's Answer: {model_answer}

Model's Reasoning:
{model_reasoning[:2000]}

Classify the error type."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": ERROR_CLASSIFY_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            max_tokens=200,
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON response
        try:
            # Find JSON in response
            json_match = re.search(r'\{[^}]+\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result
        except json.JSONDecodeError:
            pass

        # Fallback: try to extract error type from text
        for error_type in ErrorType:
            if error_type.value in content.lower():
                return {
                    "error_type": error_type.value,
                    "confidence": 0.5,
                    "reasoning": content,
                }

        return {
            "error_type": ErrorType.UNKNOWN.value,
            "confidence": 0.0,
            "reasoning": content,
        }

    def classify_single(
        self,
        question_id: str,
        question: str,
        correct_answer: str,
        model_answer: str,
        model_reasoning: str,
        method: str = "",
    ) -> ErrorClassification:
        """Classify a single error completely."""
        topic = self.classify_topic(question)
        error_info = self.classify_error(
            question, correct_answer, model_answer, model_reasoning
        )

        # Map error_type string to enum
        error_type = ErrorType.UNKNOWN
        for et in ErrorType:
            if et.value == error_info.get("error_type"):
                error_type = et
                break

        # Derive cognitive stage from error type
        cognitive_stage = ERROR_TO_STAGE_MAPPING.get(error_type, CognitiveStage.UNKNOWN)

        return ErrorClassification(
            question_id=question_id,
            topic=topic,
            error_type=error_type,
            cognitive_stage=cognitive_stage,
            confidence=error_info.get("confidence", 0.5),
            reasoning=error_info.get("reasoning", ""),
            model_answer=model_answer,
            correct_answer=correct_answer,
            model_reasoning=model_reasoning,
            method=method,
        )

    def classify_batch(
        self,
        errors: List[Dict[str, Any]],
        verbose: bool = True,
    ) -> List[ErrorClassification]:
        """Classify a batch of errors.

        Args:
            errors: List of dicts with keys:
                - question_id, query, correct_answer, answer, reasoning, method
            verbose: Print progress

        Returns:
            List of ErrorClassification objects
        """
        results = []
        for i, err in enumerate(errors):
            if verbose:
                print(f"  Classifying {i+1}/{len(errors)}: {err['question_id']} ({err.get('method', '?')})")

            classification = self.classify_single(
                question_id=err["question_id"],
                question=err["query"],
                correct_answer=err["correct_answer"],
                model_answer=err["answer"],
                model_reasoning=err.get("reasoning", ""),
                method=err.get("method", ""),
            )
            results.append(classification)

        return results
