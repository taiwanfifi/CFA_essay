# D4: Overconfident Risk — When AI Is Confident and Wrong

## Research Question

Among LLM errors on CFA questions, which ones are *most dangerous*? We focus on **overconfident errors** — cases where the model is highly confident (≥80%) but incorrect — and classify them by financial risk severity.

This builds on D1 (confidence calibration) results.

---

## Pipeline

```
D1 calibration results
    → Filter: confidence ≥ 80% AND incorrect
    → GPT-4o classifies each error's financial risk
    → Risk matrix + collective hallucination detection
```

---

## Risk Severity Categories

| Severity | Description | Example |
|----------|-------------|---------|
| Critical | Could cause significant financial loss or regulatory violation | Wrong derivative pricing, misapplied ethics standard |
| High | Could mislead investment decisions | Wrong bond valuation, incorrect cost of capital |
| Medium | Conceptual error that could propagate | Confused financial ratios |
| Low | Minor error unlikely to cause real harm | Rounding error |

---

## Worked Example

### D1 Result Entry

```json
{
    "question_id": "challenge_42",
    "question": "A portfolio manager discovers that an analyst...",
    "correct_answer": "B",
    "answer": "A",
    "correct": false,
    "confidence": 0.92,
    "method": "verbalized"
}
```

### Risk Classification (by GPT-4o)

```json
{
    "risk_severity": "critical",
    "risk_category": "Ethics/Compliance",
    "real_world_impact": "Misidentifying the applicable CFA Standard could lead a portfolio manager to take improper action, potentially resulting in client harm and regulatory sanctions.",
    "error_mechanism": "Model confused Standard III(A) Loyalty with Standard I(B) Independence, both involve duty but apply to different situations."
}
```

### Collective Hallucination Detection

When 2+ models are overconfident and wrong on the same question, it's a **collective hallucination** — especially dangerous because ensemble methods would also fail.

```
Question challenge_42:
  - gpt-4o-mini: conf=92%, answer=A (wrong)
  - qwen3:32b:   conf=87%, answer=A (wrong)
  → Collective hallucination! Ensemble voting would also get this wrong.
```

---

## Running

```bash
# From D1 results (must exist)
python -m experiments.D4_overconfident_risk.run_experiment \
    --input "experiments/D1_confidence_calibration/results/run_*/results.json" \
    --confidence-threshold 0.8

# Limit classification to first 10 errors (for POC)
python -m experiments.D4_overconfident_risk.run_experiment \
    --input "experiments/D1_confidence_calibration/results/run_*/results.json" \
    --confidence-threshold 0.8 --limit 10

# Analysis
python -m experiments.D4_overconfident_risk.analysis \
    --input experiments/D4_overconfident_risk/results/run_*/results.json
```

---

## Output Format

```json
{
  "metadata": {
    "experiment": "D4_overconfident_risk",
    "confidence_threshold": 0.8,
    "n_classified": 15
  },
  "summary": {
    "total_overconfident_errors": 23,
    "severity_distribution": {"critical": 3, "high": 8, "medium": 9, "low": 3},
    "avg_confidence": 0.87,
    "collective_hallucinations": 2
  },
  "classified_errors": [...],
  "collective_hallucinations": [...]
}
```

---

## Dependencies

- `experiments/D1_confidence_calibration/results/` must contain completed runs
- `experiments/shared/` (config, llm_client)
- OpenAI API key (`OPENAI_API_KEY` env var)
