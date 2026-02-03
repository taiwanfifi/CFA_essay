# I1 反事實壓力測試：LLM 是真懂金融邏輯還是背考古題？
# Counterfactual Stress Testing: Do Financial LLMs Reason or Memorize?

## 研究問題

LLM 在 CFA benchmark 上的高準確率可能是假象——模型在預訓練階段大量接觸了考試準備材料（SchweserNotes、Kaplan、AnalystPrep 等），因此「答對」可能只是 memorization 而非 reasoning。這個問題在金融領域特別嚴重：CFA 考試題庫有限、結構固定、數值模式重複，完美符合 data contamination 的條件。

本研究提出 Counterfactual Stress Test 方法：對原始 CFA 題目進行 **數值微擾**（改變利率、期限、面額等參數）與 **邏輯反轉**（改變前提條件），測試模型是否能 consistent 地產出正確答案。如果模型真正理解金融邏輯，則微擾後的準確率應與原題相近；如果只是背誦，則微擾後準確率會顯著下降。

## 核心方法

### 三層微擾設計

**Level 1 — 數值微擾（Numerical Perturbation）**
- 改變題目中的數值參數（利率 5% → 7%、面額 1000 → 1500、期限 3 年 → 5 年），保持解題邏輯不變
- 正確答案隨之改變，但所需的公式與推理步驟完全相同
- 測量：模型能否在新數值下正確重算？

**Level 2 — 條件反轉（Conditional Inversion）**
- 改變題目的前提條件（annual compounding → continuous compounding、call option → put option、bull spread → bear spread）
- 需要選擇不同公式或調整推理方向
- 測量：模型能否在新條件下正確切換推理路徑？

**Level 3 — 情境重構（Scenario Reconstruction）**
- 保留核心金融概念，但完全重寫題目情境（換公司名稱、換產業背景、換市場條件）
- 如果模型依賴的是表面模式匹配，重構後應失敗
- 測量：模型的推理能否遷移到全新情境？

### 核心指標

- **Consistency Score** = 微擾後準確率 / 原題準確率
- **Memorization Gap** = 原題準確率 - 微擾題準確率（正值表示 memorization 依賴）
- **Robust Accuracy** = 只有原題 + 所有微擾版本都答對才計分
- **Level-wise Degradation Curve**：隨微擾強度增加，準確率如何衰退

## 實驗設計

**實驗 1：大規模微擾生成**
- 從 CFA-Challenge (90) + CFA-Easy (1,032) 中篩選含數值計算的題目（預估 400-500 題）
- 每道題自動生成 Level 1 微擾 × 3 變體 + Level 2 微擾 × 2 變體 = 5 個微擾版本
- 使用 GPT-4o 生成微擾並人工驗證正確性（抽查 100 題）

**實驗 2：原題 vs 微擾題對照實驗**
- 對每個模型分別跑原題與所有微擾版本
- 計算 per-model、per-topic 的 Consistency Score 與 Memorization Gap
- 統計檢驗：Paired t-test 或 McNemar's test 確認 gap 的顯著性

**實驗 3：Memorization 指標的模型規模效應**
- 假說：更大的模型 memorization 更嚴重（因為看過更多訓練數據）
- 繪製 Memorization Gap vs Model Size 曲線
- 比較 base model vs fine-tuned model 的 memorization 程度

**實驗 4：Robust Accuracy 重新排名**
- 以 Robust Accuracy 取代傳統 accuracy 重新排列 model leaderboard
- 分析：排名變動最大的模型——這些模型在傳統 benchmark 上的表現最虛胖

**實驗 5：與 Data Contamination 的關聯**
- 使用 membership inference attack 或 n-gram overlap 偵測模型是否見過原題
- 相關性分析：contamination 指標與 Memorization Gap 是否高度相關？

## 需要的積木
- ✅ FinEval-CFA-Challenge (90) + CFA-Easy (1,032) — 已就緒
- ✅ OpenAI API (GPT-4o) — 用於微擾生成與驗證
- ✅ Ollama local models — 被測模型
- ❌ 微擾生成 pipeline — 需設計 prompt 模板，自動改變數值/條件並計算新答案
- ❌ 微擾品質驗證機制 — 需確保微擾後題目仍有唯一正確答案
- ❌ Robust Accuracy 評分器 — 需實作「全部版本皆對才計分」的邏輯

## 預期產出
- `results/I1_memorization_gap.json` — 每個模型的 Memorization Gap（per topic）
- `results/I1_consistency_scores.csv` — Model × Topic × Perturbation Level 的 Consistency Score
- `results/I1_robust_accuracy_leaderboard.json` — Robust Accuracy 模型排名
- `figures/I1_degradation_curve.png` — 微擾強度 vs 準確率衰退曲線
- `figures/I1_memorization_vs_model_size.png` — Memorization Gap vs 模型規模
- `figures/I1_leaderboard_shift.png` — 傳統 accuracy vs Robust Accuracy 排名變動圖
- Table: Top-10 highest memorization gap topics with example questions

## 資料需求
- FinEval-CFA-Easy: 全部 1,032 題（篩選計算題後 ~400-500 題）
- FinEval-CFA-Challenge: 90 題（高難度子集）
- CFA_Extracted: 1,124 題的 material 欄位用於輔助微擾設計
- 預估產出微擾題：~2,500 道（500 原題 × 5 微擾版本）

## 模型需求
- OpenAI API: gpt-4o（微擾生成 + 被測）, gpt-4o-mini（被測）
- Ollama local: qwen3:32b, qwen3:30b-a3b, deepseek-r1:14b, llama3.1:8b
- Ollama small: qwen3:4b, phi3.5:3.8b, gemma3
- FinDAP fine-tuned models: Llama-Fin-8b（如可取得，用於比較 fine-tuning 的 memorization 效應）

## 狀態
Ready — 所有 dataset 已就緒。核心瓶頸在於微擾生成 pipeline 的設計與品質控制。

## 可合併的點子
- **A1** (Open-ended Benchmark)：I1 的微擾版本可直接使用 A1 的 open-ended 格式，雙重去除 crutch effect
- **A5** (MCQ Option Bias)：可分析 memorization 在 MCQ vs open-ended 下的差異
- **E1** (Error Atlas)：微擾後新增的錯誤可豐富 E1 的 error taxonomy
- **I3** (Noise & Red Herrings)：Level 3 情境重構與 I3 的雜訊注入有方法論重疊

## 來源筆記
- 靈感來自 GSM-Symbolic (Apple, 2024)：對數學推理題做 symbolic perturbation，發現 LLM 準確率顯著下降
- Contamination 偵測方法參考 Shi et al. (2023) "Detecting Pretraining Data from Large Language Models"
- 金融領域的 data contamination 問題特別嚴重：CFA 題庫小、結構固定、網路資源豐富
