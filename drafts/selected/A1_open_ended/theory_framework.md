# A1+A5 Theory Framework: Open-Ended Evaluation and Option Bias
# Beyond Multiple Choice: Unmasking the True Financial Reasoning Ability of LLMs

## Paper Title
**Beyond Multiple Choice: How Answer Options Inflate LLM Financial Reasoning Scores**

**Target Journal**: Finance Research Letters (FRL), SSCI Q1

---

## 1. Research Hypotheses

### H1: Option Inflation Hypothesis (A5 Core)
**LLM accuracy on CFA questions is significantly higher in MCQ format than in open-ended format, demonstrating that answer options systematically inflate perceived financial reasoning ability.**

- **Rationale**: MCQ options leak three types of information: (a) magnitude clues — option values constrain the answer's order of magnitude; (b) sign clues — option signs constrain the answer's direction; (c) elimination clues — implausible options can be rejected without solving the problem. This "crutch effect" inflates accuracy beyond the model's genuine reasoning capacity.
- **Operationalization**: Option Bias = Accuracy_MCQ − Accuracy_OpenEnded per model/topic. McNemar's test for statistical significance on paired (question, format) observations.
- **Expected effect size**: +15–30% option bias for calculation questions, +5–15% for conceptual questions.

### H2: Model Size Modulates Bias
**Smaller models exhibit larger option bias than larger models, because smaller models have less genuine reasoning capacity and rely more heavily on option-derived heuristics.**

- **Rationale**: Larger models can internalize more complete financial formulas and reasoning procedures, making them less dependent on option-provided shortcuts. Smaller models, lacking this capacity, disproportionately exploit the answer space restriction.
- **Operationalization**: Regress Option Bias on log(model_size) across 6+ models.

### H3: Topic-Dependent Bias
**Option bias varies significantly across CFA topics: calculation-intensive topics (Quantitative Methods, Fixed Income, Derivatives) show larger bias than memory-intensive topics (Ethics, Economics).**

- **Rationale**: Calculation questions benefit most from magnitude/sign clues in options. Ethics questions require judgment that is less affected by answer choices. This creates a topic-dependent measurement artifact in current benchmarks.
- **Operationalization**: Per-topic Option Bias with Kruskal-Wallis test for significant between-topic variation.

### H4: Three-Tier Evaluation Reveals Hidden Competence (A1 Core)
**A substantial fraction (15–25%) of LLM responses classified as "incorrect" in binary evaluation are actually directionally correct — using valid reasoning approaches but with different assumptions or minor calculation errors.**

- **Rationale**: Financial calculations inherently involve ambiguity: annual vs. continuous compounding, different day-count conventions, rounding policies. Binary scoring conflates genuine errors with legitimate analytical disagreements.
- **Operationalization**: Three-tier classification — Level A (exact/acceptable match, ±2%), Level B (directionally correct, right approach but wrong final number), Level C (fundamentally incorrect). Report Strict Accuracy (Level A) and Lenient Accuracy (A+B).

### H5: Error Attribution Reveals Systematic Weaknesses
**LLM errors cluster into identifiable categories — formula selection errors dominate for complex topics, while calculation errors dominate for simpler topics.**

- **Rationale**: For well-understood financial concepts, LLMs typically select the correct formula but may err in arithmetic. For complex topics (structured products, multi-step derivatives), the bottleneck shifts to formula/concept selection.
- **Operationalization**: Structured error attribution using LLM-as-judge to classify each error into: formula_error, calculation_error, conceptual_error, assumption_mismatch, unit_error, extraction_error.

---

## 2. Theoretical Foundation

### 2.1 Answer-Space Restriction Bias (Testing Theory)
In classical test theory, item response is modeled as a function of the examinee's latent ability and the item's parameters (difficulty, discrimination). MCQ formats introduce a third factor: the answer option set constrains the response space, providing information beyond the examinee's ability. This is formalized as:

P(correct | MCQ) = P(knows) + P(¬knows) × P(guess | options)

For a 4-option MCQ, naive guessing yields P(guess) = 0.25. But LLMs can do better than naive guessing — they can use option-derived heuristics (magnitude matching, elimination) to achieve:

P(strategic_guess | options) >> 0.25

Our open-ended format removes this term entirely, yielding a purer measure of P(knows).

### 2.2 Financial Ambiguity and Evaluation Fairness
Unlike mathematics (where 2+2=4 unambiguously), financial calculations involve convention choices:
- Annual vs. continuous compounding
- ACT/360 vs. ACT/365 day counts
- Different rounding policies (round half up, round to even)
- Tax treatment variations

Binary scoring (correct/incorrect) penalizes responses that use different but equally valid conventions. Our three-tier framework explicitly accommodates this ambiguity, providing fairer evaluation of genuine financial competence.

---

## 3. Economic Significance

### 3.1 Benchmark Validity and Capital Allocation Decisions

If financial AI benchmarks systematically overstate model capability by 15–30% due to MCQ format bias, institutions relying on these benchmarks for technology adoption decisions face material risk:

- **Buy-side firms** evaluating AI tools for analyst augmentation may deploy systems whose "80% accuracy" is actually "55% accuracy" on novel calculations
- **Sell-side research** departments using AI-generated analyses may not realize the quality gap between standardized (MCQ-like) and open-ended analyses
- **Risk management**: A model that appears competent on structured risk metrics may fail on novel scenario analysis

The dollar impact: if 30% of perceived AI competence is format-inflated, technology budgets allocated based on inflated benchmarks represent misallocated capital.

### 3.2 CFA Exam Design and AI-Era Assessment

Our findings have direct implications for CFA Institute exam design:

1. **Format vulnerability**: Topics where option bias is highest represent the CFA exam's greatest vulnerability to AI-assisted cheating — a candidate using AI would gain the most advantage on these topics
2. **Item design**: Our option bias metric can serve as a quality indicator for individual exam items — high-bias items are poor discriminators of genuine competence
3. **Format evolution**: The results motivate exploration of partial-credit scoring and open-ended formats for future CFA exam versions

### 3.3 Regulatory and Compliance Implications

**AI Transparency Requirements**

Under the EU AI Act and emerging SEC guidance on AI in financial services:
- AI vendors should report both MCQ-format and open-ended-format accuracy, clearly distinguishing format-dependent from format-independent competence
- Compliance functions should require "option-free" evaluation of AI tools used for financial advisory
- Internal model validation (analogous to MRM/SR 11-7) should include format sensitivity testing

### 3.4 The Hidden Competence Problem

The three-tier evaluation reveals a more nuanced picture: some "errors" are actually reasonable alternative analyses. This has practical implications:

- **Portfolio review**: An AI that computes a slightly different Sharpe ratio due to different annualization assumptions is not "wrong" — it's using a different but valid convention
- **Compliance checking**: Overly strict binary evaluation may lead to unnecessary human review of acceptable AI outputs
- **Training data curation**: Level B responses should not be treated as negative examples in RLHF training

---

## 4. Discussion Points

### 4.1 The Paradox of Options
Our A5 POC data shows a surprising result: gpt-4o-mini achieves 60% accuracy WITH options but 100% WITHOUT options (on a small N=5 sample). If this pattern persists at scale, it suggests that options can sometimes HURT performance — possibly through distractor anchoring effects. This "negative option bias" phenomenon deserves dedicated analysis.

### 4.2 Implications for All LLM Benchmarks
Our findings generalize beyond CFA: any MCQ-format benchmark (MMLU, ARC, HellaSwag) may suffer from the same format inflation. We provide a methodological template — paired MCQ/open-ended evaluation — that can be applied to any domain.

### 4.3 Three-Tier Evaluation as a New Standard
We propose that the three-tier framework become a standard reporting practice for financial LLM evaluation, providing: Strict Accuracy (Level A), Lenient Accuracy (A+B), and Error Rate (Level C only). This tripartite metric gives a more complete picture than single-number accuracy.

### 4.4 Limitations
1. **Gold Answer Set construction**: Defining acceptable tolerance ranges requires domain expertise; our tolerance thresholds (±2% for exact, ±10% for directional) are reasonable but arguable
2. **Semantic matching reliability**: LLM-as-judge for open-ended evaluation introduces its own error; we report inter-rater agreement
3. **Small initial sample**: POC uses N=5; full study requires N≥200 for adequate power

---

## 5. Key References

- Zheng et al. (2024). Measuring Massive Multitask Language Understanding (MMLU). — MCQ format standard.
- Robinson et al. (2023). Leveraging Large Language Models for Multiple Choice Question Answering. — Option exploitation strategies.
- CFA Institute (2024). Candidate Body of Knowledge. — Topic structure and exam format.
- Lord (1980). Applications of Item Response Theory to Practical Testing Problems. — Answer-space restriction theory.
- Gao et al. (2024). Are LLMs Good at Multiple Choice Questions? — MCQ-specific evaluation pitfalls.
