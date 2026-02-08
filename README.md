# CFA + LLM 研究專案

本專案系統性研究大型語言模型在 CFA 特許金融分析師考試上的能力與局限，產出 **7 篇論文**，全部投稿 Finance Research Letters。

**核心問題**：金融 LLM 的評估正處於尷尬位置——所有人都在刷 benchmark 分數，但沒人追問：
- **準確率是真的嗎**？（MCQ 選項是拐杖、題目可能被背過）
- **錯的時候知道自己錯嗎**？（過度自信比答錯更危險）
- **在真實環境下還能維持嗎**？（噪音、偏誤、對抗攻擊）

**作者**：程煒倫 (Wei-Lun Cheng)，台科大財金所博士班
**指導教授**：主要指導教授 Daniel Wei-Chung Miao (繆維中)、共同指導教授 Guang-Di Chang (張光第)
**單位**：Graduate Institute of Finance, National Taiwan University of Science and Technology (NTUST)

---

## 論文 → 實驗 對照表

| # | 論文 | 實驗模組 | 資料集 | 樣本量 | 字數 |
|---|------|---------|--------|--------|------|
| **P1** | Beyond Multiple Choice (A1+A5) | `A1_open_ended` + `A5_option_bias` | CFA-Easy | N=1,032 | 3,719 |
| **P2** | Stress Testing Financial LLMs (I1+I3) | `I1_counterfactual` + `I3_noise_red_herrings` | CFA-Easy | N=1,032 | 4,367 |
| **P3** | Inherited Irrationality (I2) | `I2_behavioral_biases` | 自建場景 | 60 scenarios | 3,395 |
| **P4** | Under Pressure (D6) | `D6_adversarial_ethics` | CFA-Easy (ethics) | N=47 | 3,536 |
| **P5** | The CFA Error Atlas (E1) | `E1_error_analysis` + A1 結果 | CFA-Easy | 557 errors | 2,627 |
| **P6** | When AI Is Confidently Wrong (D1+D4) | `D1_confidence_calibration` + `D4_overconfident_risk` | CFA-Challenge | N=90 | 3,463 |
| **P7** | Certification Signal Erosion (G2) | 引用 A5 數據（理論論文） | CFA-Easy | N=1,032 | 4,231 |

### 實驗結果位置（僅保留 final runs）

| 實驗 | GPT-4o-mini Final | GPT-5-mini Final |
|------|-------------------|-----------------|
| A1 | `results/run_20260206_173445/` | `results/run_20260207_174118/` |
| A5 | `results/run_20260206_171904/` | `results/run_20260207_174114/` |
| I1 | `results/run_20260206_170129/` | `results/run_20260207_174116/` |
| I2 | `results/run_20260206_140527/` | — (removed, unreliable) |
| I3 | `results/run_20260206_203913/` | `results/run_20260207_174115/` |
| D1 | `results/run_20260202_034237/` | — |
| D4 | `results/run_20260205_010016/` | — |
| D6 | `results/run_20260206_112341/` | `results/run_20260207_023637/` |
| E1 | `error_analysis_*230751.json` + `golden_context_*032341.json` | `golden_context_*220440.json` |

---

## 7 篇論文核心結果

### P1: Beyond Multiple Choice — 開放式作答 + 選項偏差 (A1+A5)

| 指標 | GPT-4o-mini | GPT-5-mini |
|------|------------|------------|
| MCQ 準確率 | 82.6% | 92.8% |
| 開放式 Strict (Level A) | 24.5% | 41.8% |
| 開放式 Lenient (A+B) | 46.0% | 64.1% |
| Option Bias | +1.9pp (p=0.251, n.s.) | +9.6pp (p<0.001***) |

**關鍵發現**：選項偏差是模型依賴的——更強模型反而更依賴選項線索。

### P2: Stress Testing — 反事實 + 雜訊敏感度 (I1+I3)

| 指標 | GPT-4o-mini | GPT-5-mini |
|------|------------|------------|
| 原題準確率 | 82.4% | 91.8% |
| 擾動後準確率 | 63.8% | 55.3% |
| Memorization Gap | 18.6pp | 36.4pp |
| N1 Noise Sensitivity | 0.032 | 0.017 |

**關鍵發現**：GPT-5-mini 的記憶差距翻倍（36.4pp），更強的模型可能更依賴記憶。

### P3: Inherited Irrationality — 行為金融偏誤 (I2)

| 偏誤類型 | 偏誤分數 | Debiasing 效果 |
|----------|---------|---------------|
| Loss Aversion | 0.650 | +0.400（最易去偏）|
| Anchoring | 0.500 | +0.200 |
| Framing | 0.350 | +0.100 |
| Overconfidence | 0.600 | +0.050 |
| Recency | 0.400 | 0.000（完全抵抗）|
| Disposition Effect | 0.450 | 0.000（完全抵抗）|

**關鍵發現**：LLM 繼承了人類的行為偏誤，但去偏效果因偏誤類型差異極大。

### P4: Under Pressure — 對抗式道德測試 (D6)

| 指標 | GPT-4o-mini | GPT-5-mini |
|------|------------|------------|
| 標準準確率 | 85.1% | 91.5% |
| 道德翻轉次數 | 14 flips | 0 flips |
| 最弱攻擊面 | Profit / Authority (ERS=0.925) | 完全免疫 |

**關鍵發現**：GPT-4o-mini 可被道德壓力攻擊翻轉，GPT-5-mini 完全免疫。

### P5: The CFA Error Atlas — 錯誤分類 + 黃金知識注入 (E1)

| 指標 | GPT-4o-mini | GPT-5-mini (cross-model) |
|------|------------|--------------------------|
| 557 errors 分類 | 概念錯誤 68.8%，推理不完整 10.8% | — |
| GCI 修復率 (any) | 82.4% | 88.3% |
| GCI 完全修復 (Level A) | 25.5% | 50.4% |
| 仍然答錯 | 17.6% | 11.7% |

**關鍵發現**：82.4% 的錯誤可透過提供正確知識修復 → 主要是知識不足，非推理缺陷。

### P6: When AI Is Confidently Wrong — 信心校準 + 過度自信 (D1+D4)

| 指標 | GPT-4o-mini | qwen3:32b |
|------|------------|-----------|
| ECE (Verbalized) | 0.315 | 0.247 |
| ECE (Self-Consistency) | 0.307 | — |
| Overconfidence Gap | +22–32% | — |
| OC Error Rate | 30.0% | — |

**關鍵發現**：30% 的錯誤是高信心錯誤——模型完全確信但答案錯誤。

### P7: Certification Signal Erosion — CFA 訊號理論 (G2)

| 指標 | 數值 |
|------|------|
| CFA Signaling Retention Ratio | R = 0.288 (~29%) |
| Format Invariance | GPT-4o-mini: 成立 (p=0.251) → GPT-5-mini: 不成立 (p<0.001) |

**關鍵發現**：AI 已能複製 ~50% 的 CFA 能力，認證僅保留 29% 訊號價值。格式改革無法阻止訊號侵蝕，需要內容改革。

---

## 專案結構

```
CFA_essay/
├── drafts/selected/              # 7 篇論文（LaTeX + PDF）
│   ├── A1_open_ended/            # P1: Beyond Multiple Choice
│   ├── I1_counterfactual/        # P2: Stress Testing
│   ├── I2_behavioral_biases/     # P3: Inherited Irrationality
│   ├── D6_adversarial_ethics/    # P4: Under Pressure
│   ├── E1_error_atlas/           # P5: The CFA Error Atlas
│   ├── D1_calibration/           # P6: When AI Is Confidently Wrong
│   └── G2_signaling_theory/      # P7: Certification Signal Erosion
│
├── experiments/                   # 實驗程式碼 + 最終結果
│   ├── shared/                    # 共用模組（LLM client, 評分, 資料載入）
│   ├── A1_open_ended/             # 開放式作答（P1, P5 使用）
│   ├── A5_option_bias/            # 選項偏差量化（P1, P7 使用）
│   ├── D1_confidence_calibration/ # 信心校準（P6）
│   ├── D4_overconfident_risk/     # 過度自信風險（P6）
│   ├── D6_adversarial_ethics/     # 對抗式道德測試（P4）
│   ├── E1_error_analysis/         # 錯誤分類 + GCI（P5）
│   ├── I1_counterfactual/         # 反事實壓力測試（P2）
│   ├── I2_behavioral_biases/      # 行為偏誤（P3）
│   └── I3_noise_red_herrings/     # 雜訊敏感度（P2）
│
├── datasets/FinEval/              # 評估資料集
│   ├── CFA_Challenge/             # 90 題（難）— D1, D4 使用
│   ├── CFA_Easy/                  # 1,032 題（標準）— 大部分實驗使用
│   └── CRA_Bigdata/               # 1,472 題（股價預測）
│
├── docs/                          # 研究文書（繁中）
└── drafts/ideas/                  # 42 個研究點子
```

---

## 快速開始

### 環境設定

```bash
conda create -n cfa-llm python=3.10 && conda activate cfa-llm
pip install openai python-dotenv tqdm requests pydantic
echo "OPENAI_API_KEY=your-key-here" > .env
```

### 跑實驗

所有實驗使用統一的 CLI 模式：

```bash
# A1: 開放式作答
python -m experiments.A1_open_ended.run_experiment --dataset easy --model gpt-4o-mini

# A5: 選項偏差
python -m experiments.A5_option_bias.run_experiment --dataset easy --model gpt-4o-mini

# I1: 反事實壓力測試
python -m experiments.I1_counterfactual.run_experiment --dataset easy --model gpt-4o-mini

# I2: 行為偏誤
python -m experiments.I2_behavioral_biases.run_experiment --bias-types loss_aversion anchoring framing recency disposition_effect overconfidence --model gpt-4o-mini

# I3: 雜訊敏感度
python -m experiments.I3_noise_red_herrings.run_experiment --dataset easy --model gpt-4o-mini --noise-types N1 N2 N3 N4

# D1: 信心校準
python -m experiments.D1_confidence_calibration.run_experiment --dataset challenge --model gpt-4o-mini

# D4: 過度自信分析（需要 D1 結果）
python -m experiments.D4_overconfident_risk.run_experiment --input "experiments/D1_confidence_calibration/results/run_*/results.json"

# D6: 對抗式道德測試
python -m experiments.D6_adversarial_ethics.run_experiment --dataset easy --model gpt-4o-mini
```

結果存在 `experiments/XX/results/run_YYYYMMDD_HHMMSS/results.json`。

---

## 支援的模型

| Provider | Model | 用於 |
|----------|-------|------|
| OpenAI | gpt-4o-mini | 所有 7 篇論文的主要模型 |
| OpenAI | gpt-5-mini | 跨模型驗證（P1, P2, P4, P5）|
| Ollama | qwen3:32b | D1 信心校準（本地模型對照）|

---

## 資料集說明

- 所有 CFA 題目來自 **SchweserNotes**，非 CFA Institute 官方考題
- 資料集由 Salesforce AI Research 整理，EMNLP 2025 論文背書
- 技術基礎：[FinDAP](https://github.com/SalesforceAIResearch/FinDAP) (EMNLP 2025 Oral)

---

## 授權

本專案僅供學術研究使用。
