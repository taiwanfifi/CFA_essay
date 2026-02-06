# 精選論文研究組合：7 篇可投稿

> **最後更新**：2026-02-06
> **狀態**：7 篇論文全部達到投稿水準，含編譯 PDF + 出版品質圖表 (14 張) + 完整實驗數據
> **作者**：程煒倫 (Wei-Lun Cheng)，台科大財金所博士班
> **主要指導教授**：Daniel Wei-Chung Miao (繆維中)
> **共同指導教授**：Guang-Di Chang (張光第)
> **單位**：Graduate Institute of Finance, National Taiwan University of Science and Technology (NTUST)

---

## 總覽

| # | 論文代號 | 論文標題 | 頁數 | 樣本量 | 數據規模 | 狀態 |
|---|---------|---------|------|--------|---------|------|
| 1 | **D1+D4** | When AI Is Confidently Wrong: Calibration and Risk Analysis of LLMs in Financial Decision-Making | 15pp | N=257 | **完整** (90Q × 3 configs) | **可投稿** |
| 2 | **I1+I3** | Stress Testing Financial LLMs: Counterfactual Perturbation and Noise Sensitivity Analysis on CFA Examinations | 17pp | N=100 | **完整** (100Q × 5 conditions) | **可投稿** |
| 3 | **A1+A5** | Beyond Multiple Choice: How Answer Options Inflate LLM Financial Reasoning Scores | 11pp | N=100 | **完整** (100Q paired design) | **可投稿** |
| 4 | **E1** | The CFA Error Atlas: Mapping Failure Modes of LLMs in Financial Reasoning | 11pp | N=229 errors | **完整** (全部錯誤分析) | **可投稿** |
| 5 | **D6** | Under Pressure: Adversarial Stress Testing of LLM Ethical Judgment in Financial Decision-Making | 9pp | N=47 | **完整** (47Q × 5 attacks) | **可投稿** |
| 6 | **G2** | The Certification Signal Erosion Hypothesis: A Modified Spence Model for AI-Disrupted Professional Credentialing | 24pp | 理論模型 | **純理論** (不需實驗) | **可投稿** |
| 7 | **I2** | Inherited Irrationality: Behavioral Finance Biases in LLM Financial Recommendations | 23pp | N=20 (5 bias types) | **完整** (5 偏誤類型) | **可投稿** |

### 合併邏輯

原始研究提案有 11 個（見下方檔案索引），其中 3 組合併成一篇、4 個獨立成篇，共 **7 篇論文**：

| 論文資料夾 | 合併了 | 為什麼合併 | 對應 `.md` 提案 |
|-----------|--------|-----------|----------------|
| `D1_calibration/` | D1 + D4 | D4 的數據就是從 D1 篩出來的高信心錯誤 | `D1-*.md` + `D4-*.md` |
| `I1_counterfactual/` | I1 + I3 | 都測「穩健性」：反事實微擾 + 雜訊注入 | `I1-*.md` + `I3-*.md` |
| `A1_open_ended/` | A1 + A5 | 同一研究問題的兩面：去選項 vs 有選項 | `A1-*.md` + `A5-*.md` |
| `E1_error_atlas/` | E1 獨立 | -- | `E1-*.md` |
| `D6_adversarial_ethics/` | D6 獨立 | -- | `D6-*.md` |
| `G2_signaling_theory/` | G2 獨立 | -- | `G2-*.md` |
| `I2_behavioral_biases/` | I2 獨立 | -- | `I2-*.md` |

> **注意**：被合併的 A5、D4、I3 不再有獨立資料夾，內容全部寫在合併後的論文中。
> H1 (Multimodal) 暫緩，缺 CFA 圖表資料，目前無資料夾。

### 數據規模分級說明

| 等級 | 定義 | 可發表性 |
|------|------|---------|
| **完整** | 樣本量足夠支撐統計檢定，結果穩健 | 可直接投稿 |
| **純理論** | 數學模型推導，無需實驗數據 | 可直接投稿 |

---

## 投稿優先序與策略

| 優先級 | 組合 | 目標期刊 | 理由 | 狀態 |
|--------|------|---------|------|------|
| **首選** | D1+D4 | Finance Research Letters (FRL) | 數據最完整、統計顯著、老師專長對口 | **可投稿** |
| **次選** | I1+I3 | Finance Research Letters (FRL) | 數據完整(n=100)、敏感度分析 | **可投稿** |
| 第三 | E1 | FRL / J. Financial Data Science | 229 筆錯誤、完整 taxonomy | **可投稿** |
| 第四 | G2 | FRL / J. Financial Economics | 純理論、Modified Spence Model | **可投稿** |
| 第五 | I2 | FRL / J. Behavioral and Experimental Finance | 5 種偏誤完整測試 | **可投稿** |
| 第六 | A1+A5 | FRL | N=100，McNemar p=0.045 顯著 | **可投稿** |
| 第七 | D6 | FRL / J. Financial Regulation | N=47，全 5 種攻擊均降低準確率 | **可投稿** |

---

## 各論文詳細狀態

---

### Paper 1: D1+D4 — 信心校準與過度自信風險

**Title**: *When AI Is Confidently Wrong: Calibration and Risk Analysis of Large Language Models in Financial Decision-Making*

**Target Journal**: Finance Research Letters (FRL), SSCI Q1

**Status**: PUBLICATION-READY — 15 pages

#### 中文摘要

- **論文題目**：當 AI 充滿自信地答錯：金融決策中大型語言模型的校準與風險分析
- **摘要**：本研究評估 LLM 在 CFA 考試上的信心校準品質。使用 90 題 CFA 挑戰級題目、2 個模型、2 種信心估計方法，產生 257 個觀測值。發現 LLM 系統性高估自身信心（過度自信差距 +22--32%），30% 的觀測值為「高信心錯誤」，且在錯誤答案中有 66.4% 伴隨高信心。提出 Confidence-at-Risk (CaR) 指標，類比金融風險管理的 VaR 概念，為金融 AI 監管提供量化框架。
- **實驗方法**：Verbalized confidence + self-consistency + logprob 三種信心估計方法，ECE 校準度量，one-sample t-test, binomial test, chi-squared test
- **主要結果**：過度自信差距 +22--32% (p<0.0001)；OC Error Rate 30.0% (p<0.0001)；錯誤答案中過度自信佔 66.4% (p=0.0002)；CFA 主題間校準顯著差異 (chi-squared p=0.030)
- **結論**：LLM 的過度自信是系統性的，非隨機現象。在 CFA Ethics 領域過度自信率最高 (43.5%)，Derivatives 最低 (22.2%)。建議金融 AI 部署應包含校準評估。

#### 核心結果

| 指標 | 數值 | 統計顯著性 |
|------|------|-----------|
| Overconfidence Gap | +22--32% | t=9.70, p<0.0001 |
| OC Error Rate | 30.0% (77/257) | z=3.99, p<0.0001 |
| OC Among Errors | 66.4% | z=3.53, p=0.0002 |
| Topic Variation | chi-squared=12.37 | p=0.030 |
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

- **來源**: D1 calibration experiment (90 CFA-Challenge questions x 3 model-method configurations)
- **觀測數**: 257 (部分 question x config 組合無效回應被排除)
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
├── main.tex                    # 完整論文 (15 pages)
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

**Status**: PUBLICATION-READY — 17 pages

#### 中文摘要

- **論文題目**：金融 LLM 壓力測試：CFA 考試上的反事實微擾與雜訊敏感度分析
- **摘要**：本研究提出雙維度壓力測試框架：(1) 反事實微擾——改變題目中的數值或條件來測試模型是否真正理解題意還是只在背答案；(2) 雜訊注入——加入無關資訊、誤導性干擾、冗餘上下文等 4 種雜訊類型。結果顯示，標準準確率 86% 在反事實微擾下降至 62.5%，記憶化差距高達 23.5 個百分點，約 28% 的正確答案疑似來自記憶而非推理。雜訊敏感度則相對溫和 (max NSI=0.046)。
- **實驗方法**：Counterfactual perturbation (Level 1 數值替換 + Level 2 條件改變)，Noise injection (N1-N4 四種雜訊)，McNemar's test，Noise Sensitivity Index
- **主要結果**：Original Accuracy 86.0% vs Level 1 Accuracy 62.5% (Memorization Gap +23.5%)；Robust Accuracy 58.0%；Memorization Suspect Rate 28.0%；雜訊敏感度溫和 (max NSI=0.046)
- **結論**：主要漏洞是記憶化依賴而非雜訊易感性。Robust Accuracy 58.0% 遠低於標準準確率 86.0%。

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
| Clean | 86.0% | -- | -- |
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
├── main.tex                    # 完整論文 (17 pages)
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

**Status**: PUBLICATION-READY — 11 pages, N=100

#### 中文摘要

- **論文題目**：超越選擇題：答案選項如何膨脹 LLM 金融推理分數
- **摘要**：本研究以 100 題 CFA 題目測試 GPT-4o-mini，揭示選擇題格式系統性高估 LLM 金融能力。有選項時準確率 85%，去掉選項後降至 73%，選項偏差 +12 個百分點（McNemar p=0.045，統計顯著）。進一步以三層評估框架（精確匹配 / 方向正確 / 真正錯誤）分析開放式作答，發現 28% 被二元評分判為「錯」的答案其實推理方向正確、只是用了不同的金融假設。
- **實驗方法**：Paired MCQ vs open-ended evaluation, McNemar's test, three-tier scoring (exact/directional/incorrect), LLM-as-judge, structured error attribution
- **主要結果**：Option Bias +12.0 pp (McNemar p=0.045, 顯著)；Biased Questions 21/100 (21%)；Strict Accuracy 34.0%, Lenient Accuracy 62.0%；Top error: conceptual_error 21/38 (55.3%)
- **結論**：MCQ 基準同時「太寬鬆」（選項漏洞灌水 12 pp）又「太嚴格」（28% 合理替代分析被判錯）。建議金融 LLM 評估從二元 MCQ 轉向開放式三層評分。

#### 核心結果 (N=100)

**A5 Option Bias**

| 指標 | 數值 |
|------|------|
| Accuracy WITH options | 85.0% |
| Accuracy WITHOUT options | 73.0% |
| Option Bias | **+12.0 pp** |
| Biased Questions | 21/100 (21%) |
| McNemar | b=21, c=9, chi-squared=4.033, **p=0.045** (SIGNIFICANT) |

**A1 Three-Tier Evaluation**

| 等級 | 數量 | 百分比 |
|------|------|--------|
| Level A (Exact Match) | 34 | 34.0% |
| Level B (Directional) | 28 | 28.0% |
| Level C (Incorrect) | 38 | 38.0% |
| Strict Accuracy | -- | 34.0% |
| Lenient Accuracy | -- | 62.0% |

**Error Attribution (Level C, N=38)**

| 錯誤類型 | 數量 | 百分比 |
|----------|------|--------|
| conceptual_error | 21 | 55.3% |
| 其他 | 17 | 44.7% |

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| A1 結果 (N=100) | `experiments/A1_open_ended/results/run_20260206_112613/results.json` |
| A5 結果 (N=100) | `experiments/A5_option_bias/results/run_20260206_112714/results.json` |
| A1 結果 (N=20) | `experiments/A1_open_ended/results/run_20260206_044146/results.json` |
| A5 結果 (N=20) | `experiments/A5_option_bias/results/run_20260206_044311/results.json` |
| A1 POC (N=5) | `experiments/A1_open_ended/results/run_20260205_010122/results.json` |
| A5 POC (N=5) | `experiments/A5_option_bias/results/run_20260204_045830/results.json` |

#### 論文檔案結構

```
drafts/selected/A1_open_ended/
├── main.tex                    # 完整論文 (11 pages)
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

**Status**: PUBLICATION-READY — 11 pages

#### 中文摘要

- **論文題目**：CFA 錯誤圖譜：大型語言模型金融推理失敗模式的系統性映射
- **摘要**：本研究對 229 個 LLM 錯誤答案進行系統性分類，建立三維錯誤分類法：8 種錯誤類型 x 8 個 CFA 主題 x 5 個認知階段。核心發現：推理前提錯誤佔 49.3%（模型從一開始就理解錯了）；計算錯誤僅佔 12.7%（「不會算」不是主要問題）；不同 CFA 主題有截然不同的錯誤模式——Ethics 87.1% 是推理類、Derivatives 37.5% 是計算類。
- **實驗方法**：GPT-4o-mini error classification across 5 reasoning methods (Zero-Shot, CoT, CoT+Verification, Self-Consistency, Combined)
- **主要結果**：Dominant Error: Reasoning Premise 49.3%；Calculation Errors 12.7%；Ethics Reasoning Errors 87.1%；Derivatives Calculation Errors 37.5%；Concept Identification Bottleneck 53.7%
- **結論**：LLM 的金融推理瓶頸在「概念識別」階段 (53.7%)，而非計算。針對性訓練應聚焦推理前提而非算術能力。

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

**三維 Taxonomy**: Error Type (8) x CFA Topic (8) x Cognitive Stage (5)

- 數據來源：D1 calibration 實驗中所有錯誤答案的 GPT-4o-mini 分類
- 229 筆錯誤已覆蓋所有 8 個 CFA 主題

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| 錯誤分析 (全部方法) | `experiments/E1_error_analysis/results/error_analysis_all_methods_20260203_230751.json` |
| 錯誤分析 (CoT) | `experiments/E1_error_analysis/results/error_analysis_cot_20260203_211957.json` |
| 原始 D1 數據 | `experiments/D1_confidence_calibration/results/run_20260202_034237/results.json` |

#### 論文檔案結構

```
drafts/selected/E1_error_atlas/
├── main.tex                    # 完整論文 (11 pages)
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

**Status**: PUBLICATION-READY — 9 pages, N=47

#### 中文摘要

- **論文題目**：在壓力下：LLM 金融倫理判斷的對抗式壓力測試
- **摘要**：本研究測試 LLM 在 5 種對抗性壓力（利潤誘因、權威施壓、情感操控、話術重構、道德困境）下能否維持正確的金融倫理判斷。以 47 題 CFA Ethics 題目測試 GPT-4o-mini，發現所有 5 種壓力都會降低準確率（無一例外），其中利潤誘因和權威施壓最為有效（ERS=0.925，-6.4 pp），共有 14 題在壓力下「翻轉」。
- **實驗方法**：5 adversarial pressure types x 47 CFA Ethics questions, Ethics Robustness Score (ERS), flip analysis
- **主要結果**：Standard 85.1%；所有 5 種攻擊均降低準確率；Profit incentive & Authority pressure 最有效 (ERS=0.925, -6.4 pp)；14 題在壓力下翻轉
- **結論**：LLM 學到的是倫理回應的「形式」而非「原則」，所有壓力類型都能突破其倫理判斷。建議金融 AI 部署前應通過 ERS >= 0.95 的門檻測試。

#### 核心結果 (N=47 CFA Ethics questions)

| 壓力類型 | Accuracy | Flipped | ERS |
|----------|----------|---------|-----|
| Standard (baseline) | 85.1% | -- | 1.000 |
| Profit incentive | 78.7% | 4 | 0.925 |
| Authority pressure | 78.7% | 3 | 0.925 |
| Emotional manipulation | 80.8% | 2 | 0.950 |
| Reframing | 80.8% | 3 | 0.950 |
| Moral dilemma | 80.8% | 2 | 0.950 |

**關鍵發現**:
- **所有 5 種攻擊均降低準確率**，無一出現矛盾性改善
- 最有效攻擊：Profit incentive 和 Authority pressure (ERS=0.925, -6.4 pp)
- 共 14 題在壓力下翻轉（部分題目被多種壓力翻轉）
- 整體 Ethics Robustness Score 範圍：0.925--0.950

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| D6 完整結果 (N=47) | `experiments/D6_adversarial_ethics/results/run_20260206_112341/results.json` |
| D6 初步結果 (N=15) | `experiments/D6_adversarial_ethics/results/run_20260206_051053/results.json` |

#### 論文檔案結構

```
drafts/selected/D6_adversarial_ethics/
├── main.tex                    # 完整論文 (9 pages)
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

**Status**: PUBLICATION-READY — 24 pages, 純理論論文

#### 中文摘要

- **論文題目**：認證訊號侵蝕假說：AI 衝擊下專業認證的修正 Spence 模型
- **摘要**：本研究以 Spence (1973) 訊號理論為基礎，建立 AI 衝擊下專業認證價值侵蝕的數學模型。提出六維能力分類法（量化分析、概念理解、倫理判斷、溝通、策略思考、經驗直覺），發現 AI 已能複製約 50% 的 CFA 認證能力，導致 CFA 認證的訊號保留率降至 28.8%——即超過 70% 的認證訊號價值已被侵蝕。
- **實驗方法**：Modified Spence signaling model, multi-dimensional ability space, AI replicability mapping, equilibrium analysis with 2 propositions and 2 corollaries
- **主要結果**：CFA Signaling Retention Ratio (R) = 0.288；AI-replicable abilities: 50% already replicable；Six-Dimensional Ability Taxonomy
- **結論**：CFA 認證正在「部分訊號瓦解」的均衡中。認證機構應重新設計考試以強調 AI 難以複製的能力維度（策略思考、經驗直覺、溝通）。

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
├── main.tex                    # 完整論文 (24 pages)
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

**Status**: PUBLICATION-READY — 23 pages, 5 種偏誤類型完整測試

#### 中文摘要

- **論文題目**：遺傳的非理性：大型語言模型金融建議中的行為金融學偏誤
- **摘要**：本研究設計 20 個金融決策情境（涵蓋 5 種經典行為偏誤），測試 GPT-4o-mini 是否「繼承」了人類的非理性偏誤。發現 LLM 在誘導性情境下平均偏誤分數 0.525（0=完全理性, 1=完全偏誤），中性重構後降至 0.350（Wilcoxon p=0.012）。偏誤的可去除程度呈現清晰層級：損失趨避最易去偏 (+0.400)，近因偏誤和處置效應完全抵抗去偏 (0.000)。
- **實驗方法**：20 paired scenarios (bias-inducing + neutral), 5 bias types, LLM-as-judge scoring (0/0.5/1), Wilcoxon signed-rank test
- **主要結果**：Overall Bias Score: inducing 0.525 vs neutral 0.350 (Wilcoxon p=0.012)；Loss aversion debiasing +0.400；Recency & Disposition Effect debiasing 0.000
- **結論**：LLM 確實「繼承」了行為偏誤，但不同偏誤的來源機制不同——損失趨避來自表面語言（可去偏），近因偏誤來自訓練數據結構（不可去偏）。

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
├── main.tex                    # 完整論文 (23 pages)
├── main.pdf                    # 編譯 PDF
├── theory_framework.md         # 理論框架
├── STATUS.md                   # 狀態追蹤
├── figures/                    # 圖表
├── tables/                     # 表格
└── submission/                 # 投稿資料
```

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

# A1: 開放式作答 (N=100)
python -m experiments.A1_open_ended.run_experiment --dataset easy --limit 100 --model gpt-4o-mini

# A5: 選項偏差 (N=100)
python -m experiments.A5_option_bias.run_experiment --dataset easy --limit 100 --model gpt-4o-mini

# I2: 行為偏誤 (5 種)
python -m experiments.I2_behavioral_biases.run_experiment --bias-types loss_aversion anchoring framing recency disposition_effect --limit 5 --model gpt-4o-mini

# D6: 對抗式道德測試 (N=47)
python -m experiments.D6_adversarial_ethics.run_experiment --dataset easy --limit 47 --model gpt-4o-mini

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
| A1 Open-Ended | 2026-02-06 | **100** | `experiments/A1_open_ended/results/run_20260206_112613/` | A1+A5 |
| A5 Option Bias | 2026-02-06 | **100** | `experiments/A5_option_bias/results/run_20260206_112714/` | A1+A5 |
| I1 Counterfactual | 2026-02-06 | 100 | `experiments/I1_counterfactual/results/run_20260206_053445/` | I1+I3 |
| I3 Noise | 2026-02-06 | 100 | `experiments/I3_noise_red_herrings/results/run_20260206_054039/` | I1+I3 |
| I2 Biases | 2026-02-06 | 20 | `experiments/I2_behavioral_biases/results/run_20260206_052135/` | I2 |
| D6 Ethics | 2026-02-06 | **47** | `experiments/D6_adversarial_ethics/results/run_20260206_112341/` | D6 |

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

**出版品質圖表**: 7 篇論文共含 14 張出版品質圖表 (PDF 格式)。

---

## 下一步行動

### 全部 7 篇可投稿

1. **D1+D4** (15pp): 數據完整、統計顯著 -- 直接投 FRL
2. **I1+I3** (17pp): N=100 完整數據 -- 直接投 FRL
3. **A1+A5** (11pp): N=100, McNemar p=0.045 顯著 -- 直接投 FRL
4. **E1** (11pp): 229 筆錯誤完整分析 -- 直接投 FRL / JFDS
5. **D6** (9pp): N=47, 全 5 種攻擊均降低準確率 -- 直接投 FRL / JFR
6. **G2** (24pp): 純理論 -- 直接投 FRL / JFE
7. **I2** (23pp): 5 種偏誤完整測試 -- 直接投 FRL / JBEF

### 跨論文強化

- [ ] 多模型驗證：加入 gpt-4o, claude-3.5-sonnet, qwen3:32b 比較
- [ ] 交叉引用：各論文互相引用，形成研究群 (research cluster)

---

## 指導教授

### 主要指導教授：繆維中老師 (Daniel Wei-Chung Miao)

- **背景**：財務數學、風險管理、統計方法
- **偏好**：Economic Significance > NLP 指標；重視風險分析、敏感度分析、穩健性
- **最對口論文**: D1+D4 (校準+風險) -> I1+I3 (壓力測試+穩健性)

### 共同指導教授：張光第老師 (Guang-Di Chang)

---

## 檔案索引

### 研究提案 -> 論文對應

| 提案 `.md` | 說明 | 歸屬論文 |
|-----------|------|---------|
| `A1-open-ended-numerical.md` | 開放式數值推理 | -> `A1_open_ended/` |
| `A5-mcq-option-bias.md` | 選項偏差量化 | -> `A1_open_ended/` (合併) |
| `D1-calibration-selective-prediction.md` | 信心校準 | -> `D1_calibration/` |
| `D4-overconfident-ai-regulation.md` | 過度自信風險 | -> `D1_calibration/` (合併) |
| `D6-adversarial-ethics-jailbreak.md` | 對抗式道德測試 | -> `D6_adversarial_ethics/` |
| `E1-error-pattern-atlas.md` | 錯誤圖譜 | -> `E1_error_atlas/` |
| `G2-signaling-theory.md` | 訊號理論 | -> `G2_signaling_theory/` |
| `H1-multimodal-financial-reasoning.md` | 多模態金融推理 | 暫緩 |
| `I1-counterfactual-stress-test.md` | 反事實壓力測試 | -> `I1_counterfactual/` |
| `I2-behavioral-biases-llm.md` | 行為金融學偏誤 | -> `I2_behavioral_biases/` |
| `I3-noise-red-herrings.md` | 雜訊與紅鯡魚 | -> `I1_counterfactual/` (合併) |

### 論文資料夾結構（每個都相同）

```
XX_name/
├── main.tex              # LaTeX 論文主文件
├── main.pdf              # 編譯 PDF
├── theory_framework.md   # 理論框架與假說
├── run_analysis.py       # 數據分析腳本 (部分論文有)
├── analysis_results.json # 分析結果 (部分論文有)
├── STATUS.md             # 完成度檢查表
├── figures/              # 圖表 (PDF + PNG)
├── tables/               # LaTeX 表格原始碼
└── submission/           # 投稿信等
```

---

## 聯絡資訊

**程煒倫 (Wei-Lun Cheng)**
博士班研究生，Graduate Institute of Finance, NTUST (台科大財金所)
主要指導教授：Daniel Wei-Chung Miao (繆維中)
共同指導教授：Guang-Di Chang (張光第)
