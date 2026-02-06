# I2 Theory Framework: Behavioral Biases in Financial LLMs
# Do LLMs Inherit Human Cognitive Biases in Financial Decision-Making?

## Paper Title
**Inherited Irrationality: Measuring Behavioral Finance Biases in Large Language Models**

**Target Journal**: Finance Research Letters (FRL) or Journal of Behavioral Finance

---

## 1. Research Hypotheses

### H1: Bias Inheritance
**LLMs trained on human-generated text exhibit measurable behavioral finance biases (loss aversion, anchoring, framing effects) that mirror well-documented human cognitive biases.**

- **Rationale**: LLMs learn from human-generated financial text (analyst reports, news, forums) that contains embedded cognitive biases. If the training process preserves these biases, LLM outputs will exhibit similar irrational patterns.
- **Operationalization**: Bias Score = fraction of responses exhibiting the target bias when presented with bias-inducing prompts (e.g., framing a loss vs. gain scenario).
- **Expected effect size**: Bias Score = 0.30–0.60 across bias types.

### H2: Loss Aversion Dominance
**Loss aversion is the most pronounced bias in financial LLMs, reflecting its prevalence in financial training data.**

- **Rationale**: Kahneman & Tversky's prospect theory shows loss aversion is the dominant human bias in financial decision-making, with losses weighing ~2.25× gains. Financial media disproportionately covers losses, amplifying this bias in training data.
- **Operationalization**: Compare loss aversion bias score against anchoring, framing, recency, disposition, and overconfidence.

### H3: Bias-Accuracy Dissociation
**Bias scores are not correlated with standard accuracy — a model can be highly accurate on standard CFA questions while exhibiting strong behavioral biases when the question framing is manipulated.**

- **Rationale**: Standard CFA questions are designed to have objectively correct answers; biases are triggered by how information is framed. A model can learn correct answers while also learning biased reasoning patterns.
- **Operationalization**: Pearson correlation between standard accuracy and bias score across models. Expect r ≈ 0.

### H4: Model Size Does Not Eliminate Bias
**Larger models do not systematically exhibit lower bias scores — the relationship between model size and bias is non-monotonic.**

- **Rationale**: Larger models have more capacity to absorb nuanced human reasoning patterns, including biases. Scaling may improve accuracy without reducing bias.
- **Operationalization**: Bias Score vs. log(model_size) regression.

---

## 2. Economic Significance

### 2.1 AI-Amplified Market Irrationality

If AI trading systems and advisory tools exhibit behavioral biases, they can amplify rather than correct market irrationality:

- **Loss-averse AI advisor**: Recommends selling winners too early and holding losers too long (disposition effect), destroying client portfolio value
- **Anchored AI analyst**: Anchors price targets to round numbers or recent prices rather than fundamentals, contributing to market inefficiency
- **Framing-sensitive AI risk assessment**: Risk evaluation changes based on how scenarios are presented, creating inconsistent risk management

The systemic risk: as AI adoption increases in finance, correlated biases across AI systems could create new sources of market instability.

### 2.2 Investor Protection

Behavioral finance research shows that human financial advisors exhibit cognitive biases that harm client outcomes. AI was expected to be bias-free. Our findings challenge this assumption:

- **Regulatory implication**: AI systems used for financial advisory should be tested for behavioral biases, just as human advisors are evaluated for fiduciary compliance
- **Disclosure requirement**: If an AI system exhibits measurable loss aversion, this should be disclosed to clients who may assume AI advice is bias-free

### 2.3 De-Biasing as Alpha Generation

If AI biases can be identified and corrected, contrarian strategies become possible:
- An AI that is aware of its own anchoring bias can deliberately counter-adjust
- Detecting bias in competing AI systems creates trading opportunities
- Our bias measurement framework provides the diagnostic tool for systematic de-biasing

---

## 3. Discussion Points

### 3.1 Nature vs. Nurture of AI Biases
Are AI biases inherited from training data (nurture) or emergent from the architecture (nature)? Loss aversion may be training-data-driven (financial media bias), while anchoring may be architecture-driven (attention mechanism sensitivity to salient numbers).

### 3.2 Implications for Behavioral Finance Theory
If AI replicates human biases, this strengthens the case that biases arise from information processing patterns (which AI shares) rather than emotional responses (which AI lacks).

### 3.3 The De-Biasing Paradox
Attempts to de-bias AI (through RLHF or explicit prompting) may introduce new biases or reduce useful heuristics. The optimal strategy may be bias-awareness rather than bias-elimination.

---

## 4. Key References

- Kahneman, D. & Tversky, A. (1979). Prospect Theory. Econometrica.
- Shefrin, H. & Statman, M. (1985). The Disposition to Sell Winners Too Early. JF.
- Tversky, A. & Kahneman, D. (1974). Judgment Under Uncertainty: Heuristics and Biases. Science.
- Erev, I. et al. (2017). From anomalies to forecasts. Psychological Review.
