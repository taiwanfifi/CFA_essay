# CFA + LLM 研究專案

本專案以 **FinDAP** (Demystifying Domain-adaptive Post-training for Financial LLMs, EMNLP 2025 Oral) 為技術基礎，系統性研究大型語言模型在 CFA 特許金融分析師考試上的能力與局限。

**核心問題**：金融 LLM 的評估正處於尷尬位置——所有人都在刷 benchmark 分數，但沒人追問：
- **準確率是真的嗎**？（MCQ 選項是拐杖、題目可能被背過）
- **錯的時候知道自己錯嗎**？（過度自信比答錯更危險）
- **在真實環境下還能維持嗎**？（噪音、偏誤、多模態）

**作者**：程煒倫 (Wei-Lun Cheng)，台科大財金所博士班
**指導教授**：主要指導教授 Daniel Wei-Chung Miao (繆維中)、共同指導教授 Guang-Di Chang (張光第)
**單位**：Graduate Institute of Finance, National Taiwan University of Science and Technology (NTUST, 國立臺灣科技大學)

---

## 專案進度

> **最後更新**：2026-02-06

**7 篇論文全部可投稿**，含編譯 PDF、完整實驗數據、14 張圖表。

| 論文 | 標題 | 頁數 | 樣本量 | 狀態 |
|------|------|------|--------|------|
| **D1+D4** | When AI Is Confidently Wrong | 15pp | N=257 | 可投稿 |
| **I1+I3** | Stress Testing Financial LLMs | 17pp | N=100 | 可投稿 |
| **E1** | The CFA Error Atlas | 11pp | N=229 | 可投稿 |
| **G2** | Certification Signal Erosion | 24pp | 理論 | 可投稿 |
| **I2** | Inherited Irrationality | 23pp | N=20 | 可投稿 |
| **D6** | Under Pressure | 9pp | N=47 | 可投稿 |
| **A1+A5** | Beyond Multiple Choice | 11pp | N=100 | 可投稿 |

詳細的論文狀態、核心數據、檔案結構、數據路徑見 [`drafts/selected/README.md`](drafts/selected/README.md)。

---

## 快速導覽

| 想做什麼 | 去哪裡 |
|---------|--------|
| 看 7 篇論文完整狀態 | [`drafts/selected/README.md`](drafts/selected/README.md) |
| 了解研究方向 | `docs/03-研究方向深度設計.md` |
| 看論文 PDF | `drafts/selected/*/main.pdf` |
| 看實驗程式碼 | `experiments/` |
| 看實驗結果 | `experiments/*/results/run_*/results.json` |
| 看模型定價 | `MODELS.md` |
| 跑實驗 | 見下方「快速開始」 |

---

## 專案結構

```
CFA_essay/
├── docs/                          # 研究文書（5 篇，繁中）
│   ├── 01-數據集完整手冊.md       # 12 個資料集的權威參考
│   ├── 02-文獻綜述與研究定位.md   # 5 篇核心論文 + 6 個研究空白
│   ├── 03-研究方向深度設計.md     # 7 個研究方向 + 論文拆分策略
│   ├── 04-FinDAP框架解析.md       # 程式碼架構 + 局限與改進空間
│   └── 05-審稿人挑戰與應對策略.md # 6 大挑戰 + 量化防禦
│
├── drafts/                        # 論文提案與初稿
│   ├── ideas/                     # 41 個研究點子（每個一個 .md）
│   └── selected/                  # 7 篇完成初稿 + 詳細 README
│       ├── README.md              # 論文總覽、數據路徑、投稿策略
│       ├── D1_calibration/        # D1+D4: 信心校準 (15pp, N=257)
│       ├── I1_counterfactual/     # I1+I3: 壓力測試 (17pp, N=100)
│       ├── A1_open_ended/         # A1+A5: 開放式作答 (11pp, N=100)
│       ├── E1_error_atlas/        # E1: 錯誤圖譜 (11pp, N=229)
│       ├── D6_adversarial_ethics/ # D6: 道德壓力測試 (9pp, N=47)
│       ├── G2_signaling_theory/   # G2: 訊號理論 (24pp, 理論)
│       └── I2_behavioral_biases/  # I2: 行為偏誤 (23pp, N=20)
│
├── experiments/                   # 實驗程式碼 + 結果
│   ├── shared/                    # 共用模組（LLM client, prompts, evaluation）
│   ├── A1_open_ended/             # 開放式作答基準
│   ├── A5_option_bias/            # MCQ 選項偏差量化
│   ├── B1_multistep_agent/        # 多步驟推理 Agent
│   ├── C1_hybrid_retrieval/       # RAG 實驗（4 種實作）
│   ├── D1_confidence_calibration/ # 信心校準
│   ├── D4_overconfident_risk/     # 過度自信風險分析
│   ├── D6_adversarial_ethics/     # 對抗式道德測試
│   ├── E1_error_analysis/         # 錯誤圖譜
│   ├── I1_counterfactual/         # 反事實壓力測試
│   ├── I2_behavioral_biases/      # 行為金融偏誤
│   └── I3_noise_red_herrings/     # 雜訊敏感度
│
├── datasets/                      # 資料集
│   ├── FinEval/                   # 評估資料集
│   │   ├── CFA_Challenge/         # 90 題（難）
│   │   ├── CFA_Easy/              # 1,032 題（標準）
│   │   └── CRA_Bigdata/           # 1,472 題（股價預測）
│   ├── FinTrain/                  # 訓練資料集
│   └── FinDap/                    # FinDAP 訓練框架
│
├── findings/                      # 跨實驗發現（待填）
├── RESULTS.md                     # POC 實驗結果總覽
├── MODELS.md                      # 模型定價速查表
├── NOTE.md                        # 41 個研究點子總筆記
└── CLAUDE.md                      # Claude Code 專案指引
```

---

## 7 篇論文核心結果摘要

### D1+D4: 信心校準與過度自信風險 (N=257)

| 指標 | 數值 | p-value |
|------|------|---------|
| Overconfidence Gap | +22–32% | <0.0001 |
| OC Error Rate | 30.0% | <0.0001 |
| Best ECE | qwen3:32b = 0.247 | — |
| Worst ECE | gpt-4o-mini = 0.315 | — |

### I1+I3: 壓力測試 (N=100)

| 指標 | 數值 |
|------|------|
| Memorization Gap (L1) | +23.5% |
| Robust Accuracy | 58.0% (vs 86.0% standard) |
| Max NSI (noise sensitivity) | 0.046 |
| Memorization Suspect Rate | 28.0% |

### A1+A5: 開放式作答 (N=100)

| 指標 | 數值 |
|------|------|
| Option Bias | +12.0 pp |
| McNemar p-value | 0.045 (顯著) |
| Strict Accuracy (open-ended) | 34.0% |
| Lenient Accuracy | 62.0% |
| Dominant Error | Conceptual Error (55.3%) |

### E1: 錯誤圖譜 (N=229 errors)

| 指標 | 數值 |
|------|------|
| Dominant Error Type | Reasoning Premise (49.3%) |
| Calculation Errors | 12.7% |
| Concept Identification Bottleneck | 53.7% |

### D6: 道德壓力測試 (N=47)

| 壓力類型 | Accuracy | ERS | Flipped |
|----------|----------|-----|---------|
| Standard | 85.1% | 1.000 | — |
| Profit incentive | 78.7% | 0.925 | 4 |
| Authority pressure | 78.7% | 0.925 | 3 |
| Emotional manipulation | 80.8% | 0.950 | 2 |
| Reframing | 80.8% | 0.950 | 3 |
| Moral dilemma | 80.8% | 0.950 | 2 |

### G2: 訊號理論 (理論)

| 指標 | 數值 |
|------|------|
| CFA Signaling Retention | R = 0.288 (~29%) |
| AI-replicable abilities | 50% tipping point |

### I2: 行為偏誤 (N=20, 5 bias types)

| 偏誤類型 | Debiasing Effect |
|----------|-----------------|
| Loss Aversion | +0.400 (最易去偏) |
| Anchoring | +0.200 |
| Framing | +0.100 |
| Recency / Disposition | 0.000 (完全抵抗) |

---

## 快速開始

### 環境設定

```bash
# 建立環境
conda create -n cfa-llm python=3.10 && conda activate cfa-llm

# 安裝依賴
pip install openai python-dotenv tqdm requests pydantic

# 設定 API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

### 跑實驗

```bash
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

# I2: 行為偏誤
python -m experiments.I2_behavioral_biases.run_experiment --bias-types loss_aversion anchoring framing recency disposition_effect --limit 5 --model gpt-4o-mini

# D6: 對抗式道德測試
python -m experiments.D6_adversarial_ethics.run_experiment --dataset easy --limit 15 --model gpt-4o-mini

# D4: 過度自信風險分析（需要 D1 結果）
python -m experiments.D4_overconfident_risk.run_experiment --input "experiments/D1_confidence_calibration/results/run_*/results.json" --confidence-threshold 0.8 --limit 5
```

### 輸出位置

每個實驗的結果存在 `experiments/XX/results/run_YYYYMMDD_HHMMSS/results.json`。

---

## 實驗架構

### 每個實驗的結構

```
experiments/XX_name/
├── __init__.py
├── config.py           # 實驗專屬常數、prompt 模板
├── run_experiment.py   # 主 CLI（argparse）
├── analysis.py         # 後處理分析
└── results/            # JSON 輸出
```

### 共用模組 (`experiments/shared/`)

| 模組 | 功能 |
|------|------|
| `config.py` | `MODEL_REGISTRY`：所有支援模型的配置 |
| `llm_client.py` | `LLMClient`：OpenAI / Anthropic / Gemini / DeepSeek / Ollama 多後端 |
| `prompts.py` | `extract_answer()`：5 層 regex 答案提取 |
| `evaluation.py` | `tolerance_match()`、`semantic_match_judge()`、`mcnemar_test()` |
| `data_loader.py` | `load_dataset()`：統一資料載入介面 |

### 典型流程

```
輸入：CFA 題目（JSON）
  ↓
處理：
  1. 載入題目 → data_loader.py
  2. 建構 prompt → config.py / prompts.py
  3. 呼叫 LLM → llm_client.py
  4. 提取答案 → prompts.py
  5. 評判正確性 → evaluation.py
  ↓
輸出：results.json（含 metadata, summary, 逐題結果）
```

---

## 支援的模型

詳見 `MODELS.md`。

### 雲端模型

| Provider | Model | Input $/M | Output $/M |
|----------|-------|----------|------------|
| OpenAI | gpt-4o-mini | $0.15 | $0.60 |
| OpenAI | gpt-4o | $2.50 | $10.00 |
| OpenAI | gpt-4.1 | $2.00 | $8.00 |
| OpenAI | gpt-4.1-nano | $0.10 | $0.40 |
| OpenAI | gpt-5-mini | $0.25 | $2.00 |
| Anthropic | Claude 3.5 Sonnet | $3.00 | $15.00 |
| Google | Gemini 2.5 Pro | $1.25 | $10.00 |
| Google | Gemini 2.5 Flash | $0.15 | $0.60 |

### 本地模型 (Ollama)

| Model | VRAM |
|-------|------|
| qwen3:32b | ~20GB |
| llama3.1:8b | ~6GB |
| deepseek-r1:14b | ~10GB |

---

## 關鍵發現

- 所有 CFA 資料集均非官方真題（SchweserNotes 來源，有 EMNLP 2025 論文背書）
- 最佳模型 (o4-mini) 在 CFA Level III 上準確率 79.1%，仍有 20%+ 錯誤率
- GPT-4o 在金融數學推理上僅 60.9%（vs 人類 92%），差距 31%
- **30% 的錯誤是高信心錯誤** — 模型完全確信但答案錯誤 (D1+D4)
- **23.5% Memorization Gap** — 約 28% 的正確答案可能來自記憶而非推理 (I1+I3)
- **49.3% 推理前提錯誤** — 不是計算錯，是理解就錯了 (E1)
- **CFA 認證僅保留 29% 訊號價值** — AI 已能複製 50% 的 CFA 能力 (G2)
- **Loss aversion 最易去偏，recency/disposition 完全抵抗** (I2)
- **Option bias +12.0 pp 且統計顯著** (McNemar p=0.045) — MCQ 格式系統性高估模型能力，開放式作答 strict accuracy 僅 34% (A1+A5)
- **所有 5 種道德壓力均使準確率下降** — 利益誘導與權威壓力最有效 (ERS=0.925)，無反常提升 (D6)

---

## 下一步

### 7 篇論文全部可投稿

1. **D1+D4** → Finance Research Letters (首選)
2. **I1+I3** → Finance Research Letters
3. **E1** → FRL / J. Financial Data Science
4. **G2** → FRL / J. Financial Economics
5. **I2** → FRL / J. Behavioral and Experimental Finance
6. **D6** → FRL / J. Business Ethics
7. **A1+A5** → FRL / J. Financial Education

所有論文圖表已生成（共 14 張），PDF 已編譯完成。

### 強化方向

- 多模型驗證：加入 gpt-4o, claude-3.5-sonnet, qwen3:32b
- 各論文交叉引用形成研究群

---

## 建議閱讀順序

1. **快速了解數據**：`docs/01-數據集完整手冊.md`
2. **了解研究現狀**：`docs/02-文獻綜述與研究定位.md`
3. **核心——研究方向**：`docs/03-研究方向深度設計.md`
4. **看論文初稿狀態**：`drafts/selected/README.md`
5. **技術參考**：`docs/04-FinDAP框架解析.md`
6. **論文防禦**：`docs/05-審稿人挑戰與應對策略.md`

---

## 聯絡資訊

程煒倫 (Wei-Lun Cheng)
Graduate Institute of Finance, National Taiwan University of Science and Technology (NTUST)
國立臺灣科技大學 財務金融研究所 博士班

## 授權

本專案僅供學術研究使用。CFA 相關資料來源為 SchweserNotes，非官方考題。
