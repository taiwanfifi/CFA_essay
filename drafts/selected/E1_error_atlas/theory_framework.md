# E1 Theory Framework: CFA Error Pattern Atlas
# A Systematic Taxonomy of Financial LLM Failures

## Paper Title
**The CFA Error Atlas: Mapping Failure Modes of Large Language Models in Financial Reasoning**

**Target Journal**: Finance Research Letters (FRL) or Journal of Financial Data Science

---

## 1. Research Hypotheses

### H1: Error Non-Uniformity
**LLM errors on CFA questions are non-uniformly distributed across error types and financial topics, exhibiting systematic patterns that reflect structural limitations rather than random noise.**

- **Rationale**: If errors were random (coin-flip noise), the error distribution across topics and types would be roughly proportional to topic frequency. Systematic deviations indicate specific cognitive bottlenecks.
- **Operationalization**: Chi-squared test of independence between Error Type × CFA Topic. Reject H0 (uniform distribution) at p < 0.05.

### H2: Calculation Dominance in Quantitative Topics
**Quantitative topics (Fixed Income, Derivatives, Quant Methods) are dominated by Calculation Errors and Formula Misapplication, while qualitative topics (Ethics, Economics) are dominated by Distractor Confusion and Knowledge Gaps.**

- **Rationale**: Quantitative questions have well-defined solution procedures; LLMs can identify the correct approach but fail in execution. Qualitative questions require nuanced judgment; LLMs fail by being misled by plausible-sounding wrong options.
- **Operationalization**: Per-topic error type distribution; test dominance via proportion tests.

### H3: Cross-Model Error Convergence
**Different LLMs fail on the same questions with the same error types more often than chance, suggesting shared training data biases rather than model-specific weaknesses.**

- **Rationale**: All major LLMs are trained on similar internet corpora. Shared knowledge gaps and misconceptions should manifest as correlated error patterns.
- **Operationalization**: Cosine similarity between error distribution vectors of model pairs. Compare to null distribution from permutation test.

### H4: Cognitive Stage Bottleneck
**The majority of LLM errors originate in the early cognitive stages (Concept Identification, Formula Recall) rather than late stages (Calculation, Verification), contradicting the naive assumption that LLMs struggle primarily with arithmetic.**

- **Rationale**: Modern LLMs with chain-of-thought can perform multi-step arithmetic reasonably well. The primary bottleneck is selecting the correct framework and formula for the given problem — a higher-order cognitive task.
- **Operationalization**: Distribution of errors across 5 cognitive stages; test for non-uniformity.

---

## 2. Economic Significance

### 2.1 Targeted Remediation for Financial AI

The Error Atlas enables **precision remediation**: instead of generic fine-tuning, institutions can target specific failure modes:

- If Fixed Income errors are predominantly "Formula Misapplication" → create targeted training data with diverse bond calculation scenarios
- If Ethics errors are predominantly "Distractor Confusion" → improve the model's ability to resist plausible-sounding wrong options
- **ROI**: Targeted remediation is 3–5x more efficient than generic fine-tuning (fewer training examples, faster convergence)

### 2.2 Risk-Weighted Error Assessment

Not all errors are equally costly. A formula misapplication in derivatives pricing can cause catastrophic losses; a knowledge gap about ESG regulations may have minor consequences. The Atlas enables risk-weighted accuracy reporting:

Risk-Weighted Accuracy = Σ (correctness_i × risk_weight_i) / Σ risk_weight_i

where risk_weight is determined by topic (Derivatives > Ethics) and error type (Calculation Error > Knowledge Gap in terms of consequence unpredictability).

### 2.3 Human-AI Complementarity Design

The Atlas reveals where human oversight is most needed:
- **High error convergence** topics: Multiple models fail similarly → these are structural blind spots requiring mandatory human review
- **Low error convergence** topics: Models fail differently → ensemble approaches or model selection can address the weakness
- **Calculation-dominated** errors: Consider hybrid systems where LLMs handle reasoning and external tools handle computation

---

## 3. Discussion Points

### 3.1 The Atlas as a Living Resource
The Error Atlas should be continuously updated as new models emerge. We propose a community standard format (JSON schema) for error classification that enables cross-study comparison.

### 3.2 Error Patterns as Model Selection Criteria
Different deployment scenarios require different error profiles. A compliance tool should minimize Knowledge Gap errors (need comprehensive knowledge). A calculation tool should minimize Calculation Errors (need arithmetic precision). The Atlas provides the data for informed model selection.

### 3.3 Limitations
- Automated error classification (GPT-4o as judge) may itself contain systematic biases
- Human annotation of 200-question validation set provides inter-rater reliability but is not exhaustive
- Error taxonomy is domain-specific to CFA; generalization to broader finance tasks requires further study

---

## 4. Key References

- Lightman et al. (2023). Let's Verify Step by Step. — Process-level error analysis.
- Cobbe et al. (2021). Training Verifiers to Solve Math Word Problems. — Error detection methodology.
- Hendrycks et al. (2021). Measuring Mathematical Problem Solving with MATH. — Error categorization in mathematical reasoning.
