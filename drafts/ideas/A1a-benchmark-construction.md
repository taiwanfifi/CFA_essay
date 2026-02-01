# A1a CFA 開放式數值基準建構與基線
# CFA Open-Ended Numerical Benchmark Construction & Baseline

## 研究問題

如何將現有的 CFA MCQ 題庫系統性地轉換為 open-ended numerical reasoning benchmark，使其既能消除 answer-space restriction bias，又能公平處理金融領域特有的答案模糊性（如不同 compounding convention、day-count convention、rounding policy）？現有的 open-ended 數值 benchmark（如 GSM8K 的去選項版）僅需簡單的 exact match，但金融題目的「正確答案」往往是一個集合而非單一數值。本研究的核心貢獻是：建構一個 canonicalized、tolerance-aware、assumption-documented 的 CFA open-ended benchmark，並釋出為公共資源。

## 核心方法

Benchmark 建構的核心挑戰在於 answer canonicalization。對每道 CFA 計算題，我們定義一個 Gold Answer Set 結構：(1) primary_value：出題者預設假設下的精確答案；(2) acceptable_assumptions：所有合理的替代假設列表（如 annual vs semi-annual compounding）；(3) value_range：每種假設組合對應的數值範圍；(4) tolerance：可接受的精度誤差（通常為 0.5-2%，視題目而定）。

建構流程採用 semi-automatic pipeline：首先使用 GPT-4o 對每道題目提取計算步驟、辨識可能的假設分歧點、計算各假設下的答案；然後由具備 CFA 知識的人工校驗者確認 acceptable_assumptions 的完整性與 tolerance 的合理性。CFA_Extracted dataset 的 material 和 gpt4_answer_justification 欄位提供了豐富的初始資訊。

Baseline 實驗使用統一的 evaluation protocol：模型收到題目（不含選項），輸出自由格式答案，evaluation pipeline 自動提取數值、匹配 Gold Answer Set 中的 value_range、判定 Level A (exact/acceptable) / Level B (directionally correct) / Level C (incorrect)。所有模型使用相同 prompt template，temperature=0，single pass（不允許 retry）。

## 實驗設計

1. 從 FinEval-CFA-Easy (1,032 題) 篩選所有含數值計算成分的題目，預估 400-500 題
2. 使用 GPT-4o 對每題生成 structured extraction：{formula_needed, variables, assumptions, primary_answer, alternative_answers}
3. 人工校驗 200 題（約 40-60 小時），建立 Gold Answer Set quality benchmark
4. 使用校驗後的 200 題評估 GPT-4o auto-extraction 的品質（precision/recall of assumptions）
5. 迭代修正 extraction prompt 直到 assumption coverage > 90%
6. 對全部篩選後題目完成 Gold Answer Set 建構
7. 跑所有模型的 baseline（zero-shot, no options），報告 Level A/B/C 分布
8. 與原始 MCQ 格式的 accuracy 進行 paired comparison
9. 釋出完整 benchmark：題目 + Gold Answer Set + evaluation script

## 需要的積木
- ✅ FinEval-CFA-Easy dataset — 已下載，含題目文本與正確答案
- ✅ CFA_Extracted dataset — 含 material, scenario, exhibit, gpt4_answer_justification 欄位
- ✅ OpenAI API (gpt-4o) — 用於 semi-automatic Gold Answer Set extraction
- ❌ Answer canonicalization pipeline — 需從自由格式答案中提取數值（regex + LLM fallback）
- ❌ Gold Answer Set schema & validator — 需定義 JSON schema 並實作 validation logic
- ❌ Three-tier evaluation script — 需實作 exact/tolerance/directional matching

## 預期產出
- `datasets/CFA_OpenEnded/questions.json` — 去選項的 CFA 計算題（400-500 題）
- `datasets/CFA_OpenEnded/gold_answer_sets.json` — 每題的 Gold Answer Set（含 assumptions + tolerance）
- `datasets/CFA_OpenEnded/eval_script.py` — 標準化評分腳本
- `results/A1a_baseline_results.json` — 所有模型的 Level A/B/C baseline 分數
- `figures/A1a_mcq_vs_open_accuracy.png` — MCQ vs open-ended accuracy 對比圖
- Table: inter-annotator agreement on Gold Answer Set construction (Cohen's Kappa)

## 資料需求
- FinEval-CFA-Easy: 全部 1,032 題（篩選後 400-500 題）
- CFA_Extracted: 1,124 題用於輔助建構
- FinEval-CFA-Challenge: 90 題作為 hard subset

## 模型需求
- OpenAI API: gpt-4o（Gold Answer Set extraction + baseline）, gpt-4o-mini（baseline）
- Ollama local: qwen3:32b, deepseek-r1:14b, llama3.1:8b（baseline comparison）
- 小模型: qwen3:4b, phi3.5:3.8b（lower bound 估計）

## 狀態
Ready — dataset 已就緒，需先定義 Gold Answer Set JSON schema 再開始 pipeline 開發

## 可合併的點子
- A1 (整體框架) 的 benchmark 建構子集——可獨立發表為 dataset/resource paper
- A1b (error taxonomy) 可使用本 benchmark 的 Level B/C 答案作為輸入
- A5 (MCQ option bias) 直接使用本 benchmark 的 with/without options 對比數據

## 來源筆記
drafts/archive/old-raw-2.md — 「把選擇題 canonicalize 成 open-form numerical task」、Gold Answer Set = {value_range, acceptable_assumptions, tolerance} 的設計源自此文件
