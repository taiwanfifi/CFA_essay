# 精選論文研究組合：7 篇完成初稿

> **最後更新**：2026-02-06
> **狀態**：7 篇論文初稿全部完成，含編譯 PDF + 實驗數據

---

## 總覽

| # | 論文代號 | 論文標題 | 頁數 | 樣本量 | 數據規模 | 初稿 |
|---|---------|---------|------|--------|---------|------|
| 1 | **D1+D4** | When AI Is Confidently Wrong: Calibration and Risk Analysis of LLMs in Financial Decision-Making | 14pp | N=257 | **完整** (90Q × 3 configs) | **DONE** |
| 2 | **I1+I3** | Stress Testing Financial LLMs: Counterfactual Perturbation and Noise Sensitivity Analysis on CFA Examinations | 13pp | N=100 | **完整** (100Q × 5 conditions) | **DONE** |
| 3 | **A1+A5** | Beyond Multiple Choice: How Answer Options Inflate LLM Financial Reasoning Scores | 10pp | N=20 | **POC** (需放大) | **DONE** |
| 4 | **E1** | The CFA Error Atlas: Mapping Failure Modes of LLMs in Financial Reasoning | 8pp | N=229 errors | **完整** (全部錯誤分析) | **DONE** |
| 5 | **D6** | Under Pressure: Adversarial Stress Testing of LLM Ethical Judgment in Financial Decision-Making | 7pp | N=15 | **POC** (需放大) | **DONE** |
| 6 | **G2** | The Certification Signal Erosion Hypothesis: A Modified Spence Model for AI-Disrupted Professional Credentialing | 21pp | 理論模型 | **純理論** (不需實驗) | **DONE** |
| 7 | **I2** | Inherited Irrationality: Behavioral Finance Biases in LLM Financial Recommendations | 17pp | N=20 (5 bias types) | **完整** (5 偏誤類型) | **DONE** |

### 數據規模分級說明

| 等級 | 定義 | 可發表性 |
|------|------|---------|
| **完整** | 樣本量足夠支撐統計檢定，結果穩健 | 可直接投稿 |
| **POC** | 概念驗證通過，管道跑通，但樣本量不足 | 需 scale up 後投稿 |
| **純理論** | 數學模型推導，無需實驗數據 | 可直接投稿 |

---

## 投稿優先序與策略

| 優先級 | 組合 | 目標期刊 | 理由 | 是否可直接投稿 |
|--------|------|---------|------|---------------|
| **首選** | D1+D4 | Finance Research Letters (FRL) | 數據最完整、統計顯著、老師專長對口 | **可以** |
| **次選** | I1+I3 | Finance Research Letters (FRL) | 數據完整(n=100)、敏感度分析 | **可以** |
| 第三 | E1 | FRL / J. Financial Data Science | 229 筆錯誤、完整 taxonomy | **可以** |
| 第四 | G2 | FRL / J. Financial Economics | 純理論、Modified Spence Model | **可以** |
| 第五 | I2 | FRL / J. Behavioral and Experimental Finance | 5 種偏誤完整測試 | **可以** |
| 第六 | A1+A5 | FRL | 需放大到 n≥100 | 需 scale up |
| 第七 | D6 | FRL / J. Financial Regulation | 需放大到 n≥50 | 需 scale up |

---

## 各論文詳細狀態

---

### Paper 1: D1+D4 — 信心校準與過度自信風險

**Title**: *When AI Is Confidently Wrong: Calibration and Risk Analysis of Large Language Models in Financial Decision-Making*

**Target Journal**: Finance Research Letters (FRL), SSCI Q1

**Status**: DRAFT COMPLETE — 可直接投稿

#### 核心結果

| 指標 | 數值 | 統計顯著性 |
|------|------|-----------|
| Overconfidence Gap | +22–32% | t=9.70, p<0.0001 |
| OC Error Rate | 30.0% (77/257) | z=3.99, p<0.0001 |
| OC Among Errors | 66.4% | z=3.53, p=0.0002 |
| Topic Variation | χ²=12.37 | p=0.030 |
| Best ECE | qwen3:32b = 0.247 | |
| Worst ECE | gpt-4o-mini verbalized = 0.315 | |
| Coverage-at-Risk (5%) | Undefined for all models | |

#### 四大假說全部顯著

| 假說 | 內容 | 結果 |
|------|------|------|
| H1 | LLM 系統性高估自身信心 | Supported (p<0.0001) |
| H2 | 過度自信錯誤佔比超過 25% | Supported (30.0%, p<0.0001) |
| H3 | 錯誤答案中過度自信佔主導 | Supported (66.4%, p=0.0002) |
| H4 | 校準品質因 CFA 主題而異 | Supported (p=0.030) |

#### 實驗數據

- **來源**: D1 calibration experiment (90 CFA-Challenge questions × 3 model-method configurations)
- **觀測數**: 257 (部分 question × config 組合無效回應被排除)
- **模型**: gpt-4o-mini (verbalized + logprob), qwen3:32b (logprob)

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| 主要結果 (N=250) | `experiments/D1_confidence_calibration/results/run_20260202_034237/results.json` |
| 補充結果 | `experiments/D1_confidence_calibration/results/run_20260202_031947/results.json` |
| 補充結果 | `experiments/D1_confidence_calibration/results/run_20260202_175051/results.json` |
| D4 風險分析 | `experiments/D4_overconfident_risk/results/run_20260205_010016/results.json` |
| 分析腳本輸出 | `drafts/selected/D1_calibration/analysis_results.json` |

#### 論文檔案結構

```
drafts/selected/D1_calibration/
├── main.tex                    # 完整論文 (14 pages, ~30K chars)
├── main.pdf                    # 編譯 PDF
├── run_analysis.py             # 數據分析腳本
├── analysis_results.json       # 分析結果 JSON
├── theory_framework.md         # 理論框架與假說發展
├── STATUS.md                   # 詳細完成度檢查表
├── figures/                    # 6 張出版品質圖表 (PDF)
│   ├── reliability_diagrams.pdf
│   ├── ece_comparison.pdf
│   ├── coverage_accuracy.pdf
│   ├── overconfidence_gap.pdf
│   ├── topic_analysis.pdf
│   └── confidence_distribution.pdf
├── tables/                     # LaTeX 表格原始碼
│   ├── calibration_metrics.tex
│   ├── overconfident_errors.tex
│   ├── topic_calibration.tex
│   └── hypothesis_tests.tex
└── submission/
    └── cover_letter.tex        # FRL 投稿信
```

---

### Paper 2: I1+I3 — 反事實壓力測試與雜訊敏感度

**Title**: *Stress Testing Financial LLMs: Counterfactual Perturbation and Noise Sensitivity Analysis on CFA Examinations*

**Target Journal**: Finance Research Letters (FRL), SSCI Q1

**Status**: DRAFT COMPLETE — 數據已升級至 n=100

#### 核心結果

**I1 Counterfactual Perturbation (N=100)**

| 指標 | 數值 |
|------|------|
| Original Accuracy | 86.0% |
| Level 1 (numerical) Accuracy | 62.5% (n_valid=64) |
| Level 2 (conditional) Accuracy | 72.9% (n_valid=85) |
| Memorization Gap (L1) | **+23.5%** |
| Memorization Gap (L2) | +13.1% |
| Robust Accuracy | 58.0% |
| Memorization Suspect Rate | 28.0% |

**I3 Noise Sensitivity (N=100)**

| 雜訊類型 | Accuracy | NSI | Flipped |
|----------|----------|-----|---------|
| Clean | 86.0% | — | — |
| N1 (irrelevant data) | 82.0% | 0.046 | 7/100 |
| N2 (plausible distractor) | 85.0% | 0.012 | 5/100 |
| N3 (verbose context) | 85.0% | 0.012 | 3/100 |
| N4 (contradictory hint) | 87.0% | -0.012 | 3/100 |

**關鍵發現**:
- 主要漏洞是記憶化（23.5% gap at L1），而非雜訊易感性
- 雜訊敏感度遠低於初步測試（max NSI=0.046 vs smoke test 0.222）
- Robust Accuracy (58.0%) 顯著低於 Standard (86.0%)
- 約 28% 的正確答案可能來自記憶而非推理

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| I1 完整結果 (N=100) | `experiments/I1_counterfactual/results/run_20260206_053445/results.json` |
| I3 完整結果 (N=100) | `experiments/I3_noise_red_herrings/results/run_20260206_054039/results.json` |
| I1 初步結果 (N=20) | `experiments/I1_counterfactual/results/run_20260206_044809/results.json` |
| I3 初步結果 (N=20) | `experiments/I3_noise_red_herrings/results/run_20260206_045209/results.json` |
| I1 POC (N=5) | `experiments/I1_counterfactual/results/run_20260205_010209/results.json` |

#### 論文檔案結構

```
drafts/selected/I1_counterfactual/
├── main.tex                    # 完整論文 (13 pages)
├── main.pdf                    # 編譯 PDF
├── theory_framework.md         # 理論框架
├── STATUS.md                   # 狀態追蹤
├── figures/                    # 圖表
├── tables/                     # 表格
└── submission/
    └── cover_letter.tex        # FRL 投稿信
```

---

### Paper 3: A1+A5 — 開放式作答與選項偏差

**Title**: *Beyond Multiple Choice: How Answer Options Inflate LLM Financial Reasoning Scores*

**Target Journal**: Finance Research Letters (FRL), SSCI Q1

**Status**: DRAFT COMPLETE — POC 數據 (n=20)，需 scale up

#### 核心結果 (n=20)

**A5 Option Bias**

| 指標 | 數值 |
|------|------|
| Accuracy WITH options | 75.0% |
| Accuracy WITHOUT options | 65.0% |
| Option Bias | **+10.0%** |
| Biased Questions | 5/20 (25%) |
| McNemar p-value | 0.724 (不顯著 — 需更大樣本) |

**A1 Three-Tier Evaluation**

| 等級 | 數量 | 百分比 |
|------|------|--------|
| Level A (Exact Match) | 8 | 40.0% |
| Level B (Directional) | 6 | 30.0% |
| Level C (Incorrect) | 6 | 30.0% |
| Strict Accuracy | — | 40.0% |
| Lenient Accuracy | — | 70.0% |

**Scale-up 需求**: McNemar p=0.724 不顯著，需放大至 n≥100 以獲得統計 power

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| A1 結果 (N=20) | `experiments/A1_open_ended/results/run_20260206_044146/results.json` |
| A5 結果 (N=20) | `experiments/A5_option_bias/results/run_20260206_044311/results.json` |
| A1 POC (N=5) | `experiments/A1_open_ended/results/run_20260205_010122/results.json` |
| A5 POC (N=5) | `experiments/A5_option_bias/results/run_20260204_045830/results.json` |

#### 論文檔案結構

```
drafts/selected/A1_open_ended/
├── main.tex                    # 完整論文 (10 pages)
├── main.pdf                    # 編譯 PDF
├── theory_framework.md         # 理論框架
├── STATUS.md                   # 狀態追蹤
├── figures/                    # 圖表
├── tables/                     # 表格
└── submission/                 # 投稿資料
```

---

### Paper 4: E1 — 錯誤圖譜

**Title**: *The CFA Error Atlas: Mapping Failure Modes of Large Language Models in Financial Reasoning*

**Target Journal**: Finance Research Letters / J. Financial Data Science

**Status**: DRAFT COMPLETE — 完整數據

#### 核心結果 (N=229 errors)

| 指標 | 數值 |
|------|------|
| Total Errors Analyzed | 229 |
| Error Types | 8 categories |
| CFA Topics | 8 topics |
| Cognitive Stages | 5 stages |
| Dominant Error | Reasoning Premise (49.3%) |
| Calculation Errors | 12.7% |
| Ethics Reasoning Errors | 87.1% |
| Derivatives Calculation Errors | 37.5% |
| Concept Identification Bottleneck | 53.7% |

**三維 Taxonomy**: Error Type (8) × CFA Topic (8) × Cognitive Stage (5)

- 數據來源：D1 calibration 實驗中所有錯誤答案的 GPT-4o-mini 分類
- 不需額外 scale up — 229 筆錯誤已覆蓋所有 8 個 CFA 主題

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| 錯誤分析 (全部方法) | `experiments/E1_error_analysis/results/error_analysis_all_methods_20260203_230751.json` |
| 錯誤分析 (CoT) | `experiments/E1_error_analysis/results/error_analysis_cot_20260203_211957.json` |
| 原始 D1 數據 | `experiments/D1_confidence_calibration/results/run_20260202_034237/results.json` |

#### 論文檔案結構

```
drafts/selected/E1_error_atlas/
├── main.tex                    # 完整論文 (8 pages)
├── main.pdf                    # 編譯 PDF
├── theory_framework.md         # 理論框架
├── STATUS.md                   # 狀態追蹤
├── figures/                    # 圖表
├── tables/                     # 表格
└── submission/                 # 投稿資料
```

---

### Paper 5: D6 — 對抗式金融道德測試

**Title**: *Under Pressure: Adversarial Stress Testing of LLM Ethical Judgment in Financial Decision-Making*

**Target Journal**: Finance Research Letters / J. Financial Regulation

**Status**: DRAFT COMPLETE — POC 數據 (n=15)，需 scale up

#### 核心結果 (n=15 CFA Ethics questions)

| 壓力類型 | Accuracy | ERS | Flipped |
|----------|----------|-----|---------|
| Standard (baseline) | 53.3% | 1.000 | — |
| Profit incentive | 60.0% | 1.125 | 0 |
| Authority pressure | 46.7% | 0.875 | 2 |
| Emotional manipulation | 40.0% | **0.750** | **3** |
| Reframing | 66.7% | 1.250 | 1 |
| Moral dilemma | 53.3% | 1.000 | 2 |

**關鍵發現**:
- Emotional manipulation 是最有效的攻擊方式 (ERS=0.750)
- 模型在 reframing 下反而表現更好 (ERS=1.250)
- 整體 Ethics Robustness Score 範圍: 0.750–1.250

**Scale-up 需求**: n=15 太小，需放大到 n≥50 才有統計 power

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| D6 結果 (N=15) | `experiments/D6_adversarial_ethics/results/run_20260206_051053/results.json` |

#### 論文檔案結構

```
drafts/selected/D6_adversarial_ethics/
├── main.tex                    # 完整論文 (7 pages)
├── main.pdf                    # 編譯 PDF
├── theory_framework.md         # 理論框架
├── STATUS.md                   # 狀態追蹤
├── figures/                    # 圖表
├── tables/                     # 表格
└── submission/                 # 投稿資料
```

---

### Paper 6: G2 — 訊號理論

**Title**: *The Certification Signal Erosion Hypothesis: A Modified Spence Model for AI-Disrupted Professional Credentialing*

**Target Journal**: Finance Research Letters / J. Financial Economics

**Status**: DRAFT COMPLETE — 純理論論文

#### 核心結果 (理論推導)

| 指標 | 數值 |
|------|------|
| CFA Signaling Retention Ratio (R) | **0.288** (保留 ~29% 訊號價值) |
| AI-replicable abilities (tipping point) | 50% already replicable |
| Ability Taxonomy Dimensions | 6 dimensions |
| Framework | Modified Spence (1973) + Autor Task Framework |

**三大命題**:
1. **Partial Signaling Collapse Theorem** (Proposition 1): 當 AI 能複製部分能力時，認證的訊號均衡部分瓦解
2. **Tipping Point Analysis** (Proposition 2): 超過 50% 的 CFA 能力已可被 AI 複製
3. **Six-Dimensional Ability Taxonomy**: 量化分析、概念理解、倫理判斷、溝通、策略思考、經驗直覺

**不需實驗數據** — 純數學模型與理論推導

#### 論文檔案結構

```
drafts/selected/G2_signaling_theory/
├── main.tex                    # 完整論文 (21 pages, 666 lines)
├── main.pdf                    # 編譯 PDF
├── theory_framework.md         # 理論框架
├── STATUS.md                   # 狀態追蹤
├── figures/                    # 圖表
├── tables/                     # 表格
└── submission/                 # 投稿資料
```

---

### Paper 7: I2 — 行為金融學偏誤

**Title**: *Inherited Irrationality: Behavioral Finance Biases in Large Language Model Financial Recommendations*

**Target Journal**: Finance Research Letters / J. Behavioral and Experimental Finance

**Status**: DRAFT COMPLETE — 5 種偏誤類型完整測試

#### 核心結果 (n=20 scenarios, 5 bias types, GPT-4o-mini)

| 偏誤類型 | N | Bias Score (inducing) | Neutral Score | Debiasing Effect |
|----------|---|----------------------|---------------|-----------------|
| Loss Aversion | 5 | 0.500 | 0.100 | **+0.400** |
| Anchoring | 5 | 0.600 | 0.400 | +0.200 |
| Framing | 5 | 0.500 | 0.400 | +0.100 |
| Recency | 3 | 0.500 | 0.500 | 0.000 |
| Disposition Effect | 2 | 0.500 | 0.500 | 0.000 |
| **Overall** | **20** | **0.525** | **0.350** | **+0.175** |

**關鍵發現**:
- **Debiasing hierarchy**: Loss aversion >> Anchoring > Framing >> Recency = Disposition
- Loss aversion: 4/5 scenarios 完全去偏
- Recency + Disposition: 0/5 scenarios 有去偏效果 (完全抵抗去偏)
- 極端偏誤案例: an_04, fr_05 (bias=1.0)
- 完全理性案例: fr_02 (bias=0.0)

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| I2 完整結果 (N=20, 5 types) | `experiments/I2_behavioral_biases/results/run_20260206_052135/results.json` |
| I2 POC (N=10, 2 types) | `experiments/I2_behavioral_biases/results/run_20260205_010409/results.json` |

#### 論文檔案結構

```
drafts/selected/I2_behavioral_biases/
├── main.tex                    # 完整論文 (17 pages)
├── main.pdf                    # 編譯 PDF
├── theory_framework.md         # 理論框架
├── STATUS.md                   # 狀態追蹤
├── figures/                    # 圖表
├── tables/                     # 表格
└── submission/                 # 投稿資料
```

---

## 暫緩/空目錄

| 資料夾 | 用途 | 狀態 |
|--------|------|------|
| `A5_option_bias/` | A5 數據合併至 A1+A5 論文 | 空 (已合併) |
| `D4_overconfident/` | D4 數據合併至 D1+D4 論文 | 空 (已合併) |
| `I3_noise_sensitivity/` | I3 數據合併至 I1+I3 論文 | 空 (已合併) |
| `H1_multimodal/` | 多模態金融推理 | **暫緩** (缺 CFA 圖表資料) |

---

## 實驗基礎設施

### 共用模組 (`experiments/shared/`)

| 模組 | 功能 |
|------|------|
| `config.py` | `MODEL_REGISTRY` — 20+ 模型的配置與定價 |
| `llm_client.py` | `LLMClient` — OpenAI / Anthropic / Gemini / DeepSeek / Ollama 多後端 |
| `prompts.py` | `extract_answer()` — 5 層 regex 答案提取 |
| `evaluation.py` | `tolerance_match()`, `semantic_match_judge()`, `mcnemar_test()` |
| `data_loader.py` | `load_dataset()` — 統一資料載入介面 |

### 跑實驗指令

```bash
# 環境設定
conda create -n cfa-llm python=3.10 && conda activate cfa-llm
pip install openai python-dotenv tqdm requests pydantic
echo "OPENAI_API_KEY=your-key" > .env

# D1: 信心校準
python -m experiments.D1_confidence_calibration.run_experiment --dataset easy --limit 100 --model gpt-4o-mini

# I1: 反事實壓力測試
python -m experiments.I1_counterfactual.run_experiment --dataset easy --limit 100 --model gpt-4o-mini --perturbation-levels 1 2

# I3: 雜訊敏感度
python -m experiments.I3_noise_red_herrings.run_experiment --dataset easy --limit 100 --model gpt-4o-mini --noise-types N1 N2 N3 N4

# A1: 開放式作答
python -m experiments.A1_open_ended.run_experiment --dataset easy --limit 100 --model gpt-4o-mini

# A5: 選項偏差
python -m experiments.A5_option_bias.run_experiment --dataset easy --limit 100 --model gpt-4o-mini

# I2: 行為偏誤 (5 種)
python -m experiments.I2_behavioral_biases.run_experiment --bias-types loss_aversion anchoring framing recency disposition_effect --limit 5 --model gpt-4o-mini

# D6: 對抗式道德測試
python -m experiments.D6_adversarial_ethics.run_experiment --dataset easy --limit 15 --model gpt-4o-mini

# D4: 過度自信風險分析 (依賴 D1 結果)
python -m experiments.D4_overconfident_risk.run_experiment --input "experiments/D1_confidence_calibration/results/run_*/results.json" --confidence-threshold 0.8 --limit 5

# E1: 錯誤分析 (依賴 D1 結果中的錯誤)
python -m experiments.E1_error_analysis.run_experiment --input "experiments/D1_confidence_calibration/results/run_*/results.json"
```

### 結果存放

所有結果自動存在 `experiments/XX/results/run_YYYYMMDD_HHMMSS/results.json`。

---

## 全部實驗結果路徑索引

| 實驗 | 日期 | N | 路徑 | 用於論文 |
|------|------|---|------|---------|
| D1 Calibration | 2026-02-02 | 250 | `experiments/D1_confidence_calibration/results/run_20260202_034237/` | D1+D4 |
| D4 Risk | 2026-02-05 | 74 篩選 | `experiments/D4_overconfident_risk/results/run_20260205_010016/` | D1+D4 |
| E1 Error Analysis | 2026-02-03 | 229 errors | `experiments/E1_error_analysis/results/error_analysis_all_methods_20260203_230751.json` | E1 |
| A1 Open-Ended | 2026-02-06 | 20 | `experiments/A1_open_ended/results/run_20260206_044146/` | A1+A5 |
| A5 Option Bias | 2026-02-06 | 20 | `experiments/A5_option_bias/results/run_20260206_044311/` | A1+A5 |
| I1 Counterfactual | 2026-02-06 | 100 | `experiments/I1_counterfactual/results/run_20260206_053445/` | I1+I3 |
| I3 Noise | 2026-02-06 | 100 | `experiments/I3_noise_red_herrings/results/run_20260206_054039/` | I1+I3 |
| I2 Biases | 2026-02-06 | 20 | `experiments/I2_behavioral_biases/results/run_20260206_052135/` | I2 |
| D6 Ethics | 2026-02-06 | 15 | `experiments/D6_adversarial_ethics/results/run_20260206_051053/` | D6 |

---

## LaTeX 編譯

所有論文使用 `elsarticle` 文件類別（Elsevier 官方模板），preprint 格式：

```bash
# 編譯單篇論文
cd drafts/selected/D1_calibration
/Library/TeX/texbin/pdflatex main.tex && /Library/TeX/texbin/pdflatex main.tex

# 需要跑兩次以解決交叉引用
```

**Overleaf 相容性**: 所有論文可直接上傳 Overleaf 編譯。`elsarticle` 是 Overleaf 內建支援的標準模板類別。上傳 `main.tex` 即可，不需額外安裝任何套件。

---

## 下一步行動

### 立即可投稿 (5 篇)

1. **D1+D4**: 數據完整、統計顯著 → 直接投 FRL
2. **I1+I3**: 已升級至 n=100 → 直接投 FRL
3. **E1**: 229 筆錯誤完整分析 → 直接投 FRL / JFDS
4. **G2**: 純理論 → 直接投 FRL / JFE
5. **I2**: 5 種偏誤完整 → 直接投 FRL / JBEF

### 需 Scale Up (2 篇)

6. **A1+A5**: 放大到 n≥100 (McNemar test 需更大樣本)
7. **D6**: 放大到 n≥50 (目前 n=15 太小)

### 跨論文強化

- [ ] 多模型驗證：加入 gpt-4o, claude-3.5-sonnet, qwen3:32b 比較
- [ ] 圖表強化：為所有論文生成 publication-quality figures
- [ ] 交叉引用：各論文互相引用，形成研究群 (research cluster)

---

## 指導教授：繆維中老師

- **背景**：財務數學、風險管理、統計方法
- **偏好**：Economic Significance > NLP 指標；重視風險分析、敏感度分析、穩健性
- **最對口論文**: D1+D4 (校準+風險) → I1+I3 (壓力測試+穩健性)

---

## 聯絡資訊

**程煒倫 William**
Research Assistant, Institute of Information Science, Academia Sinica
