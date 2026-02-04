# I2: Behavioral Biases — Do LLMs Exhibit Financial Biases?

## Research Question

CFA Level III tests candidates' understanding of behavioral finance. Do LLMs themselves exhibit these biases when making financial recommendations? We test 6 bias types using paired scenarios (bias-inducing vs neutral framing).

---

## Bias Types Tested

| Bias | Description | Tested Via |
|------|-------------|-----------|
| Loss Aversion | Prefer avoiding losses over equivalent gains | Gain/loss framing of same EV gamble |
| Anchoring | Over-reliance on initial information | Prior prices/targets before fundamental changes |
| Framing Effect | Different response to same info, different framing | Gain vs loss frame of identical outcomes |
| Recency Bias | Overweighting recent events | Recent performance vs long-run fundamentals |
| Disposition Effect | Selling winners, holding losers | Portfolio with gains and losses to liquidate |
| Overconfidence | Excessive confidence in predictions | Prediction interval calibration |

---

## Paired Scenario Design

Each scenario has two versions:

### Example: Loss Aversion (la_01)

**Bias-inducing version:**
```
Investment A: 80% chance of gaining $10,000 and 20% chance of LOSING $2,000
             (EV = $7,600)
Investment B: Guaranteed return of $7,000 (EV = $7,000)

Which investment do you recommend?
```

**Neutral version:**
```
Investment A: Expected Value = $7,600 (with variance)
Investment B: Expected Value = $7,000 (guaranteed)

Which has higher expected value?
```

**Rational baseline:** Investment A (EV $7,600 > $7,000)
**Biased answer:** Investment B (avoiding the stated loss)

### Bias Score

| Score | Interpretation |
|-------|---------------|
| 0.0 | Fully rational — recommends the EV-optimal choice |
| 0.5 | Mixed / hedged recommendation |
| 1.0 | Fully biased — recommends the bias-predicted choice |

### Debiasing Effect

```
Debiasing Effect = bias_score (inducing) - bias_score (neutral)
```

Positive value = neutral framing successfully reduces bias.

---

## Scenario Library

The experiment includes 20 scenarios across 6 bias types:
- Loss Aversion: 5 scenarios
- Anchoring: 5 scenarios
- Framing Effect: 5 scenarios
- Recency Bias: 3 scenarios
- Disposition Effect: 2 scenarios

All scenarios feature realistic CFA-level financial decisions.

---

## Running

```bash
# POC: 2 bias types, up to 5 scenarios each
python -m experiments.I2_behavioral_biases.run_experiment \
    --bias-types loss_aversion anchoring --limit 5 --model gpt-4o-mini

# All bias types
python -m experiments.I2_behavioral_biases.run_experiment --model gpt-4o-mini

# Single bias type (all scenarios)
python -m experiments.I2_behavioral_biases.run_experiment \
    --bias-types framing --model gpt-4o-mini

# Analysis
python -m experiments.I2_behavioral_biases.analysis \
    --input experiments/I2_behavioral_biases/results/run_*/results.json
```

---

## Output Format

```json
{
  "metadata": {
    "model": "gpt-4o-mini",
    "bias_types": ["loss_aversion", "anchoring"],
    "n_scenarios": 10
  },
  "summary": {
    "avg_bias_score": 0.45,
    "avg_neutral_score": 0.15,
    "avg_debiasing_effect": 0.30,
    "by_bias_type": {
      "loss_aversion": {
        "avg_bias_score": 0.62,
        "avg_neutral_score": 0.10,
        "avg_debiasing_effect": 0.52
      }
    }
  },
  "results": [
    {
      "scenario_id": "la_01",
      "bias_type": "loss_aversion",
      "bias_version_score": 0.8,
      "neutral_version_score": 0.1,
      "debiasing_effect": 0.7
    }
  ]
}
```

---

## Dependencies

- `experiments/shared/` (config, llm_client)
- OpenAI API key (`OPENAI_API_KEY` env var)
- No external datasets needed (scenarios are self-contained)
