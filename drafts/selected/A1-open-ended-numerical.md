# A1 開放式數值推理基準與錯誤歸因系統
# Open-Ended Numerical Reasoning Benchmark for CFA with Structured Error Attribution

## 研究問題

現有 CFA benchmark 幾乎全部採用 MCQ 選擇題格式，但選項本身會洩漏答案的分布方向——這在測試理論中稱為 answer-space restriction bias。例如，選項中的量級提示（0.1 / 1 / 10 / 100）讓模型不需要真正計算就能推斷 order of magnitude；符號提示（全正或有負）進一步縮小搜索空間。這導致 MCQ 格式系統性地高估模型的金融推理能力，尤其對小模型更為明顯。本研究提出：移除選項、要求 LLM 直接輸出數值答案，並建立三層判定機制與結構化錯誤歸因系統，以更真實地衡量模型的 CFA 解題能力。

## 核心方法

第一步是將現有 CFA MCQ 題目轉換為 open-ended numerical reasoning 格式。不是簡單刪除選項，而是需要對每道題目定義 Gold Answer Set = {value_range, acceptable_assumptions, tolerance}，處理金融領域特有的模糊性（如 annual vs continuous compounding、ACT/365 vs ACT/360、不同 rounding policy）。

第二步是設計三層判定機制取代傳統的對/錯二分法。Level A (Exact/Acceptable Match)：數值在 tolerance 內且假設合理，記為 correct。Level B (Directionally Correct)：符號正確、order of magnitude 正確、但使用了不同的合理假設，accuracy 記為 wrong 但單獨統計。Level C (Incorrect)：邏輯錯誤、公式錯誤、單位錯誤等真正的錯誤。accuracy = #Level A / total，但額外報告 Level B 與 Level C 的比例及分布。

第三步是 structured error attribution：對所有非 Level A 的回答，分析錯誤源頭——是 formula selection error、numerical extraction error、calculation error、還是 assumption mismatch。這裡使用 post-hoc error explanation：請 LLM 解釋為什麼它的答案與正解不一致，但不將修正後的答案計入 accuracy（否則測的是 agent 而非 model）。

## 實驗設計

1. 從 FinEval-CFA-Easy (1,032 題) 中篩選所有含數值計算的題目，移除選項，建構 open-ended 版本
2. 為每道題定義 Gold Answer Set（包含 acceptable_assumptions 與 tolerance）
3. 對所有可用模型進行推論，收集 first-pass 答案（不允許修正）
4. 使用三層判定機制分類所有回答為 Level A / B / C
5. 對 Level B 和 Level C 進行 error attribution 分類
6. 建立 CFA Topic x Error Type 的二維熱力圖
7. 比較 MCQ 格式 vs open-ended 格式的 accuracy 差距（即 option bias 的量化）

## 需要的積木
- ✅ FinEval-CFA-Easy dataset (1,032 題) — 已下載，含 CFA 主題標籤
- ✅ CFA_Extracted dataset (1,124 題) — 含 material/scenario/exhibit 欄位可用於 Gold Answer Set 建構
- ✅ OpenAI API (gpt-4o) — 用於 error attribution 的 LLM-as-judge
- ❌ Gold Answer Set 建構工具 — 需為每道計算題定義 value_range + acceptable_assumptions + tolerance
- ❌ 三層判定評分器 — 需實作 exact match / tolerance match / directional match 的自動評分邏輯
- ❌ Error attribution 分類器 — 需設計 prompt 讓 GPT-4o 進行結構化錯誤歸因

## 預期產出
- `results/A1_accuracy_comparison.json` — MCQ vs open-ended accuracy 對比（per model, per topic）
- `results/A1_three_tier_distribution.json` — Level A/B/C 分布（per model, per topic）
- `results/A1_error_attribution_matrix.csv` — CFA Topic x Error Type 熱力圖數據
- `figures/A1_option_bias_heatmap.png` — 選項偏差量化視覺化
- `figures/A1_error_attribution_sankey.png` — 錯誤歸因流向圖
- Table: accuracy drop per topic (MCQ -> open-ended)

## 資料需求
- FinEval-CFA-Easy: 全部 1,032 題（篩選計算題後預估 400-500 題）
- CFA_Extracted: 1,124 題的 material 欄位用於輔助 Gold Answer Set 建構
- FinEval-CFA-Challenge: 90 題作為高難度子集

## 模型需求
- OpenAI API: gpt-4o（主力）, gpt-4o-mini（成本對比）
- Ollama local: qwen3:32b, qwen3:30b-a3b, deepseek-r1:14b, llama3.1:8b
- 小模型對比: qwen3:4b, phi3.5:3.8b, gemma3

## 狀態
Ready — 所有 dataset 已就緒，需開發 Gold Answer Set 建構工具與三層評分器

## 可合併的點子
- A1a (benchmark construction) + A1b (error taxonomy) 是本點子的兩個可獨立拆分方向
- A5 (MCQ option bias) 的實驗是本研究的子集（with vs without options 的比較）
- A2 (4-level evaluation) 的 Level 0/1 直接使用本研究的 open-ended 格式

## 來源筆記
drafts/archive/old-raw-2.md — 「把回答題目的規格從選擇題變成 open questions」的完整討論，包含三層判定機制、Gold Answer Set 設計、post-hoc error attribution 方法論
