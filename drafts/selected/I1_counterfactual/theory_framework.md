# I1+I3 Theory Framework: Stress Testing Financial LLMs
# Counterfactual Perturbation and Noise Sensitivity Analysis

## Paper Title
**Stress Testing Financial LLMs: Do They Reason or Memorize?**

**Target Journal**: Finance Research Letters (FRL), SSCI Q1

---

## 1. Research Hypotheses

### H1: Memorization Hypothesis (I1)
**When numerical parameters of CFA questions are perturbed while preserving the underlying financial logic, LLM accuracy declines significantly, indicating reliance on memorization rather than genuine reasoning.**

- **Rationale**: CFA exam prep materials (SchweserNotes, Kaplan) are extensively represented in LLM pretraining corpora. The limited question pool size (~2,000 unique questions across major prep providers) and stereotypical numerical patterns (e.g., coupon rate = 5%, face value = 1000) create ideal conditions for rote memorization. If models have memorized question-answer pairs, changing "5% coupon" to "7.3% coupon" should cause disproportionate accuracy drops even though the reasoning procedure is identical.
- **Operationalization**: Memorization Gap = Accuracy_original − Accuracy_perturbed. Robust Accuracy = fraction of questions where model is correct on both original AND all perturbation variants.
- **Expected effect size**: 10–25% accuracy drop for Level 1 (numerical) perturbations.

### H2: Perturbation Severity Gradient (I1)
**Accuracy degradation is monotonically increasing with perturbation severity: Level 1 (numerical only) < Level 2 (conditional inversion) < Level 3 (scenario reconstruction).**

- **Rationale**: Level 1 preserves the exact same formula and reasoning path; only the numerical inputs change. Level 2 requires selecting a different formula or adjusting the reasoning direction. Level 3 requires transferring the concept to an entirely new context. Each level demands progressively more genuine understanding.
- **Operationalization**: Per-level accuracy and per-level memorization gap.

### H3: Noise Sensitivity Hypothesis (I3)
**Injecting irrelevant or misleading information into CFA questions significantly reduces LLM accuracy, revealing poor signal-to-noise discrimination.**

- **Rationale**: Real-world financial analysis requires filtering vast amounts of irrelevant data. CFA exams deliberately include "red herring" information. Current benchmarks use clean, minimal question text, which does not test this critical skill. If LLMs are sensitive to noise, their benchmark scores overstate their practical utility.
- **Operationalization**: Noise Sensitivity Index (NSI) = (Acc_clean − Acc_noisy) / Acc_clean. Ranges from 0 (noise-immune) to 1 (noise-destroyed).
- **Expected effect size**: NSI = 0.05–0.20 for N1 (irrelevant data), higher for N2 (misleading statements) and N4 (contradictory information).

### H4: Noise Type Heterogeneity (I3)
**Different noise types produce significantly different degradation patterns: misleading financial distractors (N2) and contradictory information (N4) are more harmful than irrelevant data (N1) or formatting noise (N3).**

- **Rationale**: Irrelevant data (N1) can be ignored if the model understands what's relevant. Misleading data (N2) actively competes with correct information for the model's attention. Contradictory data (N4) creates a logical inconsistency the model must resolve. Format noise (N3) is superficial and should be least harmful for sophisticated models.
- **Operationalization**: Compare NSI across four noise types using repeated-measures ANOVA or Friedman test.

### H5: Model Size Mitigates Both Effects
**Larger models exhibit smaller memorization gaps and lower noise sensitivity, but the relationship is not linear—there exists a threshold below which robustness degrades rapidly.**

- **Rationale**: Larger models have greater capacity for genuine pattern learning (not just memorization) and more sophisticated attention mechanisms for filtering irrelevant tokens. However, larger models also have greater memorization capacity, creating a tension.
- **Operationalization**: Plot Memorization Gap and NSI against model parameter count. Test for non-linear threshold effects.

---

## 2. Theoretical Foundation

### 2.1 Data Contamination & Benchmark Validity
The threat of data contamination in financial LLM benchmarks is uniquely severe. Unlike general-purpose reasoning benchmarks (e.g., GSM8K with >7,000 questions), CFA exam question pools are:
- **Small**: ~1,000–2,000 unique prep questions per level
- **Structurally stereotyped**: Fixed templates (bond pricing, portfolio return, option Greeks)
- **Widely distributed**: SchweserNotes, Kaplan, AnalystPrep materials are extensively scraped

This creates what we term the **"narrow corridor problem"** — the space of plausible CFA questions is so constrained that near-memorization can masquerade as reasoning. Our counterfactual perturbation approach directly addresses this by testing whether performance generalizes beyond the memorized corridor.

### 2.2 Robustness in Financial Decision-Making
The financial industry's adoption of AI systems requires **stress testing** — a concept well-established in risk management (Basel III framework, CCAR/DFAST stress tests). We propose an analogous framework for AI cognitive stress testing:

| Banking Stress Test | Our AI Stress Test |
|---|---|
| Adverse macro scenario | Counterfactual perturbation (I1) |
| Market shock | Noise injection (I3) |
| Capital adequacy | Robust Accuracy |
| Stressed VaR | Performance under worst-case noise |

This analogy positions our work within the familiar framework of financial risk management.

### 2.3 Connection to Sensitivity Analysis
In quantitative finance, sensitivity analysis (delta, gamma, vega) measures how outputs change with respect to input perturbations. Our framework applies the same principle to AI systems:
- **Delta (first-order)**: How does accuracy change with numerical perturbation? (I1 Level 1)
- **Gamma (second-order)**: How does the rate of accuracy change accelerate with perturbation severity? (I1 Level 1→2→3)
- **Vega (noise sensitivity)**: How does accuracy change with information noise? (I3 NSI)

---

## 3. Economic Significance

### 3.1 Financial Risk Management Implications

**Quantifying the Memorization Premium in AI-Assisted Analysis**

If an AI system achieves 80% accuracy on standard CFA questions but only 60% on perturbation variants, the "true" accuracy for novel financial analysis is 60%, not 80%. The 20-percentage-point gap represents a **memorization premium** — inflated performance that evaporates when the AI encounters genuine novel problems.

For a portfolio manager using AI-assisted analysis:
- **Standard benchmark accuracy** (80%) suggests the AI correctly processes 4 out of 5 financial calculations
- **Robust accuracy** (60%) reveals it actually processes 3 out of 5 correctly
- The **1 in 5 "phantom correct"** responses arise from memorization, not reasoning — these will fail unpredictably on real-world problems that differ from training examples

In dollar terms: if AI-assisted analysis informs $100M in investment decisions, and 20% of the AI's "correct" outputs are memorization artifacts, approximately $20M of capital allocation is based on unreliable analysis.

### 3.2 CFA Exam Integrity and AI-Proofing

The CFA Institute invests heavily in exam security and question integrity. Our findings directly inform:

1. **Question recycling risk**: If AI can memorize CFA question patterns, human candidates using AI assistance can exploit the same narrow question space. Our Robust Accuracy metric provides a measure of how "AI-permeable" the current exam format is.

2. **Question design recommendations**: Topics where I1 memorization gap is highest should receive priority for question pool diversification. Topics where I3 noise sensitivity is lowest indicate areas where AI demonstrates genuine competence.

3. **Adaptive testing implications**: Questions that show high memorization gap but low noise sensitivity are ideal candidates for adaptive testing — they discriminate between memorizers and genuine reasoners.

### 3.3 AI Regulatory Implications

**Minimum Robustness Standards for Financial AI**

The EU AI Act classifies AI systems used in financial services as "high-risk." Our stress testing framework provides concrete, quantifiable criteria for robustness assessment:

1. **Memorization Gap Threshold**: A financial AI system should demonstrate Memorization Gap < 10% — meaning its performance is not inflated by rote memorization. Systems exceeding this threshold require additional human oversight.

2. **Noise Sensitivity Threshold**: NSI < 0.15 across all noise types — the system should not lose more than 15% of its accuracy when presented with real-world noise levels.

3. **Robust Accuracy Reporting**: Regulators should require financial AI vendors to report Robust Accuracy alongside standard accuracy, similar to how banks report stressed capital ratios alongside unstressed ones.

These thresholds are analogous to the capital adequacy ratios in banking regulation — they provide a concrete, measurable standard for AI system quality.

### 3.4 Implications for AI-Assisted Financial Advisory

**The Illusion of Competence Problem**

When an AI advisory system trained on financial materials gives a confident answer that happens to match a memorized pattern, it creates a dangerous illusion: the system appears competent, but its competence is brittle. Consider:

- **Scenario A**: AI correctly calculates bond duration for a standard textbook example (5% coupon, 10-year, semi-annual). The client is impressed.
- **Scenario B**: The same AI is asked about a non-standard structure (variable coupon, callable, different compounding). It applies the memorized formula pattern incorrectly because the numbers don't match its training data.

The transition from Scenario A to B is invisible to the end user but critical for investment outcomes. Our I1 perturbation framework directly quantifies this transition risk.

---

## 4. Discussion Points

### 4.1 Memorization vs. Reasoning: A Spectrum, Not a Binary

Our results likely reveal that LLMs don't purely memorize or purely reason — they exist on a spectrum. The Memorization Gap metric allows us to place each model on this spectrum for each financial topic. This has implications for:
- **Model selection**: For tasks requiring genuine reasoning (novel analysis, stress testing), prefer models with lower Memorization Gap even if their standard accuracy is lower
- **Confidence interpretation**: High-confidence answers on standard questions should be discounted by the model's memorization rate

### 4.2 The Financial Domain's Unique Vulnerability

We argue that the financial domain is uniquely vulnerable to memorization artifacts for three structural reasons:
1. **Narrow question typology**: Unlike open-ended reasoning, financial calculations follow a finite set of templates
2. **Public exam materials**: CFA prep materials are widely available online and in training corpora
3. **High-stakes consequences**: Unlike academic benchmarks, financial decisions based on AI output have real monetary consequences

### 4.3 Stress Testing as Due Diligence

CFA Standard V(A) — Diligence and Reasonable Basis — requires that investment professionals have a reasonable basis for their recommendations. We argue that deploying an AI system without stress testing its reasoning (i.e., relying on standard accuracy alone) violates the spirit of this standard. Our framework provides a practical tool for due diligence in AI-assisted finance.

### 4.4 Limitations and Future Directions

1. **Perturbation quality**: Automated perturbation generation may introduce errors; we mitigate with human verification on a subsample
2. **Single-shot evaluation**: We test memorization in a single-pass setting; multi-turn reasoning (agent-style) may yield different patterns
3. **Benchmark specificity**: Results are specific to CFA-domain questions; generalization to other financial tasks (credit analysis, portfolio optimization) requires further study
4. **Causal attribution**: A high memorization gap suggests but does not prove memorization — it could also reflect sensitivity to numerical range or problem framing

---

## 5. Methodology Summary

### 5.1 Counterfactual Perturbation (I1)

Three levels of perturbation severity:
- **Level 1** (Numerical): Change 1 numerical parameter (rate, term, face value), keeping formula identical
- **Level 2** (Conditional): Change the problem condition (compounding frequency, option type, spread direction)
- **Level 3** (Scenario): Rewrite the entire scenario while preserving the core concept

Each original question generates 3 Level 1 + 2 Level 2 = 5 variants (Level 3 optional for subset).

### 5.2 Noise Injection (I3)

Four noise types at controlled intensity:
- **N1**: Irrelevant data points (1–5 extra numbers)
- **N2**: Misleading financial statements (plausible but irrelevant assertions)
- **N3**: Format noise (inconsistent number formatting, extra whitespace)
- **N4**: Contradictory information (conflicting data in different parts of the question)

### 5.3 Combined Analysis

The integration of I1 and I3 creates a 2×2 framework:

|  | Clean Question | Noisy Question |
|---|---|---|
| **Original** | Standard Accuracy | Noise-Degraded Accuracy |
| **Perturbed** | Robust Accuracy | Worst-Case Accuracy |

The "Worst-Case Accuracy" (perturbed + noisy) represents the most realistic estimate of AI performance in genuine novel financial analysis.

---

## 6. Key References

- Apple (2024). GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models. — Methodological inspiration for counterfactual perturbation.
- Shi et al. (2023). Detecting Pretraining Data from Large Language Models. — Data contamination detection.
- Jia & Liang (2017). Adversarial Examples for Evaluating Reading Comprehension Systems. — Noise injection methodology.
- Black (1986). Noise. Journal of Finance. — Theoretical foundation for noise in financial markets.
- Basel Committee on Banking Supervision (2018). Stress Testing Principles. — Analogy framework for AI stress testing.
- CFA Institute (2024). Code of Ethics and Standards of Professional Conduct. — Standard V(A) due diligence.
- EU AI Act (2024). — High-risk AI system requirements for financial services.
