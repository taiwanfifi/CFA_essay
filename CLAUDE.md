# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research repository producing **7 papers** (all targeting Finance Research Letters) that systematically evaluate LLM financial reasoning using CFA exam questions. Built on **FinDAP** (Demystifying Domain-adaptive Post-training for Financial LLMs), EMNLP 2025 Oral by Salesforce AI Research. Research docs are in Traditional Chinese; technical terms remain in English so keyword search works normally.

### Paper → Experiment Mapping

| Paper | Experiment Modules | Dataset | N |
|-------|-------------------|---------|---|
| P1 (Option Bias) | `A1_open_ended` + `A5_option_bias` | CFA-Easy | 1,032 |
| P2 (Stress Test) | `I1_counterfactual` + `I3_noise_red_herrings` | CFA-Easy | 1,032 |
| P3 (Behavioral Biases) | `I2_behavioral_biases` | Custom scenarios | 60 |
| P4 (Adversarial Ethics) | `D6_adversarial_ethics` | CFA-Easy (ethics) | 47 |
| P5 (Error Atlas) | `E1_error_analysis` + A1 results | CFA-Easy | 557 errors |
| P6 (Calibration) | `D1_confidence_calibration` + `D4_overconfident_risk` | CFA-Challenge | 90 |
| P7 (Signaling Theory) | Theoretical; cites A5 data | CFA-Easy | 1,032 |

## Key Directories

- `experiments/` — Active experiment modules, each self-contained with `run_experiment.py` CLI
- `experiments/shared/` — Shared infrastructure: `llm_client.py`, `config.py` (model registry), `prompts.py` (answer extraction), `evaluation.py` (metrics), `data_loader.py`
- `drafts/selected/` — 7 paper directories (LaTeX + figures + PDF), 7 Chinese summary `.md` files, presentations/
- `drafts/ideas/` — 42 research idea files by category prefix: A (Evaluation), B (Reasoning), C (RAG), D (Confidence), E (Error Analysis), F (Scaling), G (Assessment Theory), H (Cross-boundary), I (Adversarial)
- `docs/` — 5 numbered research documents (01–05). Reading order: 01 → 02 → 03 → 04 → 05
- `datasets/FinEval/` — Evaluation datasets: CFA-Challenge (90 hard), CFA-Easy (1,032), CRA-Bigdata (1,472)
- `datasets/FinDap/FinDAP/` — FinDAP training framework (Salesforce repo, excluded from git tracking)

## Common Commands

### Running Experiments (Primary workflow)
```bash
# Setup
conda create -n cfa-llm python=3.10 && conda activate cfa-llm
pip install openai anthropic google-generativeai python-dotenv tqdm requests pydantic
echo "OPENAI_API_KEY=your-key" > .env

# All experiments use same CLI pattern
python -m experiments.A5_option_bias.run_experiment --dataset easy --limit 5 --model gpt-4o-mini
python -m experiments.A1_open_ended.run_experiment --dataset easy --limit 5 --model gpt-4o-mini
python -m experiments.I1_counterfactual.run_experiment --dataset easy --limit 5 --model gpt-4o-mini
python -m experiments.I2_behavioral_biases.run_experiment --bias-types loss_aversion anchoring --limit 5 --model gpt-4o-mini
python -m experiments.I3_noise_red_herrings.run_experiment --dataset easy --limit 5 --model gpt-4o-mini --noise-types N1 N2 N3 N4
python -m experiments.D4_overconfident_risk.run_experiment --input "experiments/D1_confidence_calibration/results/run_*/results.json" --confidence-threshold 0.8 --limit 5
```

Results saved to `experiments/XX/results/run_YYYYMMDD_HHMMSS/results.json`.

### Building Papers (LaTeX)
```bash
# Compile any paper (double-pass for references)
cd drafts/selected/A1_open_ended
/Library/TeX/texbin/pdflatex -interaction=nonstopmode main.tex && /Library/TeX/texbin/pdflatex -interaction=nonstopmode main.tex

# Word count via detex
/Library/TeX/texbin/detex main.tex | wc -w
```

### Figure Generation
```bash
python drafts/selected/generate_all_figures.py           # Main figures for all papers
python drafts/selected/generate_cross_model_figures.py   # Cross-model comparison figures
```

### Training (3-stage pipeline via Accelerate + FSDP)
```bash
./datasets/FinDap/FinDAP/scripts/cpt_sft/mix_cpt_mix_sft_extend_book_exercise_downsample_from_base.sh  # Stage 1
./datasets/FinDap/FinDAP/scripts/cpt_sft/mix_cpt_mix_sft_extend_book_exercise_downsample_from_v1.sh    # Stage 2
./datasets/FinDap/FinDAP/scripts/offline_rl/rpo_cfa_stepwise.sh                                         # Stage 3
```

GPU configs in `datasets/FinDap/FinDAP/yaml/` (2, 4, 8, 16 GPUs). Training scripts run inline `pip install/uninstall`—review before running.

## Architecture

### Experiments Framework (`experiments/`)

Each module is self-contained:
```
experiments/XX_name/
├── __init__.py
├── config.py           # Experiment-specific constants, prompts
├── run_experiment.py   # Main CLI (argparse)
├── analysis.py         # Post-processing
└── results/            # JSON output
```

### Shared Infrastructure (`experiments/shared/`)

- `config.py` — `MODEL_REGISTRY` with 20 models across 5 backends (OpenAI, Anthropic, Gemini, DeepSeek, Ollama). `DEFAULT_MODEL = "gpt-4o-mini"`, `DEFAULT_JUDGE_MODEL = "gpt-4o-mini"`
- `llm_client.py` — `LLMClient` class: unified API across all backends. Reasoning models (gpt-5-*, o1, o3) require `max_completion_tokens` (not `max_tokens`), minimum 16384 tokens, temperature omitted. Retry: 3 attempts with 10/30/60s backoff
- `prompts.py` — `extract_answer()`: 5-layer regex answer extraction from LLM responses
- `evaluation.py` — `tolerance_match()` (numerical), `semantic_match_judge()` (LLM-as-judge), `mcnemar_test()` (with Yates' correction)
- `data_loader.py` — Unified dataset loading for CFA-Easy, CFA-Challenge, CRA-Bigdata

### FinDAP Training Framework (`datasets/FinDap/FinDAP/`)

**Entry point:** `posttrain.py` routes via `--idrandom` flag:
- `"dapt_mix_sft_mix_full_extend_exercise_book"` → `Posttrain.sft_trainer()` (Stages 1 & 2)
- `"dpo_cfa_sample_from_policy_stepwise"` → `Posttrain.dpo_trainer()` (Stage 3, triggered by `"dpo"` substring)

**Key modules:** `config.py` (~100 argparse flags), `approaches/posttrain.py` (trainer methods), `utils/prepare.py` (PosttrainPreparer), `dataloader/data.py` (HuggingFace datasets under `ZixuanKe/` namespace, requires `HF_TOKEN`)

## Model-Specific Gotchas

- **GPT-5-mini**: Omit `temperature` parameter. Use `max_completion_tokens` (not `max_tokens`), minimum 16384. Reasoning tokens can exhaust budget on complex scenarios—set 32768+ for I2-style tasks
- **Ollama models**: Only backend supporting logprobs (via native `/api/chat` endpoint)
- **LLM-as-judge**: `semantic_match_judge()` accepts optional `judge_model` parameter. Empty LLM responses get scored ~55% correct by judge—always check for empty responses in results

## Data Integrity Notes

- **GPT-5-mini I2 data removed**: 80% empty responses produced artifact bias scores (0.892). Only GPT-4o-mini I2 results are reliable
- **A5 GPT-5-mini corrected**: 58 empty without-options responses were incorrectly judged correct. Corrected accuracy: 83.2% (not 86.3%), option bias: +9.6pp (not +6.5pp)
- No datasets contain official CFA Institute exam questions (all sourced from SchweserNotes)
- `flare-cfa` ≈ `FinEval-CFA-Easy` (near-duplicate); flare-cfa archived

## Git Notes

- `.gitignore` excludes: `datasets/FinDap/` (nested repo), large data files, LaTeX artifacts, titled PDF copies (only `main.pdf` tracked), exploratory experiments (B1, C1), personal files
- Experiment results: only final full runs tracked (test/pilot runs excluded)
- Environment variables in `.env` (not tracked): `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `DEEPSEEK_API_KEY`
