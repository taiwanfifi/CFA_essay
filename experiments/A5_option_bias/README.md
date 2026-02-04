# A5: Option Bias — Do MCQ Choices Help LLMs Cheat?

## Research Question

When an LLM answers a CFA question correctly in MCQ format, does it *actually know* the answer — or is it exploiting the option set to guess? We measure **option bias** by testing the same question in two formats:

- **Format A (MCQ):** Standard multiple-choice with A/B/C options
- **Format B (Open-ended):** Same question with choices removed; model must compute the answer independently

**Option bias** = questions where the model gets it right *only* with options present.

---

## Worked Example

### Original Question (CFA-Easy #9)

```
Q: An investment of €500,000 today that grows to €800,000 after six years has
a stated annual interest rate closest to:
CHOICES: A: 7.5% compounded continuously. B: 7.7% compounded daily.
C: 8.0% compounded semiannually.
Answer:
```

**Correct answer:** C (8.0% compounded semiannually)

### Format A — MCQ Prompt

**System:** You are a CFA exam expert. Read the question carefully, show your reasoning, then state your final answer as: ANSWER: X (where X is A, B, or C).

**User:** *(full question with choices)*

**Model output:**
```
We need: 500,000 × (1 + r/2)^12 = 800,000
(1 + r/2)^12 = 1.6
r/2 = 1.6^(1/12) - 1 = 0.03988
r = 0.07977 ≈ 8.0%
ANSWER: C
```

**Extraction:** regex → `C` → correct ✓

### Format B — Open-ended Prompt

**System:** You are a CFA exam expert. Solve the following problem step by step. Do NOT choose from multiple-choice options — compute and state your answer directly.

**User:**
```
An investment of €500,000 today that grows to €800,000 after six years has
a stated annual interest rate closest to:
```

**Model output:**
```
Using FV = PV × (1 + r)^n:
800,000 = 500,000 × (1 + r)^6
(1 + r)^6 = 1.6
r = 1.6^(1/6) - 1 = 0.08148 ≈ 8.15%

The stated annual interest rate is approximately 8.15%.
```

**Evaluation:** The question asks about *semiannual* compounding, but without options to hint at compounding frequency, the model defaults to annual compounding. The numerical answer (8.15%) doesn't match the gold answer for semiannual compounding (8.0%).

**→ This is an option-biased question.** The MCQ options (which mention "compounded semiannually") cue the model to use the right compounding method.

### LLM-as-Judge (for non-numerical answers)

For conceptual questions where numerical matching doesn't apply:

```
System: You are an expert CFA exam grader...
User: Question: [question] | Correct: [gold] | Student: [response]
→ {"correct": false, "reasoning": "Student assumed annual compounding..."}
```

---

## Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Accuracy (MCQ) | correct_mcq / N | Standard MCQ performance |
| Accuracy (Open) | correct_open / N | True understanding |
| Option Bias | acc_mcq - acc_open | Positive = options help |
| Bias Rate | biased_questions / N | % questions with bias |
| McNemar's p | χ²(1) | Statistical significance |

An **option-biased** question: correct with MCQ format AND incorrect in open-ended format.

---

## Model Configuration

| Model | Role | Why |
|-------|------|-----|
| gpt-4o-mini | Subject + Judge | Low cost, fast, POC default |
| gpt-4o | Subject | Stronger baseline |
| qwen3:32b | Subject | Local large model |
| llama3.1:8b | Subject | Small model, expect more bias |

---

## Running

```bash
# POC: 5 questions
python -m experiments.A5_option_bias.run_experiment \
    --dataset easy --limit 5 --model gpt-4o-mini

# Full easy dataset
python -m experiments.A5_option_bias.run_experiment \
    --dataset easy --model gpt-4o-mini

# Challenge dataset
python -m experiments.A5_option_bias.run_experiment \
    --dataset challenge --model gpt-4o-mini

# Analysis
python -m experiments.A5_option_bias.analysis \
    --input experiments/A5_option_bias/results/run_*/results.json
```

---

## Output Format

```json
{
  "metadata": {"dataset": "easy", "n_questions": 5, "model": "gpt-4o-mini"},
  "summary": {
    "accuracy_with_options": 0.8,
    "accuracy_without_options": 0.6,
    "option_bias": 0.2,
    "n_biased_questions": 1,
    "bias_rate": 0.2,
    "mcnemar_test": {"b": 1, "c": 0, "chi2": 0.0, "p_value": 1.0}
  },
  "results": [
    {
      "question_id": "easy_9",
      "correct_with_options": true,
      "correct_without_options": false,
      "answer_with": "C",
      "answer_without": "8.15%",
      "judge_verdict": "NUMERICAL_MISMATCH",
      "option_biased": true
    }
  ]
}
```

---

## Dependencies

- `experiments/shared/` (config, llm_client, prompts, evaluation, data_loader)
- OpenAI API key (`OPENAI_API_KEY` env var)
- CFA-Easy or CFA-Challenge dataset in `datasets/FinEval/`
