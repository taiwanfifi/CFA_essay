# A1b 金融錯誤歸因分類系統
# Financial Error Attribution Taxonomy for LLM Numerical Reasoning

## 研究問題

當 LLM 在 CFA 開放式數值題上答錯時，錯誤的根本原因是什麼？是選錯公式（formula selection error）、從題幹中提取錯誤的數值（numerical extraction error）、計算過程出錯（calculation error）、還是使用了不同但合理的假設（assumption mismatch）？現有研究僅報告最終正確率，完全忽略錯誤的結構性差異。一個「因為用了 continuous compounding 而非 annual compounding 導致答案偏差 0.3%」的錯誤，與一個「完全用錯公式導致答案差兩個 order of magnitude」的錯誤，在性質上截然不同，但在現有評測中被等同處理。本研究提出一套結構化的金融錯誤歸因分類系統（Financial Error Attribution Taxonomy），並實證分析不同模型、不同 CFA 主題的錯誤模式差異。

## 核心方法

分類系統建立在 A1a 的三層判定之上，專注於 Level B (directionally correct) 和 Level C (incorrect) 的細分。對於 Level B，進一步區分 assumption mismatch 的具體類型：compounding convention mismatch、day-count convention mismatch、rounding policy mismatch、tax treatment assumption mismatch。對於 Level C，建立四大類錯誤分類：(1) Formula Selection Error — 選用了不適用的公式或原則；(2) Numerical Extraction Error — 從題幹/exhibit 中讀取了錯誤的數值；(3) Calculation Execution Error — 公式正確但計算過程有誤（算術錯誤、單位錯誤、精度錯誤）；(4) Conceptual Confusion — 混淆了相似但不同的金融概念。

分類的關鍵工具是 post-hoc error explanation：對每個錯誤回答，要求 LLM 自身解釋「為什麼你的答案與正解不一致」。這個解釋僅用於 error attribution 分析，絕不計入 accuracy（否則測的就不是 model 而是 agent）。然後使用 GPT-4o 作為 judge，基於模型的原始推理過程和 post-hoc 解釋，分類錯誤的根本原因。

為確保分類品質，我們對 200 道題進行人工標註建立 gold standard，計算 GPT-4o 自動分類與人工標註的 Cohen's Kappa，目標 > 0.7。

## 實驗設計

1. 使用 A1a benchmark 收集所有模型的錯誤回答（Level B + Level C），預估 1,500-3,000 個錯誤樣本
2. 對每個錯誤回答，提取模型的原始 reasoning chain
3. 執行 post-hoc error explanation：prompt 模型解釋與正解的差異（不計入 accuracy）
4. 使用 GPT-4o judge 進行 error attribution 分類（四大類 + assumption mismatch 子類）
5. 人工標註 200 個錯誤樣本作為 gold standard，計算 Cohen's Kappa
6. 建立 Error Attribution Matrix: CFA Topic (rows) x Error Type (columns)
7. 分析跨模型的錯誤模式相似性（Jaccard similarity of error profiles）
8. 分析模型規模與錯誤類型分布的關係（小模型 vs 大模型是否犯不同類型的錯）
9. Case study: 選取 10 個最具代表性的錯誤案例進行深度分析

## 需要的積木
- ✅ A1a benchmark 的 Gold Answer Set — 提供三層判定的基礎
- ✅ OpenAI API (gpt-4o) — 用於 error attribution 的 LLM-as-judge
- ✅ CFA_Extracted 的 gpt4_answer_justification — 提供錯誤分析的參考
- ❌ Post-hoc explanation prompt template — 需設計讓模型解釋答案差異而非修正答案的 prompt
- ❌ Error attribution classifier prompt — 需設計結構化的分類 prompt，含決策樹邏輯
- ❌ 人工標註 protocol — 需定義標註指南、訓練標註者、建立 inter-annotator agreement 流程

## 預期產出
- `results/A1b_error_taxonomy.json` — 完整的錯誤分類結果（每個錯誤樣本的 error type + evidence）
- `results/A1b_error_attribution_matrix.csv` — CFA Topic x Error Type 矩陣（含頻率與百分比）
- `results/A1b_cross_model_similarity.json` — 模型間錯誤模式的 Jaccard similarity
- `figures/A1b_error_heatmap.png` — 錯誤歸因熱力圖
- `figures/A1b_error_by_model_size.png` — 模型規模 vs 錯誤類型分布圖
- `results/A1b_kappa_scores.json` — GPT-4o judge vs human annotator 的 Cohen's Kappa
- Table: top-5 most common error patterns per CFA topic

## 資料需求
- A1a benchmark 的全部錯誤回答（依賴 A1a 完成）
- FinEval-CFA-Challenge: 90 題的錯誤回答作為高難度子集分析
- 200 個錯誤樣本的人工標註（需 CFA 知識背景標註者，預估 30-40 小時）

## 模型需求
- OpenAI API: gpt-4o（judge + post-hoc explanation generator）
- 被分析模型: gpt-4o, gpt-4o-mini, qwen3:32b, qwen3:30b-a3b, deepseek-r1:14b, llama3.1:8b, qwen3:4b
- 模型規模跨度需覆蓋 2B-200B+ 以分析規模效應

## 狀態
Needs A1a — 依賴 A1a benchmark 的 Gold Answer Set 與 baseline 結果完成後才能開始

## 可合併的點子
- A1 (整體框架) 自然包含本研究作為 error attribution 子系統
- A2 (4-level evaluation) 可使用本研究的 error taxonomy 分析不同 Level 的錯誤模式差異
- A4 (prompt sensitivity) 可使用本研究分析 prompt 變化導致的錯誤類型轉移

## 來源筆記
drafts/archive/old-raw-2.md — 「Error attribution，而不只是 Accuracy」、「區分計算錯 vs 方向模糊但合理」、「post-hoc analysis 而非 second chance」的方法論源自此文件
