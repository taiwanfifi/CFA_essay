# Paper A Experiments: Stress Testing, Error Taxonomy, and Calibration

Experiments supporting **"The Illusion of Financial Competence"** (Paper A, targeting IRFA).

## Experiment Modules

| Module | Purpose | Dataset | N |
|--------|---------|---------|---|
| `I1_counterfactual` | Counterfactual perturbation stress test | CFA-Easy | 1,032 |
| `I3_noise_red_herrings` | Noise injection (N1-N4) | CFA-Easy | 1,032 |
| `E1_error_analysis` | Error taxonomy + GCI | CFA-Easy | 557 errors |
| `D1_confidence_calibration` | Confidence calibration + CaR | CFA-Challenge + CFA-Easy | 90 + 1,032 |

## Quick Start

```bash
# Install dependencies
pip install openai python-dotenv tqdm requests pydantic

# Set API key
echo "OPENAI_API_KEY=your-key" > .env

# Run stress testing (counterfactual perturbation)
python -m experiments.I1_counterfactual.run_experiment --dataset easy --model gpt-4o-mini

# Run noise injection (all 4 types)
python -m experiments.I3_noise_red_herrings.run_experiment --dataset easy --model gpt-4o-mini --noise-types N1 N2 N3 N4

# Run error analysis (open-ended evaluation)
python -m experiments.A1_open_ended.run_experiment --dataset easy --model gpt-4o-mini

# Run confidence calibration
python -m experiments.D1_confidence_calibration.run_experiment --dataset challenge --model gpt-4o-mini
python -m experiments.D1_confidence_calibration.run_experiment --dataset easy --model gpt-4o-mini
```

## Key Results Files

| Result | Path |
|--------|------|
| I1 GPT-4o-mini (N=1,032) | `experiments/I1_counterfactual/results/run_20260206_174011/` |
| I1 GPT-5-mini (N=1,032) | `experiments/I1_counterfactual/results/run_20260207_174124/` |
| I3 Full noise (N=1,032) | `experiments/I3_noise_red_herrings/results/run_20260207_060254/` |
| E1 Error analysis | `experiments/E1_error_analysis/results/run_20260206_180049/` |
| E1 GCI GPT-5-mini | `experiments/E1_error_analysis/results/golden_context_gpt-5-mini_20260207_220440.json` |
| D1 CFA-Challenge | `experiments/D1_confidence_calibration/results/run_20260206_193455/` |
| D1 CFA-Easy (N=1,032) | `experiments/D1_confidence_calibration/results/run_20260210_152709/` |

## Metrics

- **Memorization Gap** = Standard Accuracy - Perturbed Accuracy
- **Robust Accuracy** = correct on original AND all valid perturbations
- **NSI** = (Clean Acc - Noisy Acc) / Clean Acc
- **ECE** = Expected Calibration Error
- **CaR(alpha)** = minimum confidence threshold achieving error rate <= alpha
- **Overconfident Error Rate** = P(incorrect AND confidence >= 0.80)
