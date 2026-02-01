# A3 CFA 作為 AGI 基準：跨基準相關性分析
# CFA as AGI Benchmark: Cross-Benchmark Correlation Analysis

## 研究問題

CFA 考試涵蓋金融知識記憶、數值計算、邏輯推理、倫理判斷、情境分析等多種認知維度，但它在 LLM 能力評估生態系中的獨特定位是什麼？與 MMLU (通用知識)、GSM8K (數學推理)、ARC (抽象推理)、HumanEval (程式生成) 等主流 benchmark 相比，CFA 測量的是哪些其他 benchmark 無法捕捉的能力維度？如果一個模型在 MMLU 上表現優異但在 CFA 上失敗，這意味著什麼？反過來呢？本研究通過大規模的跨基準相關性分析，定位 CFA 在 LLM 能力圖譜中的獨特位置，並論證其作為「專業領域整合推理」benchmark 的不可替代性。

## 核心方法

第一步是收集多模型的跨 benchmark 表現數據。利用 Open LLM Leaderboard、各模型的技術報告、以及我們自己的 CFA 測試結果，建構一個 Model x Benchmark 的表現矩陣。主要 benchmark 包括：MMLU (知識廣度)、GSM8K (數學推理)、MATH (高階數學)、ARC-Challenge (抽象推理)、HumanEval (程式能力)、HellaSwag (常識推理)、TruthfulQA (事實性)、WinoGrande (語言理解)。CFA 使用 FinEval-CFA-Easy (1,032 題) 和 FinEval-CFA-Challenge (90 題) 的結果。

第二步是統計分析。計算 CFA 成績與每個 benchmark 的 Pearson/Spearman 相關係數，識別高相關（r > 0.8，CFA 可被其他 benchmark 預測）與低相關（r < 0.5，CFA 測量了獨特能力）的 benchmark。進一步使用 Principal Component Analysis (PCA) 將所有 benchmark 分數投射到二維空間，觀察 CFA 是否與其他 benchmark 聚類或獨立。

第三步是能力維度分析。將 CFA 題目按認知維度分類（Knowledge Recall, Numerical Computation, Analytical Reasoning, Ethical Judgment, Integrative Assessment），分別計算每個維度與外部 benchmark 的相關性。假說是：CFA 的 Knowledge Recall 維度與 MMLU 高度相關，Numerical Computation 與 GSM8K 高度相關，但 Ethical Judgment 和 Integrative Assessment 與所有現有 benchmark 的相關性都很低——這就是 CFA 的獨特貢獻。

## 實驗設計

1. 從 Open LLM Leaderboard 和模型技術報告收集 30+ 模型在 8+ benchmark 上的公開分數
2. 對相同的 30+ 模型（或其中可獲取的子集），在 FinEval-CFA-Easy 上進行評測
3. 建構 Model x Benchmark 表現矩陣（30+ rows x 10+ columns）
4. 計算 correlation matrix: CFA-total, CFA-by-dimension vs each external benchmark
5. 執行 PCA，將 benchmark 投射到二維空間，繪製 benchmark positioning map
6. 對 CFA 內部的 5 個認知維度分別計算與外部 benchmark 的相關性
7. 識別 CFA-unique 能力維度（與所有外部 benchmark 相關性 < 0.5 的維度）
8. Regression analysis: 能否用 {MMLU, GSM8K, ARC, HumanEval} 預測 CFA 成績？殘差代表什麼？
9. 分析 model size 與 CFA 相對表現的關係（CFA 是否比其他 benchmark 更受益於規模）

## 需要的積木
- ✅ FinEval-CFA-Easy (1,032 題) + CFA-Challenge (90 題) — 已下載
- ✅ Open LLM Leaderboard 的公開分數 — 可網路取得
- ✅ OpenAI API + Ollama local models — 用於自行評測
- ❌ 公開分數爬蟲/收集腳本 — 需系統性收集 30+ 模型的跨 benchmark 分數
- ❌ CFA 題目認知維度標註 — 需為 1,032 題標註所屬認知維度
- ❌ 統計分析 pipeline — 需實作 correlation, PCA, regression 分析

## 預期產出
- `results/A3_cross_benchmark_matrix.csv` — Model x Benchmark 完整表現矩陣
- `results/A3_correlation_analysis.json` — CFA vs each benchmark 的相關係數
- `results/A3_pca_components.json` — PCA 分析結果
- `results/A3_regression_residuals.json` — 用其他 benchmark 預測 CFA 的殘差分析
- `figures/A3_correlation_heatmap.png` — Benchmark 間相關性熱力圖
- `figures/A3_pca_benchmark_map.png` — Benchmark 在二維 PCA 空間中的定位圖
- `figures/A3_cfa_dimension_correlation.png` — CFA 各維度與外部 benchmark 的相關性圖
- Table: CFA-unique ability dimensions (low correlation with all external benchmarks)

## 資料需求
- FinEval-CFA-Easy: 全部 1,032 題（需認知維度標註）
- FinEval-CFA-Challenge: 全部 90 題
- 外部 benchmark 公開分數: 30+ 模型 x 8+ benchmark（從 leaderboard 收集）
- 部分模型可能需要自行在 CFA 上評測（若公開分數不含 CFA）

## 模型需求
- 主要使用公開分數（不需自行跑所有模型）
- 自行評測: gpt-4o, gpt-4o-mini, qwen3:32b, qwen3:30b-a3b, deepseek-r1:14b, llama3.1:8b
- 盡量覆蓋不同規模（1B-200B+）與不同系列（Llama, Qwen, GPT, Gemma, Phi, DeepSeek）

## 狀態
Ready — 外部 benchmark 分數可直接從 leaderboard 取得，需開發分數收集腳本與認知維度標註

## 可合併的點子
- A4 (prompt sensitivity) 的穩定性分析可作為 CFA 獨特性的另一個證據維度
- A2 (4-level evaluation) 的 Level 0 結果直接作為本研究的 CFA 分數輸入
- 可與 A1 (open-ended) 結合，比較 MCQ-CFA 和 open-ended-CFA 與外部 benchmark 的相關性差異

## 來源筆記
新點子 — 受 drafts/archive/old-raw-1.md 中 ARC-AGI benchmark 的討論啟發，反思 CFA 在 LLM 評估生態系中的獨特定位
