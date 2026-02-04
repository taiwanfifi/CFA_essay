# I1: Counterfactual Testing — Detecting Memorization

## Research Question

When an LLM answers a CFA question correctly, is it *reasoning* or *remembering*? We test this by creating **perturbed versions** of questions (changing numerical parameters) and checking if the model can still answer correctly.

---

## Method

```
Original question (correct answer known)
    → Perturb numerical parameters (GPT-4o generates variants)
    → Test model on original + perturbed versions
    → Compare: Memorization Gap = acc_original - acc_perturbed
```

---

## Perturbation Levels

| Level | What Changes | Example |
|-------|-------------|---------|
| 1 | Single parameter | Interest rate: 5% → 7% |
| 2 | Two parameters | Rate: 5%→7%, Maturity: 10yr→15yr |
| 3 | Question structure | "Find PV" → "Find the interest rate" |

---

## Worked Example

### Original Question

```
Q: At a 5% interest rate per year compounded annually, the PV of a 10-year
ordinary annuity with annual payments of $2,000 is $15,443.47.
The PV of a 10-year annuity due is closest to:
A: $14,709.02  B: $16,215.64  C: $17,443.47
Answer: B
```

### Level 1 Perturbation (rate change: 5% → 7%)

**GPT-4o prompt:**
```
Change the interest rate from 5% to 7%. Keep everything else the same.
Calculate the new correct answer.
```

**Generated perturbation:**
```json
{
    "perturbed_question": "At a 7% interest rate per year compounded annually,
    the PV of a 10-year ordinary annuity with annual payments of $2,000 is
    $14,047.16. The PV of a 10-year annuity due is closest to: ...",
    "perturbed_answer": "$15,030.46",
    "changes_made": ["interest rate changed from 5% to 7%"],
    "solution_steps": "PV_due = PV_ordinary × (1+r) = 14,047.16 × 1.07 = 15,030.46"
}
```

### Key Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Memorization Gap | acc_original - acc_perturbed | Positive = memorization |
| Robust Accuracy | correct on original AND all perturbations | True understanding |
| Consistency Score | 1 - gap / acc_original | 1.0 = fully robust |

---

## Running

```bash
# POC: 5 questions, Level 1 perturbation
python -m experiments.I1_counterfactual.run_experiment \
    --dataset easy --limit 5 --model gpt-4o-mini --perturbation-levels 1

# Multiple levels
python -m experiments.I1_counterfactual.run_experiment \
    --dataset easy --limit 5 --model gpt-4o-mini --perturbation-levels 1 2 3

# Analysis
python -m experiments.I1_counterfactual.analysis \
    --input experiments/I1_counterfactual/results/run_*/results.json
```

---

## Output Format

```json
{
  "metadata": {"model": "gpt-4o-mini", "dataset": "easy", "perturbation_levels": [1]},
  "summary": {
    "accuracy_original": 0.8,
    "perturbation_levels": {
      "1": {"n_valid": 5, "accuracy": 0.6, "memorization_gap": 0.2}
    },
    "robust_accuracy": 0.6,
    "memorization_suspect": 0.2
  },
  "results": [
    {
      "question_id": "easy_0",
      "original": {"answer": "B", "correct": true},
      "perturbations": [
        {
          "level": 1,
          "valid": true,
          "perturbed_answer": "15030.46",
          "model_answer": "A",
          "correct": false
        }
      ]
    }
  ]
}
```

---

## Dependencies

- `experiments/shared/` (config, llm_client, prompts, evaluation, data_loader)
- OpenAI API key (`OPENAI_API_KEY` env var)
