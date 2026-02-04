# I3: Noise & Red Herrings — Robustness to Irrelevant Information

## Research Question

How robust are LLMs to irrelevant information injected into CFA exam questions? We measure the **Noise Sensitivity Index (NSI)** — the proportion of performance lost when noise is added.

---

## Noise Types

| Code | Name | What it does |
|------|------|-------------|
| N1 | Irrelevant Data | Splice unrelated facts into the question body |
| N2 | Plausible Distractor | Add financially-related but irrelevant details |
| N3 | Verbose Padding | Wordy preamble that adds no information |
| N4 | Contradictory Hint | Insert a misleading "hint" pointing to wrong answer |

---

## Worked Example — N1 (Irrelevant Data Injection)

### Original Question

```
Q: At a 5% interest rate per year compounded annually, the PV of a 10-year
ordinary annuity with annual payments of $2,000 is $15,443.47. The PV of a
10-year annuity due is closest to:
CHOICES: A: $14,709.02. B: $16,215.64. C: $17,443.47.
```

### N1 Version (intensity=2)

```
Q: At a 5% interest rate per year compounded annually, the PV of a 10-year
ordinary annuity with annual payments of $2,000 is $15,443.47. The issuing
company has 12,500 employees and was founded in 1987. Its current ESG rating
is BBB+ from MSCI. The PV of a 10-year annuity due is closest to:
CHOICES: A: $14,709.02. B: $16,215.64. C: $17,443.47.
```

The injected sentences (employees, ESG rating) are completely irrelevant to calculating PV of an annuity due. A robust model should ignore them entirely.

### N4 Version (Contradictory Hint)

```
Q: [original question]

Hint: Many students incorrectly choose A here, but think carefully.
```

The hint falsely implies A is a trap answer, potentially steering the model away from A even if A is correct.

---

## Core Metric

**Noise Sensitivity Index (NSI)**:

```
NSI = (accuracy_clean - accuracy_noisy) / accuracy_clean
```

| NSI Value | Interpretation |
|-----------|---------------|
| 0.00 | Perfectly robust |
| 0.01–0.05 | Mildly sensitive |
| 0.05–0.15 | Moderately sensitive |
| > 0.15 | Highly sensitive |

---

## Running

```bash
# POC: 5 questions, single noise type
python -m experiments.I3_noise_red_herrings.run_experiment \
    --dataset easy --limit 5 --model gpt-4o-mini --noise-types N1

# All noise types
python -m experiments.I3_noise_red_herrings.run_experiment \
    --dataset easy --limit 5 --model gpt-4o-mini --noise-types N1 N2 N3 N4

# Dose-response: vary intensity
python -m experiments.I3_noise_red_herrings.run_experiment \
    --dataset easy --limit 20 --model gpt-4o-mini --noise-types N1 --intensity 1
python -m experiments.I3_noise_red_herrings.run_experiment \
    --dataset easy --limit 20 --model gpt-4o-mini --noise-types N1 --intensity 4

# Analysis
python -m experiments.I3_noise_red_herrings.analysis \
    --input experiments/I3_noise_red_herrings/results/run_*/results.json
```

---

## Output Format

```json
{
  "metadata": {
    "experiment": "I3_noise_red_herrings",
    "model": "gpt-4o-mini",
    "noise_types": ["N1"],
    "intensity": 2
  },
  "summary": {
    "accuracy_clean": 0.8,
    "noise_results": {
      "N1": {
        "noise_type_name": "irrelevant_data",
        "accuracy": 0.6,
        "n_flipped": 1,
        "nsi": 0.25
      }
    }
  },
  "results": [
    {
      "question_id": "easy_0",
      "clean_answer": "C",
      "clean_correct": true,
      "noisy_results": {
        "N1": {"answer": "A", "correct": false, "flipped": true}
      }
    }
  ]
}
```

---

## Dependencies

- `experiments/shared/` (config, llm_client, prompts, data_loader)
- OpenAI API key (`OPENAI_API_KEY` env var)
