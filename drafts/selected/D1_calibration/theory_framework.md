# Theory Framework: When AI Is Confidently Wrong

## Paper Identity
- **Title**: When AI Is Confidently Wrong: Calibration and Risk Analysis of Large Language Models in Financial Decision-Making
- **Target**: Finance Research Letters (SSCI Q1)
- **Core Argument**: The most dangerous failure mode of financial AI is not inaccuracy, but *miscalibrated confidence*—specifically, high-confidence errors that erode the decision-maker's ability to distinguish reliable from unreliable AI outputs.

---

## Formal Hypotheses

### H1: Systematic Overconfidence
**LLMs exhibit systematic overconfidence on CFA examination questions, with average expressed confidence significantly exceeding actual accuracy.**

- Operationalization: Overconfidence Gap = E[confidence] - E[accuracy] > 0
- Preliminary evidence: Gap = 30.7% (self-consistency) and 31.8% (verbalized) for gpt-4o-mini
- Statistical test: One-sample t-test, H₀: gap = 0

### H2: Confidence Method Heterogeneity
**Different confidence estimation methods yield significantly different calibration quality, with self-consistency outperforming verbalized confidence.**

- Operationalization: Compare ECE, AUROC across methods (verbalized, self-consistency, ensemble)
- Preliminary evidence: Self-consistency ECE = 0.307 vs Verbalized ECE = 0.318; AUROC 0.630 vs 0.600
- Statistical test: Paired Wilcoxon signed-rank test on per-question confidence-correctness pairs

### H3: High-Confidence Error Prevalence
**A substantial proportion (>20%) of all model errors occur at high confidence levels (≥80%), creating a "hidden risk" zone where users cannot rely on expressed confidence to filter errors.**

- Operationalization: Overconfident Error Rate = P(confidence ≥ 0.8 | incorrect)
- Preliminary evidence: 74/250 = 29.6% of results are high-confidence errors
- Statistical test: Binomial test, H₀: rate ≤ 0.20

### H4: Topic-Dependent Miscalibration
**Calibration quality varies significantly across CFA knowledge domains, with computation-intensive topics (Derivatives, Fixed Income, Quantitative Methods) exhibiting higher overconfident error rates than conceptual topics (Ethics, Economics).**

- Operationalization: Per-topic ECE and overconfident error rate
- Statistical test: Chi-squared test for independence between topic and overconfident error occurrence

### H5: Coverage-Accuracy Tradeoff Insufficiency
**Selective prediction via confidence thresholding cannot achieve CFA passing accuracy (≥70%) without sacrificing more than 50% coverage, rendering confidence-based filtering impractical for production deployment.**

- Operationalization: Coverage at accuracy ≥ 0.70 from coverage-accuracy curve
- Preliminary evidence: At threshold 0.95, coverage = 41.1% with accuracy = 67.6% (still below 70%)
- Implication: Even aggressive filtering cannot make the model "safe enough" for autonomous deployment

---

## Theoretical Grounding

### 1. Decision Theory: Expected Utility Under Miscalibration

In the standard financial decision framework, an agent chooses action $a$ to maximize:

$$E[U(a)] = \sum_s P(s) \cdot U(a, s)$$

When an LLM provides both a recommendation and a confidence level, the human decision-maker updates their subjective probability:

$$P_{updated}(s) = f(P_{prior}(s), P_{LLM}(s), \text{trust}(LLM))$$

**Key insight**: If the LLM's expressed confidence $P_{LLM}$ is systematically inflated, the human's $P_{updated}$ will be biased upward, leading to:
1. **Under-diversification**: Overconfident AI on specific positions → concentrated risk
2. **Premature action**: High-confidence signals trigger execution before adequate due diligence
3. **Reduced second-guessing**: "The AI is 95% confident" suppresses human critical judgment

### 2. Risk Management: VaR Analogy

Drawing from Value-at-Risk methodology, we define an analogous metric for AI confidence risk:

**Confidence-at-Risk (CaR)**: The minimum confidence level $c^*$ such that P(incorrect | confidence ≥ c*) ≤ α

From our data:
- At c* = 0.80: P(incorrect | conf ≥ 0.80) = 74/(74+N_correct_high_conf) ≈ 42.4%
- At c* = 0.95: P(incorrect | conf ≥ 0.95) ≈ 32.4%
- Even at the highest confidence levels, the error rate remains dangerously high

**Interpretation**: A risk manager using AI outputs cannot achieve a 5% error rate at *any* confidence threshold—the model's confidence signal is fundamentally unreliable for risk-budgeting purposes.

### 3. Information Economics: Noisy Signal Quality

In rational expectations models, information value is determined by signal precision $\tau = 1/\sigma^2$. A well-calibrated model provides:

$$\text{Signal value} \propto \tau_{calibrated} = \frac{1}{ECE^2}$$

For our models:
- gpt-4o-mini (verbalized): $\tau \propto 1/0.318^2 = 9.88$
- qwen3:32b (verbalized): $\tau \propto 1/0.241^2 = 17.22$

A perfectly calibrated model ($ECE = 0$) would have infinite signal value. The 24-32% ECE values suggest the confidence signal adds only modest information value—far less than what users implicitly assume when acting on "85% confident" recommendations.

---

## Economic Significance Framework

### A. Portfolio Risk Impact

**Scenario**: An AI-assisted portfolio manager relies on LLM-generated analysis for bond duration assessment.

If the LLM reports "duration = 4.2 years, confidence = 95%" but the true duration is 6.8 years:

$$\Delta V \approx -D_{error} \cdot \Delta y \cdot V = -(6.8 - 4.2) \times 0.01 \times \$10M = -\$260,000$$

A single overconfident duration error on a $10M portfolio position with a 100bp rate shock creates a $260,000 unexpected loss—representing a 2.6% portfolio-level loss that was "invisible" to the risk model.

### B. Fiduciary Duty and CFA Ethics

We map overconfident AI failures to three CFA Institute Standards:

| CFA Standard | Violation Mechanism | AI Analogy |
|---|---|---|
| **I(C) Misrepresentation** | Presenting analysis with unwarranted certainty | AI states "95% confident" on incorrect analysis |
| **V(A) Diligence & Reasonable Basis** | Failing to verify AI outputs due to high expressed confidence | Analyst skips verification because "the model is very confident" |
| **III(C) Suitability** | Recommending products based on flawed AI analysis | AI confidently recommends unsuitable asset allocation |

**Legal precedent analogy**: Just as a human analyst who routinely presents uncertain conclusions as facts would face professional sanctions, an AI system that systematically overstates confidence should trigger compliance review.

### C. Regulatory Implications

| Regulatory Framework | Relevant Provision | Our Finding |
|---|---|---|
| **EU AI Act (2024)** | High-risk AI in financial services requires transparency and accuracy assessment | ECE > 0.30 suggests current LLMs fail accuracy transparency requirements |
| **SEC AI Guidance** | AI-driven investment recommendations must have "reasonable basis" | 29.6% high-confidence error rate undermines "reasonable basis" standard |
| **MAS (Singapore) FEAT Principles** | AI systems must be "fair, ethical, accountable, transparent" | Miscalibrated confidence violates transparency principle |
| **CFA Institute AI Standards** | "AI should augment, not replace, professional judgment" | Overconfident AI *undermines* professional judgment by suppressing skepticism |

**Policy Recommendation**: Financial regulators should establish **minimum calibration standards** for AI systems used in advisory roles:
- **Tier 1 (Advisory)**: ECE < 0.15, overconfident error rate < 15%
- **Tier 2 (Screening)**: ECE < 0.25, overconfident error rate < 25%
- **Tier 3 (Research aid)**: ECE < 0.35 with mandatory confidence disclaimers

---

## Discussion Framework

### Why This Matters More Than Accuracy

The literature on AI in finance has focused overwhelmingly on *accuracy*: "Can GPT-4 pass the CFA exam?" (answer: sometimes). But accuracy alone is a poor guide to deployment safety. Consider two models:

| Model | Accuracy | ECE | Overconfident Error Rate |
|---|---|---|---|
| Model A | 70% | 0.05 | 5% |
| Model B | 75% | 0.35 | 40% |

**Model B is more accurate but more dangerous.** Its high accuracy masks the fact that when it's wrong, it's *confidently* wrong—giving users no reliable signal to identify errors. Model A, despite lower accuracy, provides calibrated uncertainty that enables effective human oversight.

This reframes the AI-in-finance debate from "How smart is the AI?" to "Does the AI know what it doesn't know?"

### Selective Prediction as a (Partial) Solution

Our coverage-accuracy analysis shows:
- gpt-4o-mini (self-consistency): At 41% coverage, accuracy reaches only 67.6%
- qwen3:32b (verbalized): At 69% coverage, accuracy reaches 81.3%

Implication: For qwen3:32b, a selective prediction system that abstains on low-confidence questions can achieve CFA passing performance—but at the cost of leaving 31% of questions unanswered. This creates a **human-AI handoff problem**: who handles the 31%? If it's always the human, the AI saves ~70% of manual work. If it's nobody, 31% of client queries go unanswered.

### Cross-Model Calibration Gap

The substantial performance gap between qwen3:32b (ECE = 0.241) and gpt-4o-mini (ECE = 0.318) suggests that:
1. **Calibration is model-dependent**, not a universal LLM property
2. **Larger models may not always be better calibrated** (model size ≠ calibration quality)
3. **Model selection for financial applications should prioritize calibration**, not just accuracy

---

## Key Figures and Tables Planned

1. **Figure 1: Reliability Diagram** — Confidence bins vs actual accuracy for all model×method combinations. Diagonal = perfect calibration.
2. **Figure 2: Coverage-Accuracy Tradeoff** — How accuracy changes as we raise the confidence threshold (selective prediction).
3. **Table 1: Overall Calibration Metrics** — ECE, MCE, Brier Score, AUROC, Overconfidence Gap per model×method.
4. **Table 2: Overconfident Error Analysis** — Rate by CFA topic, error type distribution, risk severity.
5. **Figure 3: Overconfidence Gap Visualization** — Bar chart comparing overconfidence gap across models.
6. **Table 3: Regulatory Mapping** — Connecting findings to EU AI Act, SEC guidance, CFA Ethics standards.

---

## Contribution Statement

1. **Empirical**: First systematic calibration study of LLMs on professional financial certification (CFA) questions, using 250+ observations across multiple models and confidence estimation methods.
2. **Methodological**: Introduce Confidence-at-Risk (CaR) metric adapting VaR to AI confidence assessment in finance.
3. **Policy**: Bridge the gap between NLP calibration research and financial regulation by mapping technical findings to CFA Ethics Standards and the EU AI Act.
4. **Practical**: Provide evidence-based recommendations for minimum calibration standards before deploying AI in financial advisory roles.
