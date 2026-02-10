# Comprehensive Peer Review Report
## 7 Papers on LLM Financial Reasoning (CFA Exam Evaluation Suite)
### Target Journal: Finance Research Letters

**Review Date:** 2026-02-10
**Reviewer:** Claude Opus 4.6 (Independent Review Agent)
**Methodology:** Cross-referenced against 46+ peer-reviewed papers; verified all experimental data against JSON results files; audited shared codebase for methodology quality.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Literature Comparison & Novelty Assessment](#2-literature-comparison--novelty-assessment)
3. [Data Integrity Audit](#3-data-integrity-audit)
4. [Methodology Critique](#4-methodology-critique)
5. [Per-Paper Review (P1–P7)](#5-per-paper-reviews)
6. [Cross-Paper Structural Issues](#6-cross-paper-structural-issues)
7. [Scoring Summary](#7-scoring-summary)
8. [New Research Directions](#8-new-research-directions)

---

## 1. Executive Summary

This suite of 7 papers represents a systematic evaluation of LLM financial reasoning using CFA exam questions derived from SchweserNotes (via FinDAP, EMNLP 2025 Oral). The papers span option bias measurement, robustness stress testing, behavioral bias detection, adversarial ethics, error taxonomy, confidence calibration, and signaling theory analysis.

### Overall Assessment

**Strengths:**
- **Genuine novelty** in applying established ML evaluation paradigms (perturbation robustness, calibration, format-comparison) to professional financial certification — no prior work has done this comprehensively
- **Coherent research program** — the 7 papers form an interlocking suite where findings cross-reference meaningfully
- **Methodological rigor** in core experiments (McNemar's test with Yates' correction, paired designs, full-sample coverage)
- **Corrective integrity** — empty response bias was identified and corrected rather than hidden (A5, I2)

**Weaknesses:**
- **Asymmetric evaluation methodology** in the flagship A5 experiment (letter matching vs. hybrid numerical+judge scoring) threatens the core "option bias" claim
- **Small sample sizes** in P4 (N=47) and P6 (N=90) limit generalizability
- **Single-model primary results** — most papers present GPT-4o-mini as the primary model with GPT-5-mini as cross-validation; would benefit from 3+ models
- **LLM-as-judge reliability** — the ~55% correct rate on empty responses was caught, but the fundamental judge reliability concern (60–68% expert domain agreement per survey literature) remains unaddressed
- **JSON vs. paper data discrepancy** for A5 GPT-5-mini (86.3% in file vs. 83.2% in paper) — correction is justified but JSON file was never updated, creating auditability concerns

### Verdict
5 of 7 papers are suitable for Finance Research Letters with revisions. P7 (Signaling Theory) is the strongest contribution. P4 (Adversarial Ethics) and P3 (Behavioral Biases) face the most significant challenges.

---

## 2. Literature Comparison & Novelty Assessment

### Papers Surveyed: 46+ across 6 categories

| Category | Papers Reviewed | Key Sources |
|----------|----------------|-------------|
| MCQ format bias | 4 | Zheng et al. (ICLR 2024 Spotlight), Balepur et al. (ACL 2025), Myrzakhan et al. (Open-LLM-Leaderboard 2024), Sanchez Salido et al. (2025) |
| CFA/financial exam evaluation | 6 | Callanan et al. (FinNLP/IJCAI 2024), Mahfouz et al. (EMNLP 2024 Industry), Patel et al. (arXiv 2025), Jagabathula et al. (NYU/arXiv 2025), CFA-Based Benchmark (arXiv 2509.04468), FinDAP (EMNLP 2025 Oral) |
| Memorization/robustness | 8 | GSM-Symbolic (ICLR 2025), GSM-Plus (ACL 2024), GSM-DC (EMNLP 2025), MATH-Perturb (ICML 2025), Lopez-Lira memorization (2025), RECALL (ACL 2024), Mosaic Memory (Nature Comms 2026), Generalization vs. Memorization (ICLR 2025) |
| Behavioral biases in LLMs | 4 | LLM Economicus (COLM 2024), Suri et al. (J. Exp. Psych. 2024), Malberg et al. (NLP4DH 2025), Capraro et al. (PNAS 2025) |
| Calibration/confidence | 5 | Xiong et al. (ICLR 2024), QA-Calibration (ICLR 2025), Mind the Confidence Gap (TMLR 2025), KalshiBench (2025), UQ Survey (KDD 2025) |
| Adversarial safety/ethics | 6 | FITD (EMNLP 2025), HarmBench (ICML 2024), JailbreakBench (NeurIPS 2024), TRIDENT (2025), LLM Ethics Benchmark (Sci. Reports 2025), Andriushchenko et al. (ICLR 2025) |
| Signaling theory/AI impact | 4 | Galdin & Silbert (Princeton 2025), AI & Higher Ed Signaling (MDPI 2024), "Can AI Distort Human Capital?" (2024), "Reasoning Models Ace CFA" (arXiv 2025) |
| LLM-as-judge reliability | 4 | CALM (NeurIPS 2024), Chen et al. (EMNLP 2024), Survey on LLM-as-Judge (2024), Noisy Rationales (NeurIPS 2024) |
| Financial LLM benchmarks | 5 | FinEval (2023), FinanceBench (2023), FinBen (NeurIPS 2024), BloombergGPT (2023), FinGPT (2023) |

### Novelty Verdict Per Paper

| Paper | Closest Prior Work | Novel Contribution? | Novelty Rating |
|-------|-------------------|---------------------|---------------|
| **P1** (Option Bias) | Open-LLM-Leaderboard (Myrzakhan 2024) — MCQ→open conversion on MMLU | **YES.** First MCQ vs. open-ended comparison on financial domain questions. First to show model-dependent option bias (p=0.251→p<0.001). Three-tier evaluation (A/B/C) is novel grading scheme. | ★★★★☆ |
| **P2** (Stress Test) | GSM-Symbolic (ICLR 2025) — noise/perturbation on math | **YES.** First counterfactual perturbation + noise injection on CFA questions. Domain-specific noise taxonomy (N1–N4) is novel. "Memorization gap" metric applied to professional knowledge is new. | ★★★★☆ |
| **P3** (Behavioral Biases) | LLM Economicus (COLM 2024) — behavioral biases via utility theory | **PARTIAL.** Loss aversion, anchoring, framing overlap with Ross et al. P3's novelty lies in finance-specific paired scenarios (CFA-level investment contexts) and bias types not tested elsewhere (herding, sunk cost). | ★★★☆☆ |
| **P4** (Adversarial Ethics) | TRIDENT (2025) — financial safety benchmark, FITD (EMNLP 2025) — multi-turn jailbreak | **YES.** No prior work tests adversarial flip of professional ethics judgments (as opposed to safety refusal). CFA-specific pressure taxonomy and ERS metric are novel. GPT-5-mini immunity finding is striking. | ★★★☆☆ |
| **P5** (Error Atlas) | CFA-Based Benchmark (2509.04468) — CFA error taxonomy; FLARE (ACL 2025) — error classification | **YES.** Golden Context Injection (GCI) as diagnostic oracle experiment has no precedent. Finding that only 50.4% of errors are fully recoverable even with perfect context is novel and practically important. | ★★★★☆ |
| **P6** (Calibration) | Xiong et al. (ICLR 2024) — LLM confidence calibration | **PARTIAL.** Calibration on CFA questions is new domain application. Confidence-at-Risk (CaR) metric bridging VaR and LLM calibration is genuinely novel. But N=90 limits impact. | ★★★☆☆ |
| **P7** (Signaling Theory) | Galdin & Silbert (Princeton 2025) — AI + Spence signaling in freelance markets | **YES.** First formal application of Spence signaling model to professional CFA certification disruption. Partial Signaling Collapse Theorem is original theoretical contribution. Empirical grounding via A5 data is well-integrated. | ★★★★★ |

### Key Finding: No Substantially Identical Prior Work

**None of the 46+ papers surveyed has performed a substantially identical experiment to any of the 7 papers.** The closest overlaps are:
1. P3 vs. LLM Economicus — both test behavioral biases but in different domains with different methods
2. P2's I3 vs. GSM-Symbolic — same perturbation paradigm applied to different domain
3. P6 vs. Xiong et al. — same calibration approach applied to different domain

The key differentiator is the **systematic application to professional financial knowledge (CFA exam questions)** with **domain-specific experimental designs**, which is appropriate for Finance Research Letters.

---

## 3. Data Integrity Audit

### Methodology
All experimental result JSON files were programmatically read and cross-referenced against claims in the 7 paper LaTeX files and MEMORY.md documentation.

### Verification Results

| Experiment | JSON Value | Paper Claim | Match? |
|-----------|-----------|-------------|--------|
| A5 GPT-4o-mini with options | 82.6% | 82.6% | ✅ |
| A5 GPT-4o-mini without options | 80.6% | 80.6% | ✅ |
| A5 GPT-4o-mini bias | +1.9pp | +1.9pp | ✅ |
| A5 GPT-4o-mini McNemar p | 0.251 | n.s. | ✅ |
| **A5 GPT-5-mini without options** | **86.3%** | **83.2%** | **⚠️ DISCREPANCY** |
| **A5 GPT-5-mini bias** | **+6.5pp** | **+9.6pp** | **⚠️ DISCREPANCY** |
| A5 GPT-5-mini with options | 92.8% | 92.8% | ✅ |
| A5 GPT-5-mini McNemar p | <0.001 | <0.001 | ✅ |
| A1 GPT-4o-mini Level A/B/C | 253/222/557 | 253/222/557 | ✅ |
| A1 GPT-5-mini Level A/B/C | 431/230/371 | 431/230/371 | ✅ |
| I1 GPT-4o-mini gap | 18.6pp | 18.6pp | ✅ |
| I1 GPT-5-mini gap | 36.4pp | 36.4pp | ✅ |
| I3 all NSI values (both models) | All match | All match | ✅ |
| I2 GPT-4o-mini avg bias | 0.500 | 0.500 | ✅ |
| D6 GPT-4o-mini flips | 14 | 14 | ✅ |
| D6 GPT-5-mini flips | 0 | 0 | ✅ |
| E1 GPT-4o-mini recovery | 82.4% | 82.4% | ✅ |
| E1 GPT-5-mini recovery | 88.3% | 88.3% | ✅ |
| E1 GPT-5-mini full recovery | 50.4% | 50.4% | ✅ |
| D1 total observations | 257 | 257 | ✅ |

### Critical Discrepancy: A5 GPT-5-mini

**Issue:** The JSON file (`run_20260207_174114/results.json`) shows `accuracy_without_options = 0.8634` (86.3%), yielding +6.5pp option bias. Both P1 and P7 report 83.2% without options and +9.6pp bias.

**Explanation:** This discrepancy is documented in MEMORY.md and arises from a **post-hoc correction** for empty responses:
- 58 out of 1,032 "without-options" responses were empty (model returned no content)
- The LLM-as-judge scored 32 of these 58 empty responses as "CORRECT" (55% rate)
- The authors conservatively treated all 58 empty responses as INCORRECT
- Corrected: 891 - 32 = 859 correct → 859/1032 = 83.2%
- Corrected: McNemar b=146, c=47, chi² = 49.76, p<0.001

**Assessment:** The correction is **methodologically defensible** — scoring empty responses as correct is clearly an artifact of judge limitations. However:
1. **The JSON file was never updated** to reflect the correction, creating an auditability gap
2. **No correction script exists** in the repository — the correction was applied manually to the LaTeX
3. A reviewer with access to the JSON would find numbers that don't match the paper
4. **Recommendation:** Create a documented post-processing script that applies the empty-response correction and generates the final figures used in papers

### GPT-5-mini I2 Data: Correctly Removed

The I2 behavioral biases experiment with GPT-5-mini produced 80% empty responses, resulting in an artifactual mean bias score of 0.892 (empty responses scored as bias=1.0 by the judge). Only 12/60 scenarios had non-empty responses (actual avg ≈ 0.458). **The decision to remove this data from P3 is correct and commendable.** The paper should explicitly mention this removal and the reason.

### E1 GCI GPT-5-mini: Verified

The full run (`golden_context_gpt-5-mini_20260207_220440.json`) with N=557 errors was verified. Despite 51 empty responses (9.2%), the aggregate results (50.4% full, 37.9% partial, 11.7% still wrong, 88.3% any recovery) match the paper exactly. The empty response rate is within acceptable bounds for a reasoning-intensive task with GPT-5-mini.

---

## 4. Methodology Critique

### 4.1 Critical Issues (Must Address)

**ISSUE 1: Asymmetric Evaluation in A5 Option Bias (Affects P1, P7)**

The core "option bias" measurement compares:
- **WITH options:** Standard MCQ letter extraction (`extract_answer()`) → exact character match
- **WITHOUT options:** Hybrid evaluation — numerical tolerance (±2%) attempted first, then LLM-as-judge fallback

This is **not a controlled comparison.** The "without options" condition uses a fundamentally different (and arguably more lenient for numerical questions, more variable for text questions) evaluation methodology. The measured "option bias" thus conflates:
1. True format-dependent performance difference
2. Evaluation methodology difference

**Severity: HIGH.** This is the most significant methodological concern across all 7 papers. The core finding (option bias exists and is model-dependent) is likely still directionally correct, but the magnitude (+1.9pp, +9.6pp) may be confounded by evaluation asymmetry.

**Mitigation:** The fact that GPT-4o-mini shows a non-significant +1.9pp bias (p=0.251) while GPT-5-mini shows +9.6pp (p<0.001) using the **same evaluation pipeline** suggests the model-dependent finding is robust even if absolute magnitudes are imprecise.

**ISSUE 2: LLM-as-Judge Empty Response Bias (Affects All Papers Using Judge)**

The `semantic_match_judge()` function has no validation for empty student answers. When the student answer is empty or near-empty:
- The judge receives an empty string and essentially guesses
- Approximately 55% of such judgments are "CORRECT"
- This systematically biases results upward

**Already addressed:** The A5 correction (83.2%) and I2 removal account for known instances. However, other experiments (A1, I1) that use the judge may have undetected empty responses.

**ISSUE 3: validate_perturbation() Never Called in I1 (Affects P2)**

The codebase defines a comprehensive `validate_perturbation()` function in `perturb.py` that verifies perturbation quality using an LLM call. However, this function is **never invoked** in `run_experiment.py`. The actual validation is minimal:
- Query length > 20 characters
- Not identical to original
- Non-empty answer

An estimated 10–20% of perturbations may be invalid (nonsensical questions, incorrect new answers), which could bias the memorization gap measurement **downward** (invalid perturbations are harder to answer correctly, inflating the gap).

### 4.2 Moderate Issues (Should Address)

**ISSUE 4: Confidence Calculation Bug in D1 (Affects P6)**

Self-consistency confidence divides by total `k` rather than `len(valid)`:
```python
confidence = majority_count / k  # Should be / len(valid)
```
If 3 of 10 responses fail answer extraction, confidence is computed as majority/10 instead of majority/7, artificially depressing confidence estimates by ~30%. This affects ECE and CaR calculations.

**ISSUE 5: Answer Extraction Silent Failures (Affects All)**

`extract_answer()` returns `None` silently when all 5 regex layers fail. The caller treats None as incorrect without logging. No aggregate statistics on extraction failure rate are computed. If 5% of responses have unparseable formats, those questions are silently marked as wrong.

**ISSUE 6: Numerical Extraction Takes Last Number (Affects P1 A1)**

The fallback in `extract_numerical_answer()` takes the **last number** in the response text, which may be an intermediate calculation rather than the final answer.

### 4.3 Minor Issues (Optional)

- `tolerance_match()` for gold=0 allows any prediction in [-0.02, 0.02] — rarely triggered but technically too lenient
- Judge JSON fallback uses keyword matching ("correct" in text) — could produce false positives
- I3 noise injection has no validation that the injected noise actually changed the query
- E1 golden context judge parsing uses non-robust regex for JSON extraction

---

## 5. Per-Paper Reviews

---

### Paper 1 (P1): Beyond Multiple Choice — Option Bias + Three-Tier Evaluation
**Experiments:** A1_open_ended + A5_option_bias | **N=1,032** | **Words: ~3,719**

#### Score: 78/100

#### Decision: Accept with Major Revisions

#### Strengths
1. **Novel experimental design:** First systematic MCQ vs. open-ended comparison on professional financial questions (N=1,032). No prior work has done this in the finance domain.
2. **Striking finding:** The "Option Bias Paradox" — GPT-5-mini shows +9.6pp bias (p<0.001) while GPT-4o-mini shows only +1.9pp (p=0.251, n.s.) — is genuinely surprising and has high citation potential. It challenges the intuition that stronger models are less format-dependent.
3. **Three-tier evaluation (A/B/C):** The Level A (exact match) / Level B (directionally correct) / Level C (incorrect) grading of open-ended responses adds nuance beyond binary scoring.
4. **Full-sample design:** Using all 1,032 CFA-Easy questions provides strong statistical power.
5. **McNemar's test with Yates' correction** is the appropriate paired statistical test.

#### Weaknesses
1. **CRITICAL — Asymmetric evaluation (§4.1):** The WITH-options condition uses letter matching while the WITHOUT-options condition uses a hybrid of numerical tolerance + LLM-as-judge. This is the paper's most significant vulnerability. A reviewer will immediately note that you are not comparing like with like.
2. **A5 GPT-5-mini data correction:** The 83.2% figure (correcting for 58 empty responses) is methodologically sound but creates an auditability problem when the JSON shows 86.3%. Should be documented transparently in the paper with a footnote or methodology section.
3. **Mechanism explanation is thin:** The "convergence anchoring" hypothesis for why GPT-5-mini has larger bias is plausible but speculative. Adding the process-of-elimination discussion helps but doesn't provide causal evidence.
4. **Only 2 models tested.** The field norm for format-bias studies is 5+ models (cf. Zheng et al. ICLR 2024 tested 20 models; Myrzakhan et al. tested multiple).

#### Missing Literature
- Open-LLM-Leaderboard (Myrzakhan et al., 2024) — the closest prior work converting MCQs to open-ended format, applied to MMLU. Must be cited and differentiated.
- "None of the Others" (Sanchez Salido et al., 2025) — simpler methodology testing same hypothesis on MMLU.
- Zheng et al. (ICLR 2024 Spotlight) — MCQ selection bias (tests position bias, not format bias, but must be discussed).

#### Specific Revisions Needed
1. Add a paragraph in Methodology explicitly acknowledging the evaluation asymmetry and arguing why it does not invalidate the model-comparison finding
2. Add a footnote or "Data Processing" subsection documenting the empty-response correction
3. Cite and differentiate from Open-LLM-Leaderboard
4. Consider a sensitivity analysis: what is the option bias if you use ONLY judge scoring for both conditions?

---

### Paper 2 (P2): Stress Testing — Counterfactual Perturbation + Noise Injection
**Experiments:** I1_counterfactual + I3_noise_red_herrings | **N=1,032** | **Words: ~4,367**

#### Score: 82/100

#### Decision: Accept with Minor Revisions

#### Strengths
1. **Strong experimental design:** Counterfactual perturbation (I1) + noise injection (I3) provide complementary robustness tests. The paired design (same questions, modified versions) enables clean comparison.
2. **Striking cross-model finding:** GPT-5-mini has nearly double the memorization gap (36.4pp vs. 18.6pp) despite higher baseline accuracy. This "scaling paradox" is highly quotable.
3. **Domain-specific noise taxonomy (N1–N4)** is a genuine contribution: numerical surface noise, domain-specific irrelevant information, contradictory premises, and excessive detail are CFA-relevant noise types not found in GSM-Symbolic or GSM-DC.
4. **Noise Sensitivity Index (NSI)** provides a standardized metric for cross-noise-type comparison.
5. **Full-sample coverage** (N=1,032) with reasonable valid perturbation counts (702 for GPT-4o-mini, 638 for GPT-5-mini).

#### Weaknesses
1. **validate_perturbation() unused (§4.1 Issue 3):** The perturbation quality validation function exists in code but is never called. An unknown fraction of perturbations may be mathematically invalid. This primarily biases the memorization gap upward (making the finding appear stronger than it is).
2. **GSM-Symbolic must be cited prominently:** The perturbation-injection paradigm was established by GSM-Symbolic (ICLR 2025) and GSM-Plus (ACL 2024). P2 must position itself as a domain-specific application and extension, not as if the paradigm is new.
3. **N4 (excessive detail) shows negative NSI:** Both models perform BETTER with excessive detail (-0.072, -0.041). This is counter-intuitive and underdiscussed. Is this because the added context provides useful cues? This finding deserves more space.
4. **Perturbation answer format inconsistency:** If a perturbation changes a numerical question to MCQ or vice versa, the evaluation measures different skills for perturbed vs. original.

#### Missing Literature
- GSM-Symbolic (Mirzadeh et al., ICLR 2025) — **must be cited as primary methodological precedent**
- GSM-Plus (Li et al., ACL 2024) — perturbation taxonomy for math
- GSM-DC (Yang et al., EMNLP 2025) — distractor injection
- MATH-Perturb (ICML 2025) — perturbation-based memorization detection
- Lopez-Lira et al. (2025) — memorization problem in financial LLMs (forecasting, not exam)
- Mosaic Memory (Nature Comms 2026) — theoretical basis for why perturbation works

#### Specific Revisions Needed
1. Add "Related Work" paragraph positioning P2 within the GSM-Symbolic paradigm family
2. Discuss the N4 negative NSI finding more thoroughly — is "more information helps" a genuine phenomenon?
3. Add a limitations paragraph noting that perturbation quality was not independently validated

---

### Paper 3 (P3): Inherited Irrationality — Behavioral Biases in LLMs
**Experiments:** I2_behavioral_biases | **N=60 scenarios** | **Words: ~3,395**

#### Score: 62/100

#### Decision: Revise and Resubmit

#### Strengths
1. **Creative scenario design:** 60 purpose-built paired scenarios across 6 bias types (loss aversion, anchoring, framing, sunk cost, herding, overconfidence) in CFA-relevant investment contexts.
2. **Mean bias score of 0.500** for GPT-4o-mini is a striking finding — the model is exactly at the boundary between rational and biased behavior.
3. **Debiasing hierarchy** (structured > instructional > contextual) is a practical contribution for practitioners.
4. **Finance-specific scenarios** differentiate from LLM Economicus (which uses abstract economic games) and Suri et al. (which uses classic Kahneman-Tversky paradigms).

#### Weaknesses
1. **N=60 is small.** Each bias type has only 10 scenarios. With this sample size, the per-bias-type analysis lacks statistical power. A reviewer will question whether 10 paired comparisons per bias type can support the claims made.
2. **Substantial overlap with existing literature:** LLM Economicus (COLM 2024), Suri et al. (J. Exp. Psych. 2024), and Malberg et al. (NLP4DH 2025) have all tested anchoring, framing, and loss aversion in LLMs. P3 must explicitly differentiate from each.
3. **Single primary model (GPT-4o-mini):** Cross-model comparison was removed (correctly) due to GPT-5-mini data corruption. But a single-model study is weaker for a bias paper. At minimum, one additional model (e.g., Claude, Gemini) would strengthen the claims.
4. **LLM-as-judge for bias scoring is problematic:** The bias scorer uses the same GPT-4o-mini as the judge, creating a self-evaluation concern. If the model has systematic biases, its judge may fail to detect them.
5. **"Inherited" framing is unsupported:** The title "Inherited Irrationality" implies biases are passed from training data to model behavior, but no analysis of training data composition is provided to support this causal claim.

#### Missing Literature
- LLM Economicus (Ross, Kim, Lo, COLM 2024) — **must be cited and extensively differentiated**
- Suri et al. (J. Exp. Psych. 2024) — tested same bias types in GPT-3.5
- Malberg et al. (NLP4DH 2025) — comprehensive cognitive bias evaluation across 8 types
- Capraro et al. (PNAS 2025) — amplified cognitive biases in moral decision-making

#### Specific Revisions Needed
1. Add a dedicated comparison paragraph with LLM Economicus and Suri et al.
2. Acknowledge the small sample size explicitly and frame per-bias-type results as exploratory
3. Soften the "inherited" causal framing unless training data analysis is added
4. Consider adding one more model to strengthen cross-model validity

---

### Paper 4 (P4): Under Pressure — Adversarial Ethics
**Experiments:** D6_adversarial_ethics | **N=47** | **Words: ~3,536**

#### Score: 58/100

#### Decision: Reject with Encouragement to Resubmit

#### Strengths
1. **Novel experiment:** No prior work tests whether adversarial prompting can flip professional ethics judgments (as opposed to general safety refusal). The distinction between ethical judgment consistency and safety alignment is important.
2. **Striking cross-model finding:** GPT-4o-mini shows 14 flips while GPT-5-mini shows 0 — complete immunity. This is a powerful result if it withstands scrutiny.
3. **Ethics Robustness Score (ERS)** and mapping to specific CFA Standards (I(A), III(A), III(C), III(E)) connect the experiment to the regulatory framework.
4. **Pressure taxonomy** (authority, utilitarian, slippery slope, peer pressure, financial incentive) is well-designed and draws on established social psychology.
5. **Data contamination discussion** was added (per reviewer feedback) and provides reasonable counter-arguments to the "too perfect" concern.

#### Weaknesses
1. **FATAL — N=47.** This is the complete CFA-Easy ethics subset, so expansion within this dataset is impossible. But 47 observations are insufficient for the quantitative claims made. The per-pressure-type analysis (dividing 47 questions across 5 types ≈ 9.4 per type) has essentially zero statistical power. The McNemar test is valid for the aggregate but meaningless for subgroup analysis.
2. **Zero flips remains suspicious.** The data contamination discussion helps but doesn't fully resolve the concern. If GPT-5-mini has memorized the correct answers and associated ethical reasoning, adversarial pressure may be ineffective simply because the model defaults to a cached response, not because it has robust ethical reasoning. The paper cannot distinguish between:
   - True ethical robustness (model reasons through the pressure and rejects it)
   - Memorization-based immunity (model ignores the pressure because it's matching a memorized pattern)
   This is especially concerning given P2's finding that GPT-5-mini has a 36.4pp memorization gap.
3. **Single-prompt design:** Each question gets one adversarial prompt. FITD (EMNLP 2025) showed that multi-turn escalation is far more effective at compromising model behavior. P4's single-prompt design may underestimate true vulnerability.
4. **No human baseline.** How many CFA charterholders would flip their ethical judgment under the same pressure prompts? Without a human comparison, it's impossible to contextualize the 14/47 flip rate.

#### Missing Literature
- FITD (EMNLP 2025) — multi-turn jailbreak via psychological escalation (must cite)
- TRIDENT (2025) — financial safety benchmark using CFA ethics principles (must cite)
- Andriushchenko et al. (ICLR 2025) — adaptive attacks bypass safety alignment
- HarmBench (ICML 2024) and JailbreakBench (NeurIPS 2024) — standard benchmarks

#### Specific Revisions Needed
1. Reframe conclusions to match the limited sample size — replace any claims of "systematic" patterns with "exploratory evidence"
2. Add a paragraph explicitly discussing the memorization-vs-robustness confound (cross-reference P2's memorization gap finding)
3. Cite FITD and discuss multi-turn escalation as a limitation
4. Consider expanding to additional ethics datasets (e.g., professional ethics scenarios from other certifications)

---

### Paper 5 (P5): CFA Error Atlas — Error Taxonomy + Golden Context Injection
**Experiments:** E1_error_analysis | **N=557 errors** | **Words: ~2,627**

#### Score: 76/100

#### Decision: Accept with Minor Revisions

#### Strengths
1. **GCI is genuinely novel.** Golden Context Injection as a diagnostic oracle experiment — providing perfect context and measuring recovery — has no precedent in the literature. The finding that only 25.5% (GPT-4o-mini) / 50.4% (GPT-5-mini) achieve full recovery even with perfect context is a significant diagnostic result.
2. **Error taxonomy is domain-specific and detailed.** The 68.8% conceptual error finding has practical implications for AI advisory system design.
3. **Clean interpretation:** Knowledge gaps (recoverable with context) vs. reasoning gaps (not recoverable) is a useful and actionable distinction.
4. **Cross-model validation** with GPT-5-mini (88.3% recovery rate, N=557) was verified correct.
5. **Financial theory connection** (added per reviewer feedback) linking to EMH and advisory reliability strengthens the paper's fit for FRL.

#### Weaknesses
1. **Word count (2,627) is on the low end for FRL.** The paper reads more like a technical report than a research paper. More discussion of implications, limitations, and connections to existing error taxonomy literature would strengthen it.
2. **GCI conflates knowledge gaps with attention/instruction effects (§4.3 Issue):** A model that already "knows" the concept but failed to apply it may show recovery due to better focus from the injected context, not because of genuine knowledge gap filling. The distinction between "didn't know" and "didn't attend to what it knew" is not made.
3. **Error categories are manually assigned.** Inter-rater reliability or validation of category assignments is not reported.
4. **E1 GPT-5-mini had 51 empty responses (9.2%).** While aggregate numbers check out, the paper should acknowledge this.

#### Missing Literature
- CFA-Based Benchmark (arXiv 2509.04468) — uses same error categories (knowledge, reasoning, calculation, inconsistency) from Callanan et al.
- FLARE (ACL 2025) — structured error taxonomy for LLM classification failures
- Self-RAG (ICLR 2024 Oral) — the most relevant retrieval-augmented approach to compare with GCI

#### Specific Revisions Needed
1. Add a paragraph distinguishing GCI recovery from "attention enhancement" — propose that future work could inject irrelevant context as a control to distinguish true knowledge gaps from attention effects
2. Cite and differentiate from the CFA-Based Benchmark error taxonomy
3. Report inter-rater reliability for error category assignments (or acknowledge as limitation)
4. Acknowledge the 51 empty GPT-5-mini responses

---

### Paper 6 (P6): Confidently Wrong — Calibration + Overconfident Risk
**Experiments:** D1_confidence_calibration + D4_overconfident_risk | **N=90 questions, 257 observations** | **Words: ~3,463**

#### Score: 68/100

#### Decision: Revise and Resubmit

#### Strengths
1. **Confidence-at-Risk (CaR)** is a genuinely creative metric that bridges financial risk management (VaR) and LLM calibration. This concept has standalone value regardless of sample size.
2. **Practical relevance:** Overconfident AI financial advisors pose real regulatory risk. The paper's framing around financial risk is appropriate for FRL.
3. **Multiple calibration methods** tested (verbalized confidence, self-consistency, logprobs) provides methodological breadth.
4. **ECE, Brier Score, AUROC** — standard calibration metrics properly computed.

#### Weaknesses
1. **N=90 (257 observations) is small for a calibration study.** Calibration analysis requires sufficient data to populate reliability diagram bins. With 90 base questions and 257 observations, some confidence bins will have very few samples (< 10), making the reliability diagram unreliable. Topic-level analysis (e.g., Derivatives with ~27 questions) has essentially no statistical power.
2. **Confidence calculation bug (§4.2 Issue 4):** Self-consistency confidence divides by `k` instead of `len(valid)`, artificially depressing confidence estimates. This directly affects ECE and CaR calculations. **Must be investigated.**
3. **Fallback confidence of 0.5 on parse failure** injects noise into the calibration analysis.
4. **CFA-Challenge justification is reasonable but limiting.** The authors argue that hard questions are needed to test calibration (easy questions → high accuracy → ECE uninformative). This is valid, but it means the findings may not generalize to typical financial advisory tasks where questions are easier.
5. **No comparison to existing calibration literature.** Xiong et al. (ICLR 2024) reported calibration results on general QA — how does CFA-domain calibration compare?

#### Missing Literature
- Xiong et al. (ICLR 2024) — **must be cited as primary methodological predecessor**
- QA-Calibration (ICLR 2025) — group-wise calibration
- Mind the Confidence Gap (TMLR 2025) — overconfidence analysis
- KalshiBench (2025) — epistemic calibration via prediction markets

#### Specific Revisions Needed
1. **Investigate and fix the confidence calculation bug** (k vs. len(valid))
2. Report the number of valid responses per bin in the reliability diagram
3. Cite and compare with Xiong et al. calibration results
4. Acknowledge topic-level analysis as exploratory given small per-topic N

---

### Paper 7 (P7): When Machines Pass the Test — Signaling Theory
**Experiments:** Theoretical; cites A5 data | **N=1,032 (via A5)** | **Words: ~4,231**

#### Score: 88/100

#### Decision: Accept with Minor Revisions

#### Strengths
1. **Outstanding theoretical contribution.** The formal extension of Spence's (1973) signaling model with AI as a third player that reduces signaling costs is the most original contribution in the entire suite. The "Partial Signaling Collapse Theorem" is a genuinely novel result.
2. **Signaling Retention Ratio (28.8%)** is an elegant empirical application of the theoretical model using A5 data.
3. **Policy relevance.** The paper's recommendations for CFA Institute (format redesign, AI-resistant assessment, competency-based credentialing) are actionable and timely.
4. **Supported by concurrent empirical evidence:** "Reasoning Models Ace the CFA Exams" (Patel et al., 2025) shows frontier models now pass all CFA levels with near-perfect scores, directly supporting P7's theoretical argument.
5. **Interdisciplinary strength:** Successfully bridges labor economics (Spence), education theory, and AI evaluation in a way that is rigorous in each domain.

#### Weaknesses
1. **Empirical grounding relies entirely on P1's A5 data.** If the A5 option bias measurement is questioned (due to evaluation asymmetry), P7's empirical calibration weakens. The Signaling Retention Ratio (28.8%) derives from the corrected +9.6pp bias figure.
2. **The Partial Signaling Collapse Theorem assumes CFA exam captures a binary formalizable/tacit skill split.** In reality, the skill distribution is continuous, and many CFA topics blend both (e.g., ethics requires both knowledge of standards AND contextual judgment).
3. **No direct evidence of actual signaling value erosion.** The paper argues theoretically that signaling should erode, but provides no evidence that employers are actually devaluing CFA credentials. This is acknowledged but should be more prominent.
4. **The A5 data correction (83.2%, +9.6pp) actually STRENGTHENS the argument** compared to the original 86.3%, +6.5pp — but this asymmetric dependence on the corrected figure should be transparent.

#### Missing Literature
- Galdin & Silbert (Princeton 2025) — **must be cited:** applies Spence signaling to AI disruption of freelance market writing quality
- "Reasoning Models Ace the CFA Exams" (Patel et al., 2025) — empirical support
- AI & Higher Ed Signaling (MDPI 2024) — discusses AI + Spence + credentialing qualitatively

#### Specific Revisions Needed
1. Cite Galdin & Silbert (2025) — the most directly relevant parallel application of signaling theory
2. Add a sensitivity analysis: what would the Signaling Retention Ratio be using the uncorrected (86.3%) data?
3. Discuss the continuous nature of formalizable/tacit skills rather than treating it as strictly binary
4. Acknowledge the lack of direct employer behavior evidence more prominently

---

## 6. Cross-Paper Structural Issues

### 6.1 Data Reuse and Independence
P1 and P7 share the A5 option bias data. P5 uses the A1 error set (557 Level C responses). P2 uses the same 1,032 questions. This creates a dependency chain where a flaw in the base data (CFA-Easy N=1,032) propagates across 5 papers. **This is acceptable** for a research program submitted as a suite, but each paper should be self-contained and not assume the reader has read the others.

### 6.2 GPT-5-mini Empty Response Problem
GPT-5-mini produced empty responses in three experiments:
- A5: 58/1,032 (5.6%) — corrected
- I2: 48/60 (80%) — data removed
- E1: 51/557 (9.2%) — aggregate results still valid

This is a systematic issue with the model's reasoning token budget on complex tasks. The papers handle it correctly (correction, removal, acknowledgment) but should have a consistent approach. **Recommendation:** Add a "GPT-5-mini Response Quality" note in each cross-model paper.

### 6.3 LLM-as-Judge Consistency
All experiments use `gpt-4o-mini` as the judge model. The choice is consistent (which is good) but unvalidated against human expert judgment (which is a limitation). The LLM-as-judge survey literature (2024) reports only 60–68% agreement with domain experts. This systematic limitation should be acknowledged in each paper's Limitations section.

### 6.4 Dataset Provenance
All papers use SchweserNotes-derived questions via FinDAP. This is clearly stated. However, some CFA questions may overlap with the model's training data (benchmark contamination). P2's counterfactual experiment partially addresses this (the memorization gap IS the contamination measurement), but P1, P3, P4, P5, P6 do not control for contamination.

---

## 7. Scoring Summary

| Paper | Score | Decision | Key Strength | Key Weakness |
|-------|-------|----------|-------------|-------------|
| **P7** (Signaling) | **88** | Accept w/ Minor Rev | Original theoretical contribution; Partial Signaling Collapse Theorem | Relies entirely on P1's A5 data for empirical grounding |
| **P2** (Stress Test) | **82** | Accept w/ Minor Rev | Striking memorization gap finding (36.4pp); domain-specific noise taxonomy | Must position within GSM-Symbolic paradigm; unused validation function |
| **P1** (Option Bias) | **78** | Accept w/ Major Rev | Novel MCQ vs. open-ended comparison; model-dependent bias paradox | Asymmetric evaluation methodology is critical concern |
| **P5** (Error Atlas) | **76** | Accept w/ Minor Rev | GCI is genuinely novel diagnostic; practical implications for AI advisory | Short; conflates knowledge gaps with attention effects |
| **P6** (Calibration) | **68** | Revise & Resubmit | CaR metric is creative; regulatory risk framing appropriate | N=90 insufficient; confidence calculation bug |
| **P3** (Behavioral Biases) | **62** | Revise & Resubmit | Finance-specific paired scenarios; debiasing hierarchy | N=60 small; substantial overlap with existing literature; single model |
| **P4** (Adversarial Ethics) | **58** | Reject (Resubmit) | Novel experiment; complete GPT-5-mini immunity is striking | N=47 fatal; cannot distinguish robustness from memorization |

### Score Distribution Commentary
- **P7 and P2** are the strongest papers, with genuine theoretical/empirical novelty and sufficient sample sizes
- **P1 and P5** are solid but require addressing the asymmetric evaluation concern (P1) and adding depth (P5)
- **P6 and P3** have interesting ideas (CaR, finance-specific biases) but are limited by small samples
- **P4** faces the most fundamental challenge: N=47 cannot support the claims made, and the zero-flips result is confounded by memorization

---

## 8. New Research Directions

Based on gaps identified through this comprehensive review, the following directions emerge:

### Direction 1: Multi-Model Format Bias Landscape
**Motivation:** P1 shows option bias is model-dependent (n.s. for GPT-4o-mini, p<0.001 for GPT-5-mini). Extending to 10+ models (including Claude, Gemini, Llama, DeepSeek) with the same CFA-Easy questions would map the "format bias landscape" across model families and sizes. The Open-LLM-Leaderboard (Myrzakhan 2024) did this for MMLU but not for domain-specific financial questions.

### Direction 2: Dynamic/Procedural CFA Question Generation
**Motivation:** Data contamination concerns affect all 7 papers. A system that generates novel CFA-style questions from financial first principles (e.g., given a set of economic parameters, generate a valid CFA-level question with verified solution) would eliminate contamination concerns entirely. GSM-Symbolic's template approach could be adapted for financial questions.

### Direction 3: Multi-Turn Adversarial Ethics Escalation
**Motivation:** P4's single-prompt design likely underestimates adversarial vulnerability. Following FITD (EMNLP 2025), a multi-turn escalation experiment on CFA ethics would be more realistic (e.g., a client progressively pressuring a financial advisor AI). This also addresses P4's N=47 limitation by generating more interaction data per question.

### Direction 4: Calibration-Weighted Advisory Systems
**Motivation:** P6's CaR metric could be operationalized in a real advisory system: an AI financial advisor that weights its recommendations by calibrated confidence, flagging high-uncertainty responses for human review. Evaluating such a system on CFA questions would bridge P6's theoretical framework with practical deployment.

### Direction 5: Human Expert Baseline Comparisons
**Motivation:** None of the 7 papers compare LLM performance against human CFA candidates or charterholders. A study comparing:
- Option bias in human test-takers vs. LLMs
- Memorization gap (counterfactual perturbation) in humans vs. LLMs
- Behavioral biases in human financial advisors vs. LLMs
would provide essential context for interpreting the LLM results.

### Direction 6: Longitudinal Signaling Value Tracking
**Motivation:** P7's signaling theory predicts credential erosion. A longitudinal study tracking:
- CFA charterholder salary premiums over time (as AI capability increases)
- Employer survey data on perceived CFA value
- CFA exam registration trends
would provide empirical validation of the Partial Signaling Collapse Theorem.

### Direction 7: GCI with Controlled Irrelevant Context
**Motivation:** P5's GCI experiment cannot distinguish between "model didn't know the concept" and "model knew but didn't attend to it." Injecting **irrelevant** golden context (correct textbook content for a different topic) as a control condition would isolate the attention effect from genuine knowledge recovery.

### Direction 8: Reasoning Trace Analysis
**Motivation:** GPT-5-mini's reasoning tokens are hidden (not visible in output). If reasoning tokens become accessible (or using open-source reasoning models like DeepSeek-R1), analyzing the internal reasoning traces for:
- Where memorization patterns appear
- How adversarial pressure is processed
- Where reasoning derails on perturbed questions
would provide mechanistic insight that all 7 papers currently lack.

---

## Appendix: Literature References

### MCQ Format Bias
1. Zheng et al. "Large Language Models Are Not Robust Multiple Choice Selectors." ICLR 2024 Spotlight.
2. Pezeshkpour & Hruschka. "Large Language Models Sensitivity to The Order of Options in Multiple-Choice Questions." NAACL 2024.
3. Balepur, Rudinger, Boyd-Graber. "Which of These Best Describes Multiple Choice Evaluation with LLMs?" ACL 2025.
4. Sanchez Salido et al. "None of the Others: A General Technique to Distinguish Reasoning from Memorization." 2025.
5. Myrzakhan et al. "Open-LLM-Leaderboard: From Multi-choice to Open-style Questions." 2024.

### CFA/Financial Exam Evaluation
6. Callanan et al. "Can GPT Models Be Financial Analysts?" FinNLP/IJCAI 2024.
7. Mahfouz et al. "The State of the Art of LLMs on CFA Exams." EMNLP 2024 Industry.
8. Patel et al. "Reasoning Models Ace the CFA Exams." arXiv 2025.
9. Jagabathula et al. "Advanced Financial Reasoning at Scale: CFA Level III." arXiv 2025.
10. "Evaluating LLMs for Financial Reasoning: A CFA-Based Benchmark Study." arXiv 2509.04468, 2025.
11. Ke et al. "Demystifying Domain-adaptive Post-training for Financial LLMs (FinDAP)." EMNLP 2025 Oral.

### Memorization/Robustness
12. Mirzadeh et al. "GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning." ICLR 2025.
13. Li et al. "GSM-Plus: A Comprehensive Benchmark for Evaluating Robustness." ACL 2024.
14. Yang et al. "How Is LLM Reasoning Distracted by Irrelevant Context? (GSM-DC)" EMNLP 2025.
15. "MATH-Perturb: Benchmarking LLMs' Math Reasoning against Hard Perturbations." ICML 2025.
16. Lopez-Lira, Tang, Zhu. "The Memorization Problem: Can We Trust LLMs' Economic Forecasts?" 2025.
17. Liu et al. "RECALL: Robustness against External Counterfactual Knowledge." ACL 2024.
18. "The Mosaic Memory of Large Language Models." Nature Communications, 2026.
19. Dong et al. "Generalization or Memorization: Data Contamination." ACL 2024.
20. "Generalization v.s. Memorization: Tracing Language Models' Capabilities Back to Pretraining Data." ICLR 2025.

### Behavioral Biases in LLMs
21. Ross, Kim, Lo. "LLM Economicus? Mapping the Behavioral Biases of LLMs via Utility Theory." COLM 2024.
22. Suri et al. "Do LLMs Show Decision Heuristics Similar to Humans?" J. Exp. Psych.: General, 2024.
23. Malberg et al. "A Comprehensive Evaluation of Cognitive Biases in LLMs." NLP4DH 2025.
24. Capraro et al. "Large Language Models Show Amplified Cognitive Biases in Moral Decision-Making." PNAS 2025.

### Calibration/Confidence
25. Xiong et al. "Can LLMs Express Their Uncertainty?" ICLR 2024.
26. "QA-Calibration of Language Model Confidence Scores." ICLR 2025.
27. Chhikara. "Mind the Confidence Gap: Overconfidence, Calibration, and Distractor Effects." TMLR 2025.
28. "Do LLMs Know What They Don't Know? Evaluating Epistemic Calibration (KalshiBench)." 2025.
29. "Uncertainty Quantification and Confidence Calibration in LLMs: A Survey." KDD 2025.

### Adversarial Safety/Ethics
30. "Foot-In-The-Door: A Multi-turn Jailbreak for LLMs (FITD)." EMNLP 2025.
31. Mazeika et al. "HarmBench: Standardized Evaluation Framework for Automated Red Teaming." ICML 2024.
32. Chao et al. "JailbreakBench: Open Robustness Benchmark for Jailbreaking LLMs." NeurIPS 2024.
33. Hui et al. "TRIDENT: Benchmarking LLM Safety in Finance, Medicine, and Law." 2025.
34. "LLM Ethics Benchmark: Three-Dimensional Assessment System." Scientific Reports, 2025.
35. Andriushchenko et al. "Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks." ICLR 2025.

### Signaling Theory / AI Impact
36. Galdin & Silbert. "Making Talk Cheap: Generative AI and Labor Market Signaling." Princeton Economics, 2025.
37. "Artificial Intelligence and the Sustainability of the Signaling and Human Capital Roles of Higher Education." MDPI Sustainability, 2024.
38. Li & Zhou. "Can AI Distort Human Capital?" Working Paper, 2024.

### LLM-as-Judge
39. "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM)." NeurIPS 2024.
40. Chen et al. "Humans or LLMs as the Judge? A Study on Judgement Bias." EMNLP 2024.
41. "A Survey on LLM-as-a-Judge." arXiv 2411.15594, 2024.

### Financial LLM Benchmarks
42. Zhang et al. "FinEval: A Chinese Financial Domain Knowledge Evaluation Benchmark." 2023.
43. Islam et al. "FinanceBench: A New Benchmark for Financial Question Answering." 2023.
44. Xie et al. "FinBen: A Holistic Financial Benchmark for Large Language Models." NeurIPS 2024.
45. Wu et al. "BloombergGPT: A Large Language Model for Finance." 2023.
46. Yang et al. "FinGPT: Open-Source Financial Large Language Models." 2023.

### Additional
47. Liang et al. "Can Language Models Perform Robust Reasoning with Noisy Rationales?" NeurIPS 2024.
48. "Profit Mirage: Revisiting Information Leakage in LLM-based Financial Agents (FactFin)." 2025.
49. ESMA. "Leveraging Large Language Models in Finance: Pathways to Responsible Adoption." 2025.

---

*This review was conducted programmatically with full access to all experimental code, result files, and paper manuscripts. All data cross-references were verified against the actual JSON result files in the repository.*
