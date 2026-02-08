# 精選論文研究組合：7 篇可投稿

> **最後更新**：2026-02-08
> **狀態**：7 篇論文全部達到投稿水準，含編譯 PDF + 出版品質圖表 (24 張) + 完整實驗數據 + GPT-5-mini 跨模型驗證
> **作者**：程煒倫 (Wei-Lun Cheng)，台科大財金所博士班
> **主要指導教授**：Daniel Wei-Chung Miao (繆維中)
> **共同指導教授**：Guang-Di Chang (張光第)
> **單位**：Graduate Institute of Finance, National Taiwan University of Science and Technology (NTUST)

---

## 總覽

| # | 論文代號 | 論文標題 | 字數 | 樣本量 | 模型 | 狀態 |
|---|---------|---------|------|--------|------|------|
| P1 | **A1+A5** | Beyond Multiple Choice: How Answer Options Inflate LLM Financial Reasoning Scores | 3,719 | N=1,032 | GPT-4o-mini + GPT-5-mini | **可投稿** |
| P2 | **I1+I3** | Stress Testing Financial LLMs: Counterfactual Perturbation and Noise Sensitivity Analysis on CFA Examinations | 4,367 | N=1,032 | GPT-4o-mini + GPT-5-mini | **可投稿** |
| P3 | **I2** | Inherited Irrationality: Behavioral Finance Biases in LLM Financial Recommendations | 3,395 | N=60 | GPT-4o-mini only | **可投稿** |
| P4 | **D6** | Under Pressure: Adversarial Stress Testing of LLM Ethical Judgment in Financial Decision-Making | 3,536 | N=47 | GPT-4o-mini + GPT-5-mini | **可投稿** |
| P5 | **E1** | The CFA Error Atlas: Mapping Failure Modes of LLMs in Financial Reasoning | 2,627 | N=557 errors | GPT-4o-mini + GPT-5-mini (GCI) | **可投稿** |
| P6 | **D1+D4** | When AI Is Confidently Wrong: Calibration and Risk Analysis of LLMs in Financial Decision-Making | 3,463 | N=257 | GPT-4o-mini + qwen3:32b | **可投稿** |
| P7 | **G2** | The Certification Signal Erosion Hypothesis: A Modified Spence Model for AI-Disrupted Professional Credentialing | 4,231 | 理論+A5 data | 理論模型 + A5 實證數據 | **可投稿** |

### 合併邏輯

| 論文資料夾 | 合併了 | 為什麼合併 |
|-----------|--------|-----------|
| `A1_open_ended/` | A1 + A5 | 同一研究問題的兩面：去選項 vs 有選項 |
| `I1_counterfactual/` | I1 + I3 | 都測「穩健性」：反事實微擾 + 雜訊注入 |
| `I2_behavioral_biases/` | I2 獨立 | -- |
| `D6_adversarial_ethics/` | D6 獨立 | -- |
| `E1_error_atlas/` | E1 獨立 | -- |
| `D1_calibration/` | D1 + D4 | D4 的數據就是從 D1 篩出來的高信心錯誤 |
| `G2_signaling_theory/` | G2 獨立 | -- |

> **注意**：被合併的 A5、D4、I3 不再有獨立資料夾，內容全部寫在合併後的論文中。

---

## 投稿優先序與策略

| 優先級 | 組合 | 目標期刊 | 理由 | 狀態 |
|--------|------|---------|------|------|
| **首選** | P2: I1+I3 | Finance Research Letters (FRL) | N=1,032 全量 + GPT-5-mini 跨模型 + Memorization Paradox 新發現 | **可投稿** |
| **次選** | P1: A1+A5 | Finance Research Letters (FRL) | N=1,032 + GPT-5-mini p<0.001*** 高度顯著 + 模型依賴性發現 | **可投稿** |
| 第三 | P6: D1+D4 | Finance Research Letters (FRL) | 數據最完整、統計顯著、四大假說全部成立 | **可投稿** |
| 第四 | P5: E1 | FRL / J. Financial Data Science | 557 筆錯誤 + 跨模型 GCI + 完整 taxonomy | **可投稿** |
| 第五 | P4: D6 | FRL / J. Financial Regulation | GPT-5-mini ZERO flips 對比 + ERS>1.0 新發現 | **可投稿** |
| 第六 | P7: G2 | FRL / J. Financial Economics | 純理論 + A5 實證支持 + Signal Retention Ratio | **可投稿** |
| 第七 | P3: I2 | FRL / J. Behavioral and Experimental Finance | 6 種偏誤 + 三層去偏階層 + Wilcoxon p=0.023 | **可投稿** |

---

## 各論文詳細狀態

---

### Paper 1 (P1): A1+A5 — 開放式作答與選項偏差

**Title**: *Beyond Multiple Choice: How Answer Options Inflate LLM Financial Reasoning Scores*

**Target Journal**: Finance Research Letters (FRL), SSCI Q1

**Status**: PUBLICATION-READY — 3,719 words, N=1,032 (full CFA-Easy corpus)

**Folder**: `A1_open_ended/`

#### 中文摘要

- **論文題目**：超越選擇題：答案選項如何膨脹 LLM 金融推理分數
- **摘要**：本研究以 1,032 題完整 CFA-Easy 語料庫，比較 GPT-4o-mini 和 GPT-5-mini 在有選項與無選項條件下的表現。核心發現：選項偏差是模型依賴的——GPT-4o-mini 僅 +1.9pp (McNemar p=0.251, n.s.)，但 GPT-5-mini 高達 +9.6pp (p<0.001***)。三層評估框架 (Level A/B/C) 揭示 GPT-5-mini 在 Level A 精確匹配率從 24.5% 提升至 41.8%，同時 Level C 錯誤從 54.0% 降至 35.9%。
- **實驗方法**：Paired MCQ vs open-ended evaluation, McNemar's test (Yates' correction), three-tier scoring, cross-model comparison
- **主要結果**：GPT-4o-mini option bias +1.9pp (n.s.); GPT-5-mini option bias +9.6pp (p<0.001***); Model-dependent bias discovery
- **結論**：選項偏差不是固定常數而是模型依賴性質。能力越強的模型反而越依賴選項提示，挑戰了「能力越強越穩健」的直覺假設。

#### 核心結果 (N=1,032)

**A5 Option Bias — Cross-Model Comparison**

| 指標 | GPT-4o-mini | GPT-5-mini |
|------|-------------|------------|
| Accuracy WITH options | 82.6% (852/1032) | 92.8% |
| Accuracy WITHOUT options | 80.6% (832/1032) | 83.2% |
| Option Bias | +1.9pp | **+9.6pp** |
| McNemar p-value | p=0.251 (n.s.) | **p<0.001***  |

**A1 Three-Tier Evaluation — Cross-Model Comparison**

| 等級 | GPT-4o-mini | GPT-5-mini |
|------|-------------|------------|
| Level A (Exact Match) | 24.5% | 41.8% |
| Level B (Directional) | 21.5% | 22.3% |
| Level C (Incorrect) | 54.0% | 35.9% |

**Key Finding**: Option bias is model-dependent (n.s. for 4o-mini, p<0.001 for 5-mini)

#### 圖表 (4 張)

- `fig1_option_bias` — GPT-4o-mini option bias bar chart
- `fig2_three_tier_evaluation` — GPT-4o-mini three-tier distribution
- `fig3_cross_model_option_bias` — Cross-model option bias comparison
- `fig4_cross_model_three_tier` — Cross-model three-tier comparison

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| GPT-4o-mini A5 (N=1,032) | `experiments/A5_option_bias/results/run_20260206_171904/` |
| GPT-4o-mini A1 (N=1,032) | `experiments/A1_open_ended/results/run_20260206_112613/` |
| GPT-5-mini A5 (N=1,032) | `experiments/A5_option_bias/results/run_20260207_174114/` |
| GPT-5-mini A1 (N=1,032) | `experiments/A1_open_ended/results/run_20260207_174118/` |

#### 論文檔案結構

```
drafts/selected/A1_open_ended/
├── main.tex                    # 完整論文 (3,719 words)
├── main.pdf                    # 編譯 PDF
├── figures/
│   ├── fig1_option_bias.pdf
│   ├── fig2_three_tier_evaluation.pdf
│   ├── fig3_cross_model_option_bias.pdf
│   └── fig4_cross_model_three_tier.pdf
└── submission/
```

---

### Paper 2 (P2): I1+I3 — 反事實壓力測試與雜訊敏感度

**Title**: *Stress Testing Financial LLMs: Counterfactual Perturbation and Noise Sensitivity Analysis on CFA Examinations*

**Target Journal**: Finance Research Letters (FRL), SSCI Q1

**Status**: PUBLICATION-READY — 4,367 words, N=1,032

**Folder**: `I1_counterfactual/`

#### 中文摘要

- **論文題目**：金融 LLM 壓力測試：CFA 考試上的反事實微擾與雜訊敏感度分析
- **摘要**：本研究提出雙維度壓力測試框架，以 1,032 題完整 CFA-Easy 語料庫測試 GPT-4o-mini 和 GPT-5-mini。核心發現「記憶化悖論」(Memorization Paradox)：GPT-5-mini 標準準確率從 82.4% 提升至 91.8%，但反事實微擾下降至 55.3%，記憶化差距從 18.6pp 暴增至 36.4pp——能力越強，記憶化依賴越深。雜訊敏感度則相對溫和，N4 contradictory hints 反而提升準確率。
- **實驗方法**：Counterfactual perturbation (Level 1 數值替換), Noise injection (N1-N4 四種雜訊), McNemar's test (Yates' correction), Noise Sensitivity Index, cross-model comparison
- **主要結果**：GPT-4o-mini mem_gap=18.6pp; GPT-5-mini mem_gap=36.4pp (Memorization Paradox); N4 contradictory hints 反向提升準確率
- **結論**：模型能力提升不等於理解力提升。記憶化悖論暗示更強的 LLM 可能更依賴訓練數據的表面匹配。

#### 核心結果 (N=1,032)

**I1 Counterfactual Perturbation — Cross-Model**

| 指標 | GPT-4o-mini | GPT-5-mini |
|------|-------------|------------|
| Original Accuracy | 82.4% | 91.8% |
| Level 1 Accuracy | 63.8% (n=702) | 55.3% (n=638) |
| Memorization Gap | 18.6pp | **36.4pp** |
| Robust Accuracy | 63.5% | -- |
| Memorization Suspect Rate | 18.9% | -- |

**I3 Noise Sensitivity — GPT-4o-mini (N=1,032)**

| 雜訊類型 | Accuracy | NSI |
|----------|----------|-----|
| Clean | 81.6% | -- |
| N1 (irrelevant data) | 79.0% | 0.032 |
| N2 (plausible distractor) | 80.3% | 0.015 |
| N3 (verbose context) | 82.0% | -0.005 |
| N4 (contradictory hint) | 87.5% | -0.072 |

**I3 Noise Sensitivity — GPT-5-mini (N=1,032)**

| 雜訊類型 | Accuracy | NSI |
|----------|----------|-----|
| Clean | 92.3% | -- |
| N1 (irrelevant data) | 90.8% | 0.017 |
| N2 (plausible distractor) | 91.0% | 0.015 |
| N3 (verbose context) | 92.4% | -0.001 |
| N4 (contradictory hint) | 96.1% | -0.041 |

**關鍵發現 — Memorization Paradox**:
- GPT-5-mini 標準準確率比 GPT-4o-mini 高 +9.4pp，但記憶化差距反而暴增 +17.8pp
- N4 contradictory hints 在兩個模型上都反向提升準確率（hints 名指錯誤答案，模型反而避開）
- I1 baseline (82.4%) 與 I3 baseline (81.6%) 來自不同 run，略有差異

#### 圖表 (4 張)

- `fig1_accuracy_degradation` — Counterfactual accuracy degradation
- `fig2_noise_sensitivity` — Noise sensitivity radar chart
- `fig3_stress_test_framework` — Dual-dimension stress test framework
- `fig4_memorization_paradox` — Cross-model memorization paradox

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| GPT-4o-mini I1 (N=1,032) | `experiments/I1_counterfactual/results/run_20260206_170129/` |
| GPT-4o-mini I3 (N=1,032) | `experiments/I3_noise_red_herrings/results/run_20260206_203913/` |
| GPT-5-mini I1 (N=1,032) | `experiments/I1_counterfactual/results/run_20260207_174116/` |
| GPT-5-mini I3 (N=1,032) | `experiments/I3_noise_red_herrings/results/run_20260207_174115/` |

#### 論文檔案結構

```
drafts/selected/I1_counterfactual/
├── main.tex                    # 完整論文 (4,367 words)
├── main.pdf                    # 編譯 PDF
├── figures/
│   ├── fig1_accuracy_degradation.pdf
│   ├── fig2_noise_sensitivity.pdf
│   ├── fig3_stress_test_framework.pdf
│   └── fig4_memorization_paradox.pdf
└── submission/
```

---

### Paper 3 (P3): I2 — 行為金融學偏誤

**Title**: *Inherited Irrationality: Behavioral Finance Biases in Large Language Model Financial Recommendations*

**Target Journal**: Finance Research Letters / J. Behavioral and Experimental Finance

**Status**: PUBLICATION-READY — 3,395 words, N=60 (6 bias types x 10), GPT-4o-mini only

**Folder**: `I2_behavioral_biases/`

#### 中文摘要

- **論文題目**：遺傳的非理性：大型語言模型金融建議中的行為金融學偏誤
- **摘要**：本研究設計 60 個金融決策情境（涵蓋 6 種經典行為偏誤），測試 GPT-4o-mini 是否「繼承」了人類的非理性偏誤。發現 LLM 在誘導性情境下平均偏誤分數 0.500，中性重構後降至 0.425（Wilcoxon W=14.0, p=0.023, r=0.284）。偏誤的可去除程度呈現三層階層結構。
- **注意**：GPT-5-mini 因 80% 空白回應（數據品質不可靠）而從本研究移除，僅保留 GPT-4o-mini 作為單模型研究。
- **實驗方法**：60 paired scenarios (bias-inducing + neutral), 6 bias types x 10 each, LLM-as-judge scoring (0/0.5/1), Wilcoxon signed-rank test
- **主要結果**：Mean bias: inducing=0.500, neutral=0.425, debiasing=+0.075; Wilcoxon W=14.0, p=0.023, r=0.284
- **結論**：LLM 確實「繼承」了行為偏誤，呈現三層去偏階層。

#### 核心結果 (N=60, GPT-4o-mini)

| 偏誤類型 | N | Bias Score (inducing) | Neutral Score | Debiasing Effect |
|----------|---|----------------------|---------------|-----------------|
| Loss Aversion | 10 | 0.600 | 0.300 | **+0.300** |
| Anchoring | 10 | 0.400 | 0.350 | +0.050 |
| Framing | 10 | 0.500 | 0.350 | **+0.150** |
| Recency | 10 | 0.500 | 0.550 | -0.050 |
| Disposition Effect | 10 | 0.500 | 0.500 | 0.000 |
| Overconfidence | 10 | 0.500 | 0.500 | 0.000 |
| **Overall** | **60** | **0.500** | **0.425** | **+0.075** |

**三層去偏階層 (Bias Persistence Hierarchy)**:
- **表面偏誤** (Surface)：Loss Aversion (+0.300), Framing (+0.150) — 改措辭就能去偏
- **弱反應偏誤** (Weak)：Anchoring (+0.050) — 微弱反應
- **深層偏誤** (Deep)：Disposition (0.000), Overconfidence (0.000), Recency (-0.050) — 完全抵抗去偏

Wilcoxon signed-rank test: W=14.0, **p=0.023**, effect size r=0.284

#### 圖表 (2 張)

- `fig1_bias_score_comparison` — Bias score comparison bar chart
- `fig2_debiasing_effect` — Debiasing effect by bias type

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| I2 完整結果 (N=60, 6 types) | `experiments/I2_behavioral_biases/results/run_20260206_140527/` |

#### 論文檔案結構

```
drafts/selected/I2_behavioral_biases/
├── main.tex                    # 完整論文 (3,395 words)
├── main.pdf                    # 編譯 PDF
├── figures/
│   ├── fig1_bias_score_comparison.pdf
│   └── fig2_debiasing_effect.pdf
└── submission/
```

---

### Paper 4 (P4): D6 — 對抗式金融道德測試

**Title**: *Under Pressure: Adversarial Stress Testing of LLM Ethical Judgment in Financial Decision-Making*

**Target Journal**: Finance Research Letters / J. Financial Regulation

**Status**: PUBLICATION-READY — 3,536 words, N=47 (CFA Ethics subset)

**Folder**: `D6_adversarial_ethics/`

#### 中文摘要

- **論文題目**：在壓力下：LLM 金融倫理判斷的對抗式壓力測試
- **摘要**：本研究測試 GPT-4o-mini 和 GPT-5-mini 在 5 種對抗性壓力下能否維持正確的金融倫理判斷。GPT-4o-mini 標準 85.1%，14 題在壓力下翻轉；GPT-5-mini 標準 91.5%，零翻轉且 ERS 全部 >1.0（對抗壓力反而提升表現）。跨模型對比揭示倫理穩健性存在質的飛躍。
- **實驗方法**：5 adversarial pressure types x 47 CFA Ethics questions, Ethics Robustness Score (ERS), flip analysis, cross-model comparison
- **主要結果**：GPT-4o-mini: 14 flips, ERS=0.925-0.950; GPT-5-mini: ZERO flips, all ERS>1.0
- **結論**：GPT-5-mini 展現質的倫理穩健性飛躍——對抗壓力不僅無法動搖其判斷，反而觸發更深入思考。

#### 核心結果 (N=47)

**GPT-4o-mini**

| 壓力類型 | Accuracy | Flipped | ERS |
|----------|----------|---------|-----|
| Standard (baseline) | 85.1% | -- | 1.000 |
| Profit incentive | 78.7% | 4 | 0.925 |
| Authority pressure | 78.7% | 3 | 0.925 |
| Emotional manipulation | 80.9% | 2 | 0.950 |
| Reframing | 80.9% | 3 | 0.950 |
| Moral dilemma | 80.9% | 2 | 0.950 |

**GPT-5-mini**

| 壓力類型 | Accuracy | Flipped | ERS |
|----------|----------|---------|-----|
| Standard (baseline) | 91.5% | -- | 1.000 |
| All 5 pressure types | -- | **ZERO** | **1.047-1.070** |

**關鍵發現**:
- GPT-4o-mini: 所有 5 種攻擊均降低準確率，profit/authority 最有效 (ERS=0.925)
- GPT-5-mini: 零翻轉，ERS 全部 >1.0——對抗壓力反而**提升**準確率
- 跨模型差異代表倫理推理的質的飛躍

#### 圖表 (2 張)

- `fig1_ethics_robustness` — Ethics Robustness Score comparison
- `fig2_ethics_accuracy` — Cross-model accuracy under pressure

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| GPT-4o-mini D6 (N=47) | `experiments/D6_adversarial_ethics/results/run_20260206_112341/` |
| GPT-5-mini D6 (N=47) | `experiments/D6_adversarial_ethics/results/run_20260207_023637/` |

#### 論文檔案結構

```
drafts/selected/D6_adversarial_ethics/
├── main.tex                    # 完整論文 (3,536 words)
├── main.pdf                    # 編譯 PDF
├── figures/
│   ├── fig1_ethics_robustness.pdf
│   └── fig2_ethics_accuracy.pdf
└── submission/
```

---

### Paper 5 (P5): E1 — 錯誤圖譜

**Title**: *The CFA Error Atlas: Mapping Failure Modes of Large Language Models in Financial Reasoning*

**Target Journal**: Finance Research Letters / J. Financial Data Science

**Status**: PUBLICATION-READY — 2,627 words, N=557 errors (from full-scale A1 run)

**Folder**: `E1_error_atlas/`

#### 中文摘要

- **論文題目**：CFA 錯誤圖譜：大型語言模型金融推理失敗模式的系統性映射
- **摘要**：本研究對 557 個 LLM 錯誤答案（來自完整 N=1,032 A1 開放式作答實驗）進行系統性分類，建立三維錯誤分類法：8 種錯誤類型 x 10 個 CFA 主題 x 5 個認知階段。核心發現：推理前提錯誤佔 46.0%，概念識別階段佔 50.3%。Golden Context Injection (GCI) 實驗顯示 GPT-4o-mini 恢復率 82.4%，GPT-5-mini 恢復率 88.3%（full recovery 從 25.5% 躍升至 50.4%）。
- **實驗方法**：GPT-4o-mini error classification, three-dimensional taxonomy (8 types x 10 topics x 5 stages), Golden Context Injection (GCI), cross-model GCI comparison
- **主要結果**：Dominant Error: Reasoning Premise 46.0%; Concept Identification stage 50.3%; GCI recovery: 82.4% (4o-mini), 88.3% (5-mini)
- **結論**：LLM 的金融推理瓶頸在「概念識別」階段，而非計算。GCI 跨模型比較顯示更強的模型能更好地利用補充知識。

#### 核心結果 (N=557 errors)

| 指標 | 數值 |
|------|------|
| Total Errors Analyzed | 557 |
| Error Types | 8 categories |
| CFA Topics | 10 topics |
| Cognitive Stages | 5 stages |
| Dominant Error | Reasoning Premise (46.0%) |
| Concept Identification Bottleneck | 50.3% |

**GCI Recovery — Cross-Model**

| 指標 | GPT-4o-mini | GPT-5-mini |
|------|-------------|------------|
| Total Recovery Rate | 82.4% | 88.3% |
| Full Recovery | 25.5% | 50.4% |
| Partial Recovery | 56.9% | 37.9% |
| No Recovery | 17.6% | 11.7% |

#### 圖表 (5 張)

- `fig1_error_type_distribution` — Error type distribution
- `fig2_topic_error_profile` — Topic-specific error profiles
- `fig3_cognitive_stages` — Cognitive stage bottleneck analysis
- `fig4_gci_recovery` — GCI recovery rates (GPT-4o-mini)
- `fig5_cross_model_gci` — Cross-model GCI comparison

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| 錯誤分析 (全部方法) | `experiments/E1_error_analysis/results/error_analysis_all_methods_20260203_230751.json` |
| GCI GPT-4o-mini (N=557) | `experiments/E1_error_analysis/results/golden_context_gpt-4o-mini_20260207_032341.json` |
| GCI GPT-5-mini (N=557) | `experiments/E1_error_analysis/results/golden_context_gpt-5-mini_20260207_220440.json` |

#### 論文檔案結構

```
drafts/selected/E1_error_atlas/
├── main.tex                    # 完整論文 (2,627 words)
├── main.pdf                    # 編譯 PDF
├── STATUS.md                   # 詳細完成度檢查表
├── figures/
│   ├── fig1_error_type_distribution.pdf
│   ├── fig2_topic_error_profile.pdf
│   ├── fig3_cognitive_stages.pdf
│   ├── fig4_gci_recovery.pdf
│   └── fig5_cross_model_gci.pdf
└── submission/
```

---

### Paper 6 (P6): D1+D4 — 信心校準與過度自信風險

**Title**: *When AI Is Confidently Wrong: Calibration and Risk Analysis of Large Language Models in Financial Decision-Making*

**Target Journal**: Finance Research Letters (FRL), SSCI Q1

**Status**: PUBLICATION-READY — 3,463 words, N=257 (90 CFA-Challenge x 3 configs)

**Folder**: `D1_calibration/`

#### 中文摘要

- **論文題目**：當 AI 充滿自信地答錯：金融決策中大型語言模型的校準與風險分析
- **摘要**：本研究評估 LLM 在 CFA 考試上的信心校準品質。使用 90 題 CFA 挑戰級題目、2 個模型、2 種信心估計方法，產生 257 個觀測值。發現 LLM 系統性高估自身信心（過度自信差距 +22-32%），30% 的觀測值為「高信心錯誤」，且在錯誤答案中有 66.4% 伴隨高信心。提出 Confidence-at-Risk (CaR) 指標，為金融 AI 監管提供量化框架。
- **注意**：無 GPT-5-mini 實驗（D1 需要 logprob，GPT-5-mini 不支援）。
- **實驗方法**：Verbalized confidence + self-consistency + logprob 三種信心估計方法，ECE 校準度量，one-sample t-test, binomial test, chi-squared test
- **主要結果**：過度自信差距 +22-32% (p<0.0001)；OC Error Rate 30.0% (p<0.0001)；錯誤答案中過度自信佔 66.4% (p=0.0002)；CFA 主題間校準顯著差異 (chi-squared p=0.030)
- **結論**：LLM 的過度自信是系統性的，非隨機現象。建議金融 AI 部署應包含校準評估。

#### 核心結果

| 指標 | 數值 | 統計顯著性 |
|------|------|-----------|
| Overconfidence Gap | +22-32% | t=9.70, p<0.0001 |
| OC Error Rate | 30.0% (77/257) | z=3.99, p<0.0001 |
| OC Among Errors | 66.4% | z=3.53, p=0.0002 |
| Topic Variation | chi-squared=12.37 | p=0.030 |
| Best ECE | qwen3:32b = 0.247 | |
| Worst ECE | gpt-4o-mini verbalized = 0.315 | |

#### 四大假說全部顯著

| 假說 | 內容 | 結果 |
|------|------|------|
| H1 | LLM 系統性高估自身信心 | Supported (p<0.0001) |
| H2 | 過度自信錯誤佔比超過 25% | Supported (30.0%, p<0.0001) |
| H3 | 錯誤答案中過度自信佔主導 | Supported (66.4%, p=0.0002) |
| H4 | 校準品質因 CFA 主題而異 | Supported (p=0.030) |

#### 圖表 (6 張)

- `reliability_diagrams` — Reliability diagrams
- `ece_comparison` — ECE comparison across models
- `coverage_accuracy` — Coverage-accuracy tradeoff
- `overconfidence_gap` — Overconfidence gap visualization
- `topic_analysis` — Topic-wise calibration analysis
- `confidence_distribution` — Confidence distribution

#### 實驗數據路徑

| 資料 | 路徑 |
|------|------|
| 主要結果 (N=250) | `experiments/D1_confidence_calibration/results/run_20260202_034237/` |
| D4 風險分析 | `experiments/D4_overconfident_risk/results/run_20260205_010016/` |

#### 論文檔案結構

```
drafts/selected/D1_calibration/
├── main.tex                    # 完整論文 (3,463 words)
├── main.pdf                    # 編譯 PDF
├── run_analysis.py             # 數據分析腳本
├── analysis_results.json       # 分析結果 JSON
├── STATUS.md                   # 詳細完成度檢查表
├── figures/                    # 6 張出版品質圖表 (PDF)
│   ├── reliability_diagrams.pdf
│   ├── ece_comparison.pdf
│   ├── coverage_accuracy.pdf
│   ├── overconfidence_gap.pdf
│   ├── topic_analysis.pdf
│   └── confidence_distribution.pdf
├── tables/                     # LaTeX 表格原始碼
└── submission/
    └── cover_letter.tex        # FRL 投稿信
```

---

### Paper 7 (P7): G2 — 訊號理論

**Title**: *The Certification Signal Erosion Hypothesis: A Modified Spence Model for AI-Disrupted Professional Credentialing*

**Target Journal**: Finance Research Letters / J. Financial Economics

**Status**: PUBLICATION-READY — 4,231 words, 理論模型 + A5 實證支持

**Folder**: `G2_signaling_theory/`

#### 中文摘要

- **論文題目**：認證訊號侵蝕假說：AI 衝擊下專業認證的修正 Spence 模型
- **摘要**：本研究以 Spence (1973) 訊號理論為基礎，建立 AI 衝擊下專業認證價值侵蝕的數學模型。提出六維能力分類法，發現 AI 已能複製約 50% 的 CFA 認證能力，導致 CFA 認證的訊號保留率降至 28.8%。以 A5 選項偏差實驗作為實證支持：GPT-4o-mini +1.9pp (n.s.)，GPT-5-mini +9.6pp (p<0.001)，展示 AI 能力快速提升的跨模型證據。
- **實驗方法**：Modified Spence signaling model, multi-dimensional ability space, AI replicability mapping, equilibrium analysis, A5 empirical validation
- **主要結果**：Signal Retention Ratio R=0.288; A5 cross-model evidence of rapid AI capability growth
- **結論**：CFA 認證正在「部分訊號瓦解」的均衡中。認證機構應重新設計考試以強調 AI 難以複製的能力維度。

#### 核心結果

| 指標 | 數值 |
|------|------|
| CFA Signaling Retention Ratio (R) | **0.288** (保留 ~29% 訊號價值) |
| AI-replicable abilities (tipping point) | 50% already replicable |
| Ability Taxonomy Dimensions | 6 dimensions |
| Framework | Modified Spence (1973) + Autor Task Framework |

**A5 實證支持 — 跨模型 AI 能力成長**

| 模型 | Option Bias | McNemar p |
|------|-------------|-----------|
| GPT-4o-mini | +1.9pp | p=0.251 (n.s.) |
| GPT-5-mini | +9.6pp | **p<0.001*** |

#### 圖表 (2 張)

- `fig1_ability_taxonomy` — Six-dimensional ability taxonomy
- `fig2_signal_erosion` — Signal erosion dynamics

#### 論文檔案結構

```
drafts/selected/G2_signaling_theory/
├── main.tex                    # 完整論文 (4,231 words)
├── main.pdf                    # 編譯 PDF
├── figures/
│   ├── fig1_ability_taxonomy.pdf
│   └── fig2_signal_erosion.pdf
└── submission/
```

---

## 圖表總覽

7 篇論文共含 **23 張出版品質圖表** (PDF 格式)：

| 論文 | 圖表數 | 圖表列表 |
|------|--------|---------|
| P1 (A1+A5) | 4 | option_bias, three_tier, cross_model_option_bias, cross_model_three_tier |
| P2 (I1+I3) | 4 | accuracy_degradation, noise_sensitivity, stress_test_framework, memorization_paradox |
| P3 (I2) | 2 | bias_score_comparison, debiasing_effect |
| P4 (D6) | 2 | ethics_robustness, ethics_accuracy |
| P5 (E1) | 5 | error_type_distribution, topic_error_profile, cognitive_stages, gci_recovery, cross_model_gci |
| P6 (D1+D4) | 6 | reliability_diagrams, ece_comparison, coverage_accuracy, overconfidence_gap, topic_analysis, confidence_distribution |
| P7 (G2) | 2 | ability_taxonomy, signal_erosion |
| **合計** | **25** | |

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

# A1: 開放式作答 (N=1,032)
python -m experiments.A1_open_ended.run_experiment --dataset easy --model gpt-4o-mini

# A5: 選項偏差 (N=1,032)
python -m experiments.A5_option_bias.run_experiment --dataset easy --model gpt-4o-mini

# I1: 反事實壓力測試 (N=1,032)
python -m experiments.I1_counterfactual.run_experiment --dataset easy --model gpt-4o-mini --perturbation-levels 1 2

# I3: 雜訊敏感度 (N=1,032)
python -m experiments.I3_noise_red_herrings.run_experiment --dataset easy --model gpt-4o-mini --noise-types N1 N2 N3 N4

# I2: 行為偏誤 (N=60, 6 types)
python -m experiments.I2_behavioral_biases.run_experiment --bias-types loss_aversion anchoring framing recency disposition_effect overconfidence --limit 10 --model gpt-4o-mini

# D6: 對抗式道德測試 (N=47)
python -m experiments.D6_adversarial_ethics.run_experiment --dataset easy --limit 47 --model gpt-4o-mini

# D1: 信心校準 (N=90 x 3 configs)
python -m experiments.D1_confidence_calibration.run_experiment --dataset easy --limit 100 --model gpt-4o-mini

# D4: 過度自信風險分析 (依賴 D1 結果)
python -m experiments.D4_overconfident_risk.run_experiment --input "experiments/D1_confidence_calibration/results/run_*/results.json" --confidence-threshold 0.8

# E1: 錯誤分析 (依賴 A1 結果中的錯誤)
python -m experiments.E1_error_analysis.run_experiment --input "experiments/A1_open_ended/results/run_*/results.json"
```

### 結果存放

所有結果自動存在 `experiments/XX/results/run_YYYYMMDD_HHMMSS/results.json`。

---

## 全部實驗結果路徑索引

| 實驗 | 模型 | N | 路徑 | 用於論文 |
|------|------|---|------|---------|
| A1 Open-Ended | GPT-4o-mini | 1,032 | `experiments/A1_open_ended/results/run_20260206_112613/` | P1 |
| A1 Open-Ended | GPT-5-mini | 1,032 | `experiments/A1_open_ended/results/run_20260207_174118/` | P1 |
| A5 Option Bias | GPT-4o-mini | 1,032 | `experiments/A5_option_bias/results/run_20260206_171904/` | P1, P7 |
| A5 Option Bias | GPT-5-mini | 1,032 | `experiments/A5_option_bias/results/run_20260207_174114/` | P1, P7 |
| I1 Counterfactual | GPT-4o-mini | 1,032 | `experiments/I1_counterfactual/results/run_20260206_170129/` | P2 |
| I1 Counterfactual | GPT-5-mini | 1,032 | `experiments/I1_counterfactual/results/run_20260207_174116/` | P2 |
| I3 Noise | GPT-4o-mini | 1,032 | `experiments/I3_noise_red_herrings/results/run_20260206_203913/` | P2 |
| I3 Noise | GPT-5-mini | 1,032 | `experiments/I3_noise_red_herrings/results/run_20260207_174115/` | P2 |
| I2 Biases | GPT-4o-mini | 60 | `experiments/I2_behavioral_biases/results/run_20260206_140527/` | P3 |
| D6 Ethics | GPT-4o-mini | 47 | `experiments/D6_adversarial_ethics/results/run_20260206_112341/` | P4 |
| D6 Ethics | GPT-5-mini | 47 | `experiments/D6_adversarial_ethics/results/run_20260207_023637/` | P4 |
| E1 Error Analysis | GPT-4o-mini | 557 errors | `experiments/E1_error_analysis/results/error_analysis_all_methods_20260203_230751.json` | P5 |
| E1 GCI | GPT-4o-mini | 557 | `experiments/E1_error_analysis/results/golden_context_gpt-4o-mini_20260207_032341.json` | P5 |
| E1 GCI | GPT-5-mini | 557 | `experiments/E1_error_analysis/results/golden_context_gpt-5-mini_20260207_220440.json` | P5 |
| D1 Calibration | GPT-4o-mini + qwen3:32b | 257 | `experiments/D1_confidence_calibration/results/run_20260202_034237/` | P6 |
| D4 Risk | -- | 74 篩選 | `experiments/D4_overconfident_risk/results/run_20260205_010016/` | P6 |

---

## LaTeX 編譯

所有論文使用 `elsarticle` 文件類別（Elsevier 官方模板），preprint 格式：

```bash
# 編譯單篇論文
cd drafts/selected/D1_calibration
/Library/TeX/texbin/pdflatex main.tex && /Library/TeX/texbin/pdflatex main.tex

# 需要跑兩次以解決交叉引用
```

**Overleaf 相容性**: 所有論文可直接上傳 Overleaf 編譯。`elsarticle` 是 Overleaf 內建支援的標準模板類別。

---

## 檔案索引

### 論文說明文件（每篇含學術說明 + 具體舉例 + 實際結果）

| 說明文件 | 論文 | 論文資料夾 |
|---------|------|-----------|
| `P1-A1+A5-選項偏差與開放式評估.md` | Beyond Multiple Choice (A1+A5 合併) | `A1_open_ended/` |
| `P2-I1+I3-反事實壓力測試與雜訊.md` | Stress Testing Financial LLMs (I1+I3 合併) | `I1_counterfactual/` |
| `P3-I2-行為金融偏誤.md` | Inherited Irrationality (I2) | `I2_behavioral_biases/` |
| `P4-D6-對抗式道德測試.md` | Under Pressure: Adversarial Ethics (D6) | `D6_adversarial_ethics/` |
| `P5-E1-錯誤圖譜.md` | The CFA Error Atlas (E1) | `E1_error_atlas/` |
| `P6-D1+D4-信心校準與風險.md` | When AI Is Confidently Wrong (D1+D4 合併) | `D1_calibration/` |
| `P7-G2-訊號理論.md` | Certification Signal Erosion (G2) | `G2_signaling_theory/` |

### 論文資料夾結構（每個都相同）

```
XX_name/
├── main.tex              # LaTeX 論文主文件
├── main.pdf              # 編譯 PDF
├── STATUS.md             # 完成度檢查表 (部分論文有)
├── figures/              # 圖表 (PDF + PNG)
└── submission/           # 投稿信等
```

---

## 指導教授

### 主要指導教授：繆維中老師 (Daniel Wei-Chung Miao)

- **背景**：財務數學、風險管理、統計方法
- **偏好**：Economic Significance > NLP 指標；重視風險分析、敏感度分析、穩健性
- **最對口論文**: P6: D1+D4 (校準+風險) -> P2: I1+I3 (壓力測試+穩健性)

### 共同指導教授：張光第老師 (Guang-Di Chang)

---

## 聯絡資訊

**程煒倫 (Wei-Lun Cheng)**
博士班研究生，Graduate Institute of Finance, NTUST (台科大財金所)
主要指導教授：Daniel Wei-Chung Miao (繆維中)
共同指導教授：Guang-Di Chang (張光第)
