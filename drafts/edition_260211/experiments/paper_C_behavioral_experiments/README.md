# Paper C Experiments: Behavioral Biases and Adversarial Ethics

Experiments supporting **"Inherited Irrationality and Ethical Fragility"** (Paper C, targeting FRL).

## Experiment Modules

| Module | Purpose | Dataset | N |
|--------|---------|---------|---|
| `I2_behavioral_biases` | Paired-scenario bias measurement | Custom scenarios | 60 + 80 synthetic |
| `D6_adversarial_ethics` | Adversarial pressure testing | CFA-Easy (Ethics) | 47 + 141 synthetic |

## Quick Start

```bash
# Install dependencies
pip install openai python-dotenv tqdm requests pydantic

# Set API key
echo "OPENAI_API_KEY=your-key" > .env

# Run behavioral bias experiment (all 6 bias types)
python -m experiments.I2_behavioral_biases.run_experiment \
    --bias-types loss_aversion anchoring framing recency disposition_effect overconfidence \
    --model gpt-4o-mini

# Run adversarial ethics experiment
python -m experiments.D6_adversarial_ethics.run_experiment \
    --dataset easy \
    --model gpt-4o-mini

# Run synthetic scenarios (extended replication)
python -m experiments.I2_behavioral_biases.run_experiment \
    --synthetic --model gpt-4o-mini

python -m experiments.D6_adversarial_ethics.run_experiment \
    --synthetic --model gpt-4o-mini
```

## Key Results Files

| Result | Path |
|--------|------|
| I2 Primary (N=60) | `experiments/I2_behavioral_biases/results/run_20260206_140527/results.json` |
| I2 Synthetic (N=80) | `experiments/I2_behavioral_biases/results/synthetic_gpt-4o-mini_20260210_085431/` |
| D6 Primary (N=47) | `experiments/D6_adversarial_ethics/results/run_20260206_190419/results.json` |
| D6 Synthetic (N=141) | `experiments/D6_adversarial_ethics/results/synthetic_gpt-4o-mini_20260210_091207/` |
| D6 GPT-5-mini | `experiments/D6_adversarial_ethics/results/run_20260207_213723/results.json` |

## Metrics

### Behavioral Biases
- **Bias Score**: 0.0 (rational) / 0.5 (mixed) / 1.0 (fully biased)
- **Debiasing Effect** = Bias-Inducing Score - Neutral Score
- **Three-Tier Hierarchy**: Surface (prompt-debiasable) > Weakly responsive > Deep (resistant)

### Adversarial Ethics
- **ERS** (Ethics Robustness Score) = Adversarial Accuracy / Standard Accuracy
- **Flip Count** = questions correct under standard but incorrect under adversarial
- **Rationalization Taxonomy**: Utilitarian override / Authority deference / Semantic repackaging
