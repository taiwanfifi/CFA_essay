# GPT-5-mini Experiment Progress Tracker

**Last updated**: 2026-02-07 17:41 (auto-updated during runs)

## Completed GPT-5-mini Results
| Experiment | Status | File | Key Metric |
|-----------|--------|------|------------|
| D6 (Adversarial Ethics) | DONE | `experiments/D6_adversarial_ethics/results/run_20260207_023637/results.json` | std_acc=91.5%, ZERO flips |
| I2 (Behavioral Biases) | DONE | `experiments/I2_behavioral_biases/results/run_20260207_024534/results.json` | avg_bias=0.892 |
| E1 GCI (POC N=5) | DONE | `experiments/E1_error_analysis/results/golden_context_gpt-5-mini_20260207_041248.json` | recovery=60% (POC) |

## Currently Running (Session 6)
| Experiment | Run Dir | Checkpoint | Started |
|-----------|---------|------------|---------|
| A5 (Option Bias) | `experiments/A5_option_bias/results/run_20260207_174114` | checkpoint.jsonl | 17:41 |
| I3 (Noise N1-N4) | `experiments/I3_noise_red_herrings/results/run_20260207_174115` | checkpoint.jsonl | 17:41 |
| I1 (Counterfactual) | `experiments/I1_counterfactual/results/run_20260207_174116` | checkpoint.jsonl | 17:41 |
| A1 (Open-Ended) | `experiments/A1_open_ended/results/run_20260207_174118` | checkpoint.jsonl | 17:41 |
| E1 GCI (Full N=557) | `experiments/E1_error_analysis/results/` | `checkpoint_gpt-5-mini_20260207_174124.jsonl` | 17:41 |

## Resume Commands (if interrupted)
```bash
# Resume A5
python -m experiments.A5_option_bias.run_experiment --model gpt-5-mini --dataset easy \
  --resume experiments/A5_option_bias/results/run_20260207_174114

# Resume I3
python -m experiments.I3_noise_red_herrings.run_experiment --model gpt-5-mini --dataset easy \
  --noise-types N1 N2 N3 N4 \
  --resume experiments/I3_noise_red_herrings/results/run_20260207_174115

# Resume I1
python -m experiments.I1_counterfactual.run_experiment --model gpt-5-mini --dataset easy \
  --perturbation-levels 1 \
  --resume experiments/I1_counterfactual/results/run_20260207_174116

# Resume A1
python -m experiments.A1_open_ended.run_experiment --model gpt-5-mini --dataset easy \
  --resume experiments/A1_open_ended/results/run_20260207_174118

# Resume E1 GCI
python -m experiments.E1_error_analysis.golden_context \
  --a1-results experiments/A1_open_ended/results/run_20260206_173445/results.json \
  --model gpt-5-mini \
  --resume experiments/E1_error_analysis/results/checkpoint_gpt-5-mini_20260207_174124.jsonl
```

## GPT-4o-mini Baseline Results (for comparison)
| Experiment | Key Metrics |
|-----------|------------|
| A5 | with=82.6%, without=80.6%, McNemar p=0.251 |
| A1 | Level A=24.5%, B=21.5%, C=54.0% |
| I1 | orig=82.4%, L1=63.8%, robust=63.5%, mem_gap=18.6pp |
| I3 | clean=81.6%, N1=79.0%, N2=80.3%, N3=82.0%, N4=87.5% |
| E1 GCI | recovery=82.4% (N=557) |
| D6 | std_acc=83.0%, ERS varies by technique |
| I2 | avg_bias=0.867, debiasing=0.033 |

## Paper Mapping
- **P1 (A1+A5)**: Needs A1 + A5 GPT-5-mini
- **P2 (I1+I3)**: Needs I1 + I3 GPT-5-mini
- **P3 (I2)**: DONE (has GPT-5-mini)
- **P4 (D6)**: DONE (has GPT-5-mini)
- **P5 (E1)**: Needs E1 GCI GPT-5-mini full-scale
- **P6 (D1+D4)**: No new experiment needed (calibration uses same data)
- **P7 (G2)**: Needs A5 GPT-5-mini (for signaling theory)
