# LLM Financial Reasoning: A Three-Paper Research Program

Systematic evaluation of Large Language Model financial reasoning competence using CFA examination questions. Three merged papers targeting top finance journals.

## Papers

| Paper | Title | Target Journal | Status |
|-------|-------|---------------|--------|
| **A** | The Illusion of Financial Competence: Stress Testing, Error Taxonomy, and Calibration Analysis | IRFA (IF 9.8) | Complete |
| **B** | When Machines Pass the Test: Professional Certification Signaling Erosion Under AI Disruption | FAJ (CFA Institute) | Complete |
| **C** | Inherited Irrationality and Ethical Fragility: Behavioral Biases and Adversarial Vulnerability | FRL (IF 6.9) | Complete |

### Paper A — The Risk Paper (P2 + P5 + P6)
Three-dimensional assessment revealing that LLM headline accuracy is largely illusory:
- **Stress Testing**: 18.6 pp memorization gap; GPT-5-mini paradoxically worse (36.4 pp)
- **Error Taxonomy**: 90.1% reasoning errors (68.8% conceptual); only 1.4% calculation errors
- **Calibration**: ECE = 0.315; CaR(5%) undefined; 30% high-confidence errors

### Paper B — The Theory Paper (P7 + P1)
Modified Spence Signaling Model analyzing AI's impact on CFA certification value:
- **Signaling Retention Ratio**: R = 28.8% (>70% of signaling value already eroded)
- **Option Bias**: GPT-4o-mini +1.9 pp (n.s.); GPT-5-mini +9.6 pp (p<0.001)
- **Policy**: Content reform (not format reform) is the solution

### Paper C — The Behavioral Paper (P3 + P4)
Dual threat of inherited irrationality and ethical fragility:
- **Bias Hierarchy**: Surface (debiasable) > Weakly responsive > Deep (resistant)
- **Adversarial Ethics**: All 5 attack types degrade accuracy; 14 flips with rationalization
- **Cross-Model**: GPT-5-mini achieves zero adversarial flips

## Directory Structure

```
edition_260211/
├── README.md                          # This file
├── paper_A_risk/                      # Paper A: Stress Test + Errors + Calibration
│   ├── main.tex                       # LaTeX source
│   ├── main.pdf                       # Compiled PDF
│   ├── 白話說明.md                     # Plain-language explainer (Traditional Chinese)
│   └── figures/                       # All figures
├── paper_B_signaling/                 # Paper B: Signaling Theory + Option Bias
│   ├── main.tex
│   ├── main.pdf
│   ├── 白話說明.md
│   └── figures/
├── paper_C_behavioral/                # Paper C: Behavioral Biases + Ethics
│   ├── main.tex
│   ├── main.pdf
│   ├── 白話說明.md
│   └── figures/
└── experiments/                       # Experiment documentation
    ├── paper_A_risk_experiments/      # Paper A experiment guide
    │   └── README.md
    └── paper_C_behavioral_experiments/ # Paper C experiment guide
        └── README.md
```

## Data Sources

| Dataset | N | Source | Usage |
|---------|---|--------|-------|
| CFA-Easy | 1,032 | FinEval (HuggingFace) | Papers A, B |
| CFA-Challenge | 90 | FinEval (HuggingFace) | Paper A (calibration) |
| Custom Scenarios | 60 + 80 | Generated | Paper C (biases) |
| CFA Ethics Subset | 47 + 141 | FinEval + Generated | Paper C (ethics) |

## Models Evaluated

| Model | Provider | Usage |
|-------|----------|-------|
| GPT-4o-mini | OpenAI | Primary model (all papers) |
| GPT-5-mini | OpenAI | Cross-model validation |
| Qwen3-32B | Alibaba | Calibration comparison (Paper A) |

## Reproducing Results

All experiments use the same CLI pattern from the repository root:

```bash
# Prerequisites
pip install openai anthropic python-dotenv tqdm requests pydantic
echo "OPENAI_API_KEY=your-key" > .env

# Paper A experiments
python -m experiments.I1_counterfactual.run_experiment --dataset easy --model gpt-4o-mini
python -m experiments.I3_noise_red_herrings.run_experiment --dataset easy --model gpt-4o-mini --noise-types N1 N2 N3 N4
python -m experiments.D1_confidence_calibration.run_experiment --dataset challenge --model gpt-4o-mini

# Paper B experiments
python -m experiments.A5_option_bias.run_experiment --dataset easy --model gpt-4o-mini
python -m experiments.A1_open_ended.run_experiment --dataset easy --model gpt-4o-mini

# Paper C experiments
python -m experiments.I2_behavioral_biases.run_experiment --bias-types loss_aversion anchoring framing recency disposition_effect overconfidence --model gpt-4o-mini
python -m experiments.D6_adversarial_ethics.run_experiment --dataset easy --model gpt-4o-mini
```

## Building Papers

```bash
# Compile any paper (double-pass for references)
cd paper_A_risk && /Library/TeX/texbin/pdflatex -interaction=nonstopmode main.tex && /Library/TeX/texbin/pdflatex -interaction=nonstopmode main.tex

# Word count
/Library/TeX/texbin/detex main.tex | wc -w
```

## Citation

```bibtex
@article{cheng2026illusion,
  title={The Illusion of Financial Competence: Stress Testing, Error Taxonomy, and Calibration Analysis of Large Language Models on CFA Examinations},
  author={Cheng, Wei-Lun and Miao, Daniel Wei-Chung and Chang, Guang-Di},
  journal={International Review of Financial Analysis},
  year={2026}
}

@article{cheng2026signaling,
  title={When Machines Pass the Test: Professional Certification Signaling Erosion Under AI Disruption},
  author={Cheng, Wei-Lun and Miao, Daniel Wei-Chung and Chang, Guang-Di},
  journal={Financial Analysts Journal},
  year={2026}
}

@article{cheng2026irrationality,
  title={Inherited Irrationality and Ethical Fragility: Behavioral Biases and Adversarial Vulnerability of Large Language Models in Financial Decision-Making},
  author={Cheng, Wei-Lun and Miao, Daniel Wei-Chung and Chang, Guang-Di},
  journal={Finance Research Letters},
  year={2026}
}
```

## Acknowledgments

Built on [FinDAP](https://github.com/SalesforceAIResearch/FinDAP) (EMNLP 2025 Oral, Salesforce AI Research).
