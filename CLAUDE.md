# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Financial LLM research repository built on **FinDAP** (Demystifying Domain-adaptive Post-training for Financial LLMs), EMNLP 2025 Oral by Salesforce AI Research. Adapts Llama-3-8B to the financial domain via a 3-stage training pipeline (CPT+SFT → curriculum → RPO alignment). Research docs are in Traditional Chinese; technical terms remain in English so keyword search works normally.

## Key Directories

- `docs/` — 5 numbered research documents (01–05). Start with `03-研究方向深度設計.md` for the core blueprint (7 research directions, paper split strategy). Reading order: 01 → 02 → 03 → 04 → 05.
- `drafts/ideas/` — 42 research idea files, named by category prefix: A (Evaluation), B (Reasoning), C (RAG), D (Confidence), E (Error Analysis), F (Scaling), G (Assessment Theory), H (Cross-boundary), I (Adversarial). Suffixes like `A1a-`, `B2b-` denote sub-ideas. Each file is a self-contained research proposal.
- `drafts/selected/` — 11 curated research proposals ready for implementation
- `datasets/FinDap/FinDAP/` — The FinDAP training framework (Salesforce repo). This is the main codebase.
- `datasets/FinEval/` — Evaluation datasets: CFA-Challenge (90 hard), CFA-Easy (1,032), CRA-Bigdata (1,472)
- `datasets/FinTrain/` — Training datasets: apex_instruct (1.4M), book_fineweb (4,500 CPT), cfa_exercise (2,946)
- `experiments/` — Active experiment modules, each self-contained with `run_experiment.py` CLI. Key modules: A1 (open-ended), A5 (option bias), B1 (multi-step agent), C1 (RAG), D1 (calibration), D4 (overconfidence risk), E1 (error analysis), I1 (counterfactual), I2 (behavioral biases), I3 (noise sensitivity)
- `experiments/shared/` — Shared infrastructure: `llm_client.py` (OpenAI/Ollama), `config.py` (model registry), `prompts.py` (answer extraction), `evaluation.py` (metrics), `data_loader.py`
- `scripts/` — Dataset download/analysis Python scripts
- `reference/` — Generated analysis artifacts (JSON, markdown comparison tables)
- `models/` — Model metadata JSON only (no weights)
- `archive/` — Backup of pre-restructuring docs; not actively used

## Environment Setup

```bash
conda create -n FinDAP python=3.10 && conda activate FinDAP
cd datasets/FinDap/FinDAP
pip install -r requirements.txt
```

Key dependencies: PyTorch 2.2.2, Transformers 4.40.0, TRL 0.12.0, PEFT, DeepSpeed, Accelerate, flash-attn.

Required environment variables:
```bash
export ROOT_DIR=/path/to/parent       # See path alias note below
export HF_TOKEN=your_token            # Required for ZixuanKe/ namespace datasets
export HF_DATASETS_CACHE=${ROOT_DIR}/dataset_cache
export TRANSFORMERS_CACHE=${ROOT_DIR}/model_cache
```

**Path alias gotcha:** Training scripts reference the framework as `${ROOT_DIR}/SFR-Continual-Pretrain/` (the original Salesforce repo name). Either set `ROOT_DIR` so that path resolves to `datasets/FinDap/FinDAP/`, or create a symlink: `ln -s /path/to/datasets/FinDap/FinDAP ${ROOT_DIR}/SFR-Continual-Pretrain`.

## Common Commands

### Dataset Download & Analysis
```bash
python scripts/download_and_analyze.py        # Download and analyze all datasets
python scripts/analyze_comparison.py          # Generate comparative analysis
python scripts/download_and_verify_all.py     # Download with verification
```

### Running Experiments (Primary workflow)
```bash
# Setup
conda create -n cfa-llm python=3.10 && conda activate cfa-llm
pip install openai python-dotenv tqdm requests pydantic
echo "OPENAI_API_KEY=your-key" > .env

# Run individual experiments (all use same CLI pattern)
python -m experiments.A5_option_bias.run_experiment --dataset easy --limit 5 --model gpt-4o-mini
python -m experiments.A1_open_ended.run_experiment --dataset easy --limit 5 --model gpt-4o-mini
python -m experiments.I1_counterfactual.run_experiment --dataset easy --limit 5 --model gpt-4o-mini
python -m experiments.I2_behavioral_biases.run_experiment --bias-types loss_aversion anchoring --limit 5 --model gpt-4o-mini
python -m experiments.I3_noise_red_herrings.run_experiment --dataset easy --limit 5 --model gpt-4o-mini --noise-types N1 N2 N3 N4
python -m experiments.D4_overconfident_risk.run_experiment --input "experiments/D1_confidence_calibration/results/run_*/results.json" --confidence-threshold 0.8 --limit 5
```

Results are saved to `experiments/XX/results/run_YYYYMMDD_HHMMSS/results.json`.

### Training (3-stage pipeline via Accelerate + FSDP)
```bash
# Stage 1: Joint CPT + SFT (from base Llama-3-8B-Instruct)
./datasets/FinDap/FinDAP/scripts/cpt_sft/mix_cpt_mix_sft_extend_book_exercise_downsample_from_base.sh

# Stage 2: Advanced curriculum (from Stage 1 checkpoint)
./datasets/FinDap/FinDAP/scripts/cpt_sft/mix_cpt_mix_sft_extend_book_exercise_downsample_from_v1.sh

# Stage 3: Offline RL with RPO preference alignment
./datasets/FinDap/FinDAP/scripts/offline_rl/rpo_cfa_stepwise.sh
```

**GPU configuration:** Scripts default to `fsdp_config_16.yaml` (16 GPUs). To run on fewer GPUs, change `--config_file` in the shell script to the corresponding yaml in `datasets/FinDap/FinDAP/yaml/` (configs exist for 2, 4, 8, 16 GPUs).

**Script side effects:** The training shell scripts run `pip install`, `pip uninstall`, and `pip cache purge` inline before launching training. Review and comment out these lines if you want to preserve your environment.

### Evaluation (via lm-evaluation-harness)
```bash
lm_eval --apply_chat_template --model vllm \
  --model_args pretrained=Salesforce/Llama-Fin-8b,max_length=8000,dtype=bfloat16 \
  --tasks cfa-challenge --device cuda
```

## Architecture

### FinDAP Training Framework (`datasets/FinDap/FinDAP/`)

**Entry point:** `posttrain.py` routes to one of three code paths:
1. `--convert_checkpoint_to_ckpt` → checkpoint format conversion (no training)
2. `--use_trainer` + `"dpo"` in `--idrandom` → `Posttrain.dpo_trainer()` (DPO/RPO)
3. `--use_trainer` + other `--idrandom` → `Posttrain.sft_trainer()` (SFT)

**Flow:** `posttrain.py` → `config.parsing_posttrain()` → `PosttrainPreparer` (loads model/tokenizer, prepares datasets) → `Posttrain.sft_trainer()` or `Posttrain.dpo_trainer()`. Uses Accelerate + FSDP for distributed multi-GPU training.

**Key modules:**
- `config.py` — ~100 argparse flags for all training configurations
- `approaches/posttrain.py` — `Posttrain` class with `sft_trainer()` and `dpo_trainer()` methods
- `utils/prepare.py` — `PosttrainPreparer` class: model/tokenizer loading, dataset preparation, training arg setup
- `utils/model.py` — Checkpoint conversion utilities
- `dataloader/data.py` — All datasets fetched from HuggingFace Hub (`ZixuanKe/posttrain_tokenized_{name}_qwen2.5-32b-instruct`), not loaded locally
- `utils/packing/` — Sequence packing via monkey-patching (`monkey_patch_packing.py`, `packed_dataset.py`, `assert_packing_loss.py`)

### The `--idrandom` Flag

This is the most important training flag despite its opaque name. It controls **both** the training mode routing and dataset selection:
- `"dapt_mix_sft_mix_full_extend_exercise_book"` — Stages 1 & 2: joint CPT + SFT training
- `"dpo_cfa_sample_from_policy_stepwise"` — Stage 3: RPO preference alignment (triggers DPO trainer path because it contains `"dpo"`)

The string is checked for substring `"dpo"` in `posttrain.py:52` to select the trainer. It is also parsed by `PosttrainPreparer` to determine which datasets to load.

### Other Key Training Flags
- `--use_trainer` — Required; enables HuggingFace Trainer
- `--instruction_mask` — Masks instruction tokens in loss computation
- `--isolate_attention` — Isolates attention between packed sequences
- `--use_flash_attention_2` — Enables Flash Attention 2
- `--use_rpo` — Enables Robust Policy Optimization (Stage 3)
- `--downsample` — Balances data distribution via downsampling
- `--model_name` — HuggingFace model ID (e.g., `meta-llama/Meta-Llama-3-8B-Instruct`)

## Experiments Framework (`experiments/`)

The primary development workflow. Each experiment module is self-contained with consistent structure:

```
experiments/XX_name/
├── __init__.py
├── config.py           # Experiment-specific constants, prompts
├── run_experiment.py   # Main CLI (argparse)
├── analysis.py         # Post-processing
└── results/            # JSON output
```

### Shared Infrastructure (`experiments/shared/`)
- `config.py` — `MODEL_REGISTRY` with pricing for gpt-4o-mini, gpt-4o, gpt-4.1, gpt-4.1-nano, gpt-5-mini, qwen3:32b, llama3.1:8b, deepseek-r1:14b
- `llm_client.py` — `LLMClient` class: OpenAI/Ollama dual backend with retry logic, logprobs support for local models
- `prompts.py` — `extract_answer()`: 5-layer regex answer extraction
- `evaluation.py` — `tolerance_match()`, `semantic_match_judge()`, `mcnemar_test()`
- `data_loader.py` — Unified dataset loading interface

### RAG Experiments (`experiments/C1_hybrid_retrieval/`)

Separate from the main experiment framework. Uses OpenAI embeddings (`text-embedding-3-large`) + Milvus Lite vector DB.

```bash
pip install -r experiments/C1_hybrid_retrieval/requirements_rag.txt
export OPENAI_API_KEY="your-key"

# Four independent RAG implementations:
python experiments/C1_hybrid_retrieval/rag_agent_pragmatist.py       # LangGraph multi-turn agent
python experiments/C1_hybrid_retrieval/rag_langchain_advanced.py     # LangChain: rewrite + subquery + hybrid + rerank
python experiments/C1_hybrid_retrieval/rag_llama_index.py            # LlamaIndex standard
python experiments/C1_hybrid_retrieval/rag_llama_index_vector.py     # LlamaIndex vector-only
```

**Data paths (not in repo):** RAG implementations expect `thelma2/qa_dataset.json`; evaluation runners expect `./data/ultimate_rag_challenge_questions.json`.

## Dataset Notes

- No datasets contain official CFA Institute exam questions (all sourced from SchweserNotes)
- `flare-cfa` ≈ `FinEval-CFA-Easy` (near-duplicate); flare-cfa archived to `datasets/archived/`
- `CFA_Level_III` contains only MCQs despite its name (missing essay component)
- FinEval and FinTrain are Salesforce-hosted with EMNLP 2025 paper backing
- Training datasets are pre-tokenized on HuggingFace under `ZixuanKe/` namespace; `HF_TOKEN` required

## Git & File Notes

- `.gitignore` excludes all large data files (`datasets/FinTrain/*/data.json`, `datasets/CFA_Extracted/*/data.json`) and the entire `datasets/FinDap/` directory (nested git repo). Dataset metadata/READMEs are tracked but raw data is not.
- Performance baselines from project research: o4-mini achieves 79.1% on CFA Level III; GPT-4o scores 60.9% on financial math reasoning (vs. 92% human). These numbers inform the 20%+ error gap the research aims to address.

## Key Files

- `README.md` — Project overview with quick navigation, experiment commands, supported models
- `NOTE.md` — Comprehensive notes on all 41 research ideas with concrete examples (繁中)
- `RESULTS.md` — POC experiment results from 6 validated pipelines
- `MODELS.md` — Model pricing quick reference
