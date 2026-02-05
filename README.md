# CFA + LLM 研究專案

本專案以 **FinDAP** (Demystifying Domain-adaptive Post-training for Financial LLMs, EMNLP 2025 Oral) 為技術基礎，系統性研究大型語言模型在 CFA 特許金融分析師考試上的能力與局限。

**核心問題**：金融 LLM 的評估正處於尷尬位置——所有人都在刷 benchmark 分數，但沒人追問：
- **準確率是真的嗎**？（MCQ 選項是拐杖、題目可能被背過）
- **錯的時候知道自己錯嗎**？（過度自信比答錯更危險）
- **在真實環境下還能維持嗎**？（噪音、偏誤、多模態）

---

## 快速導覽

| 想做什麼 | 去哪裡 |
|---------|--------|
| 了解研究方向 | `docs/03-研究方向深度設計.md` |
| 看 10 篇論文提案 | `drafts/selected/README.md` |
| 看實驗程式碼 | `experiments/` |
| 看 POC 實驗結果 | `RESULTS.md` |
| 看模型定價 | `MODELS.md` |
| 跑實驗 | 見下方「快速開始」 |

---

## 專案結構

```
CFA_essay/
├── docs/                          # 研究文書（5 篇，繁中）
│   ├── 01-數據集完整手冊.md       # 12 個資料集的權威參考
│   ├── 02-文獻綜述與研究定位.md   # 5 篇核心論文 + 6 個研究空白
│   ├── 03-研究方向深度設計.md     # 7 個研究方向 + 論文拆分策略 ★
│   ├── 04-FinDAP框架解析.md       # 程式碼架構 + 局限與改進空間
│   └── 05-審稿人挑戰與應對策略.md # 6 大挑戰 + 量化防禦
│
├── drafts/                        # 論文提案
│   ├── ideas/                     # 41 個研究點子（每個一個 .md）
│   └── selected/                  # 精選 10 篇 + README 路線圖 ★
│
├── experiments/                   # 實驗程式碼 + 結果
│   ├── shared/                    # 共用模組（LLM client, prompts, evaluation）
│   ├── A1_open_ended/             # 開放式作答基準
│   ├── A5_option_bias/            # MCQ 選項偏差量化
│   ├── B1_multistep_agent/        # 多步驟推理 Agent
│   ├── C1_hybrid_retrieval/       # RAG 實驗（4 種實作）
│   ├── D1_confidence_calibration/ # 信心校準
│   ├── D4_overconfident_risk/     # 過度自信風險分析
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

## 10 個研究題目

分成五條戰線，構成完整攻擊鏈：

### 戰線一：拆穿 Benchmark 假象

| 題目 | 測什麼 | 新穎點 |
|------|--------|--------|
| **A1** Open-Ended | 移除選項後的真實推理能力 | 三層判定機制 + 結構化錯誤歸因 |
| **A5** Option Bias | 選項提供了多少不公平優勢 | 精確量化 option bias 的三維分解 |

### 戰線二：揭露過度自信

| 題目 | 測什麼 | 新穎點 |
|------|--------|--------|
| **D1** Calibration | 模型的信心值是否可靠 | 四種 confidence 方法的金融場景比較 |
| **D4** Risk Analysis | 高信心錯誤答案的系統性風險 | CFA Ethics 框架 + 監管啟示 |

### 戰線三：繪製錯誤地圖

| 題目 | 測什麼 | 新穎點 |
|------|--------|--------|
| **E1** Error Atlas | 錯誤的精確分類 | 三維 Taxonomy（類型×主題×階段） |

### 戰線四：開闢新戰場

| 題目 | 測什麼 | 新穎點 |
|------|--------|--------|
| **H1** Multimodal | 圖表理解是否為獨立瓶頸 | 首個多模態 CFA 基準（暫緩，缺圖片） |
| **G2** Signaling | AI 如何瓦解專業認證的訊號價值 | Modified Spence Model（純理論） |

### 戰線五：對抗性壓力測試

| 題目 | 測什麼 | 新穎點 |
|------|--------|--------|
| **I1** Counterfactual | 背題 vs 真懂金融邏輯 | Robust Accuracy + Memorization Gap |
| **I2** Biases | LLM 是否繼承人類非理性偏誤 | 六維偏誤框架 + Debiasing 實驗 |
| **I3** Noise | 模型能否過濾無關資訊 | Noise Sensitivity Index |

---

## 已完成的實驗

### POC 驗證（2026-02-04 ~ 05）

6 個新實驗管道全部跑通：

| 實驗 | N | 核心指標 | 數值 | 狀態 |
|------|---|----------|------|------|
| A5 Option Bias | 5 題 | Option Bias | **-40.0%** | OK |
| I3 Noise | 5×4 | NSI | **0.000** | OK |
| D4 Risk | 250→74→5 | High-risk | **5/5** | OK |
| A1 Open-Ended | 5 題 | Strict/Lenient | **60%/80%** | OK |
| I1 Counterfactual | 5 題 | Mem. Gap | **+10.0%** | OK |
| I2 Biases | 10 情境 | Bias Score | **0.500** | OK |

詳細結果見 `RESULTS.md`。

### 先前完成

| 實驗 | 規模 | 關鍵結果 |
|------|------|---------|
| B1 Multi-step Agent | 90 題 | CoT+tool 驗證提升準確率 |
| D1 Calibration | 90×2 模型 | gpt-4o-mini ECE=0.18（過度自信） |
| E1 Error Analysis | 90 題 | 概念誤解和公式錯誤最多 |

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

### 跑 POC 實驗

```bash
# A5: 選項偏差
python -m experiments.A5_option_bias.run_experiment --dataset easy --limit 5 --model gpt-4o-mini

# I3: 雜訊敏感度
python -m experiments.I3_noise_red_herrings.run_experiment --dataset easy --limit 5 --model gpt-4o-mini --noise-types N1 N2 N3 N4

# A1: 開放式作答
python -m experiments.A1_open_ended.run_experiment --dataset easy --limit 5 --model gpt-4o-mini

# I1: 反事實測試
python -m experiments.I1_counterfactual.run_experiment --dataset easy --limit 5 --model gpt-4o-mini --perturbation-levels 1

# I2: 行為偏誤
python -m experiments.I2_behavioral_biases.run_experiment --bias-types loss_aversion anchoring --limit 5 --model gpt-4o-mini

# D4: 過度自信風險（需要 D1 結果）
python -m experiments.D4_overconfident_risk.run_experiment --input "experiments/D1_confidence_calibration/results/run_*/results.json" --confidence-threshold 0.8 --limit 5
```

### 輸出位置

每個實驗的結果存在 `experiments/XX/results/run_YYYYMMDD_HHMMSS/results.json`。

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

## 實驗流程說明

### 每個實驗的架構

```
experiments/XX_name/
├── __init__.py
├── config.py           # 實驗專屬常數、prompt 模板
├── run_experiment.py   # 主 CLI（argparse）
├── analysis.py         # 後處理分析
├── README.md           # 可讀指南 + 範例
└── results/            # JSON 輸出
```

### 共用模組 (`experiments/shared/`)

| 模組 | 功能 |
|------|------|
| `config.py` | `MODEL_REGISTRY`：所有支援模型的配置 |
| `llm_client.py` | `LLMClient`：OpenAI/Ollama 雙後端，含 retry |
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

## 關鍵發現

- 所有 CFA 資料集均非官方真題（SchweserNotes 來源，有 EMNLP 2025 論文背書）
- 最佳模型 (o4-mini) 在 CFA Level III 上準確率 79.1%，仍有 20%+ 錯誤率
- GPT-4o 在金融數學推理上僅 60.9%（vs 人類 92%），差距 31%
- gpt-4o-mini 在開放式作答時反而比 MCQ 表現更好（選項可能干擾）
- 近 30% 的錯誤是「高信心錯誤」——模型完全確信但答案錯誤

---

## 下一步

1. **放大樣本**：全部 CFA-Easy (1,032 題) + CFA-Challenge (90 題)
2. **多模型比較**：gpt-4o, gpt-4.1, claude-3.5-sonnet, qwen3:32b
3. **I2 補齊**：跑剩餘 4 種偏誤（framing, recency, disposition, overconfidence）
4. **D4 完整分類**：分類全部 74 筆高信心錯誤
5. **擴充 LLMClient**：支援 Anthropic/Google backend
6. **跨實驗整合**：將 A5 + A1 結合分析 MCQ vs Open-Ended 完整圖景

---

## 建議閱讀順序

1. **快速了解數據**：`docs/01-數據集完整手冊.md`
2. **了解研究現狀**：`docs/02-文獻綜述與研究定位.md`
3. **核心——研究方向**：`docs/03-研究方向深度設計.md` ★
4. **看精選論文提案**：`drafts/selected/README.md` ★
5. **技術參考**：`docs/04-FinDAP框架解析.md`
6. **論文防禦**：`docs/05-審稿人挑戰與應對策略.md`

---

## 授權

本專案僅供學術研究使用。CFA 相關資料來源為 SchweserNotes，非官方考題。
