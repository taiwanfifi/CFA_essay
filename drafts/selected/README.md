# 精選研究清單：11 篇論文的攻擊路線圖

> **緊急狀況**：資格考口試申請，開學日 2/23，需在 2/10 前遞交申請 + 投稿證明

---

## 當前情況總覽

### 時程
| 日期 | 里程碑 |
|------|--------|
| **2/5 (今天)** | 整理 GitHub 代碼、生成圖表 |
| **2/6 - 2/8** | 撰寫論文初稿（重點：Intro + Conclusion） |
| **2/9 (週一)** | 寄給繆教授 + 線上投稿（取得投稿證明） |
| **2/10** | 當面遞交資格考口試申請書 |
| **2/23** | 開學日 |

### 指導教授：繆維中老師
- **背景**：財務數學、風險管理、統計方法
- **偏好**：
  - 想看 **Economic Significance**，不只是 NLP 指標（BLEU, Accuracy）
  - 重視 **風險分析**：「AI 不知道自己錯」是金融界最怕的
  - 喜歡 **敏感度分析 (Sensitivity Analysis)**、**穩健性 (Robustness)**

### 跟老師溝通的話術

```
「繆老師您好，我是學生程煒倫。關於我的資格考試進度，我想跟老師誠實報告並尋求您的指導。

我目前已經針對『LLM 在 CFA 考試與金融決策』的研究完成了論文雛形，包含：

1. 信心校準分析 (Calibration)：證明 AI 有 29.6% 的高信心錯誤率，這對金融決策有重大風險
2. 反事實壓力測試 (Counterfactual Stress Test)：驗證 LLM 是真的理解金融公式，還是僅僅背誦考古題
   我運用了類似敏感度分析 (Sensitivity Analysis) 的方法來擾動數值

我計畫這兩天將初稿投往《Finance Research Letters》(SSCI Q1)。
這本期刊審稿快，我只要拿到投稿確認信，就能立刻向所上遞交資格考口試申請。
懇請老師支持這個方案。」
```

---

## 投稿策略

### 目標期刊（按優先順序）

| 期刊 | 等級 | 適合論文 | 速度 | 備註 |
|------|------|----------|------|------|
| **Finance Research Letters (FRL)** | SSCI Q1 | D1+D4 | 極快 | **首選**：短篇論文，審稿 2 週內 |
| **Financial Innovation (FI)** | SSCI | D1+D4, I1+I3 | 快 | 對 FinTech + AI Agent 最開放 |
| **Journal of Financial Studies (財務金融學刊)** | TSSCI | 全部 | 中 | 台灣本土頂尖，老師認可度高 |
| **證券市場發展季刊** | TSSCI | D1+D4 | 中 | 台灣證券界權威 |

### 推薦投稿組合

| 優先級 | 組合 | 綜合評分 | 通關速度 | 老師喜好度 | 理由 |
|--------|------|----------|----------|------------|------|
| **首選** | D1+D4 (校準與風險) | **95** | 極快 | 很高 | 純統計 + 風險管理，繆老師專長 |
| **次選** | I1+I3 (壓力測試) | **90** | 快 | 高 | 穩健性分析，敏感度測試 |
| 備選 | E1 (錯誤地圖) | 70 | 慢 | 中 | 偏 NLP 實證 |

### 專業術語轉換（財金所版本）

| 不要說 | 改說 |
|--------|------|
| Prompt Engineering | 不同隨機種子 (Seed) 下 AI 回答的穩健性分析 |
| AI Agent 考 CFA | 模擬自主代理人在金融倫理約束下的決策路徑優化 |
| Calibration | 信心分佈的校準誤差 (Expected Calibration Error) |
| Jailbreak | 對抗式情境下的決策偏誤 |

---

## POC 實驗狀態

### 已完成 POC（可直接寫論文）

| 實驗 | N | 核心指標 | 數值 | 管道 | 可用於論文 |
|------|---|----------|------|------|-----------|
| **D1 Calibration** | 250 | ECE | 0.18 | ✅ | D1+D4 組合 |
| **D4 Overconfident** | 74 篩選 | High-risk rate | 29.6% | ✅ | D1+D4 組合 |
| **A1 Open-Ended** | 5 | Strict/Lenient | 60%/80% | ✅ | A1+A5 組合 |
| **A5 Option Bias** | 5 | Option Bias | -40% | ✅ | A1+A5 組合 |
| **I1 Counterfactual** | 5 | Mem. Gap | +10% | ✅ | I1+I3 組合 |
| **I3 Noise** | 5×4 | NSI | 0.000 | ✅ | I1+I3 組合 |
| **I2 Biases** | 10 | Bias Score | 0.500 | ✅ | 獨立論文 |
| **E1 Error Atlas** | 90 | Taxonomy | 完成 | ✅ | 獨立論文 |
| **B1 Agent** | 90 | Accuracy | 有結果 | ✅ | 補充材料 |

### 待執行

| 實驗 | 狀態 | 需要什麼 | 預估時間 |
|------|------|----------|----------|
| **D6 Adversarial Ethics** | ❌ 未開始 | 設計 30 題對抗 prompt | 1-2 天 |
| **G2 Signaling Theory** | 📝 純理論 | 撰寫理論模型 | 2 週 |
| **H1 Multimodal** | ⏸️ 暫緩 | 需要 CFA 圖表資料 | TBD |

### 放大實驗（完整論文需要）

- [ ] D1: 擴大到 CFA-Easy 1,032 題 + CFA-Challenge 90 題
- [ ] I1: 加入 Level 2 (雙參數) 和 Level 3 (結構性) 微擾
- [ ] I2: 補齊 framing, recency, disposition, overconfidence 四種偏誤
- [ ] D4: 分類全部 74 筆高信心錯誤

---

## 論文資料夾結構

每個資料夾內應包含：
```
D1_calibration/
├── main.tex              # LaTeX 主文件
├── figures/              # 圖表
├── tables/               # 表格
├── bibliography.bib      # 參考文獻
└── submission/           # 投稿相關文件
    ├── cover_letter.tex
    └── response_to_reviewers.tex (如需)
```

### 各資料夾內容規劃

| 資料夾 | 論文標題（暫定） | 狀態 |
|--------|------------------|------|
| `D1_calibration/` | Confidence Calibration of LLMs on CFA Examinations | 🔴 待建立 |
| `D4_overconfident/` | 與 D1 合併 | — |
| `I1_counterfactual/` | Robustness of Financial LLMs: A Counterfactual Stress Test | 🔴 待建立 |
| `I3_noise_sensitivity/` | 與 I1 合併 | — |
| `A1_open_ended/` | Open-Ended Evaluation of Financial Reasoning | 🔴 待建立 |
| `A5_option_bias/` | 與 A1 合併 | — |
| `D6_adversarial_ethics/` | Can LLMs Uphold Fiduciary Duty Under Pressure? | 🔴 待建立 |
| `E1_error_atlas/` | CFA Error Pattern Atlas | 🔴 待建立 |
| `G2_signaling_theory/` | Professional Certification Signaling Under AI Disruption | 🔴 待建立 |
| `H1_multimodal/` | Multimodal Financial Reasoning Benchmark | ⏸️ 暫緩 |
| `I2_behavioral_biases/` | Behavioral Biases in Financial LLMs | 🔴 待建立 |

---

## 首選論文：D1+D4 (校準與風險)

### 為什麼選這個？

1. **老師專長對口**：繆老師是統計/風險管理背景
2. **數據已就緒**：D1 有 250 筆，D4 篩出 74 筆高風險
3. **經濟意義明確**：「29.6% 高信心錯誤」= 實際金融決策風險
4. **跑起來最快**：純統計分析 + 繪圖，不需額外 inference

### 論文結構

```
Title: When AI Is Confidently Wrong: Calibration and Risk Analysis
       of Large Language Models in Financial Decision-Making

1. Introduction
   - LLM 在金融的潛力與風險
   - 過度自信比答錯更危險

2. Related Work
   - LLM Calibration 文獻
   - AI in Finance 文獻

3. Methodology
   - Verbalized Confidence Estimation
   - Expected Calibration Error (ECE)
   - High-Confidence Error Identification

4. Experiments
   - Dataset: CFA-Challenge (90) + CFA-Easy (1,032)
   - Models: gpt-4o-mini, gpt-4o, claude-3.5-sonnet
   - Metrics: ECE, Brier Score, Coverage-Accuracy Tradeoff

5. Results
   - Table 1: Calibration metrics by model
   - Figure 1: Reliability Diagram
   - Figure 2: High-confidence error distribution by CFA topic
   - Table 2: Risk classification of overconfident errors

6. Discussion
   - Economic Significance: VaR implications
   - CFA Ethics Framework: Does overconfident AI violate fiduciary duty?
   - Regulatory Implications: Minimum calibration standards for financial AI

7. Conclusion
   - AI 不是考幾分的問題，是它知不知道自己考錯的問題
```

### 核心圖表（需生成）

1. **Reliability Diagram**：信心 vs 實際準確率
2. **ECE Bar Chart**：各模型的 ECE 比較
3. **Heatmap**：High-confidence error rate by CFA topic
4. **Risk Matrix**：Likelihood × Impact

---

## 次選論文：I1+I3 (壓力測試)

### 為什麼選這個？

1. **敏感度分析**：繆老師熟悉的方法論
2. **穩健性測試**：金融界重視的概念
3. **數據已就緒**：I1 有 5 題 POC，I3 有 4 種雜訊測試

### 論文結構

```
Title: Stress Testing Financial LLMs: Counterfactual Perturbation
       and Noise Sensitivity Analysis

1. Introduction
   - AI 是背題還是真懂？
   - 穩健性對金融決策的重要性

2. Methodology
   - Counterfactual Perturbation (I1)
   - Noise Injection (I3)
   - Robust Accuracy vs Traditional Accuracy

3. Results
   - Memorization Gap: +10%
   - Noise Sensitivity Index by noise type
   - Dose-Response Curve

4. Discussion
   - 約 1/3 的「正確」可能是記憶而非推理
   - 對 AI-assisted financial analysis 的啟示
```

---

## 快速導覽表

| 編號 | 題目 | 測什麼 | 新穎點 | POC | 依賴 |
|------|------|--------|--------|-----|------|
| **D1** | Calibration | 信心值是否可靠 | ECE 金融場景 | ✅ 250筆 | 無 |
| **D4** | Overconfident Risk | 高信心錯誤風險 | CFA Ethics 框架 | ✅ 74筆 | D1 |
| **D6** | Adversarial Ethics | 道德防線韌性 | Jailbreak 金融版 | ❌ | 無 |
| **A1** | Open-Ended | 去選項後真實能力 | 三層判定機制 | ✅ 5題 | 無 |
| **A5** | Option Bias | 選項優勢量化 | 三維分解 | ✅ 5題 | A1 |
| **E1** | Error Atlas | 錯誤分類地圖 | 三維 Taxonomy | ✅ 90題 | 無 |
| **G2** | Signaling Theory | AI 瓦解認證價值 | Modified Spence | 📝 | G1 |
| **H1** | Multimodal | 圖表理解瓶頸 | 首個多模態 CFA | ⏸️ | 無 |
| **I1** | Counterfactual | 背題 vs 真懂 | Robust Accuracy | ✅ 5題 | 無 |
| **I2** | Behavioral Biases | 繼承人類偏誤 | 六維偏誤框架 | ✅ 10情境 | 無 |
| **I3** | Noise Sensitivity | 雜訊過濾能力 | NSI 指標 | ✅ 5×4 | 無 |

---

## 檔案索引

| 研究提案文件 | 說明 |
|--------------|------|
| `A1-open-ended-numerical.md` | 開放式數值推理基準 |
| `A5-mcq-option-bias.md` | 選項偏差量化 |
| `D1-calibration-selective-prediction.md` | 信心校準與選擇性預測 |
| `D4-overconfident-ai-regulation.md` | 過度自信 AI 風險分析 |
| `D6-adversarial-ethics-jailbreak.md` | 對抗式金融道德測試 |
| `E1-error-pattern-atlas.md` | 錯誤圖譜 |
| `G2-signaling-theory.md` | 訊號理論 |
| `H1-multimodal-financial-reasoning.md` | 多模態金融推理 |
| `I1-counterfactual-stress-test.md` | 反事實壓力測試 |
| `I2-behavioral-biases-llm.md` | 行為金融學偏誤 |
| `I3-noise-red-herrings.md` | 雜訊與紅鯡魚 |

| 論文資料夾 | 用途 |
|------------|------|
| `D1_calibration/` | D1+D4 合併論文（首選） |
| `I1_counterfactual/` | I1+I3 合併論文（次選） |
| `A1_open_ended/` | A1+A5 合併論文 |
| `D6_adversarial_ethics/` | D6 獨立論文 |
| `E1_error_atlas/` | E1 獨立論文 |
| `G2_signaling_theory/` | G2 理論論文 |
| `H1_multimodal/` | H1 暫緩 |
| `I2_behavioral_biases/` | I2 獨立論文 |

---

## 立即行動 (2/5 Today)

### 第一優先：生成 D1+D4 圖表

```bash
# 跑完整 D1 實驗（放大樣本）
python -m experiments.D1_confidence_calibration.run_calibration \
  --dataset challenge --model gpt-4o-mini

# 生成 Reliability Diagram
python -m experiments.D1_confidence_calibration.visualize \
  --input experiments/D1_confidence_calibration/results/run_*/results.json
```

### 第二優先：整理現有 POC 結果

所有 POC 結果已在 `RESULTS.md`，需要：
1. 轉換成論文圖表格式
2. 加入統計顯著性檢定
3. 撰寫 figure captions

### 第三優先：準備投稿材料

1. 下載 FRL 的 LaTeX 模板
2. 準備 cover letter
3. 確認共同作者資訊

---

## 聯絡資訊

**程煒倫 William**
Research Assistant, Institute of Information Science, Academia Sinica
+886 908-070-602
