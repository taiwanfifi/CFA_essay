# A5 MCQ 選項偏差量化
# MCQ Option Bias Quantification on CFA Benchmarks

## 研究問題

MCQ 選項本身是否為 LLM 提供了不公平的「拐杖」（crutch effect）？在測試理論中這稱為 answer-space restriction bias：選項洩漏了答案的量級（0.1/1/10/100 的 order of magnitude）、符號方向（全正或有負）、以及排除不合理答案的策略性線索。這意味著 MCQ 格式系統性地高估了 LLM 的金融推理能力。但這個 bias 到底有多大？不同模型的 bias 是否一致？不同 CFA 主題的 bias 是否有差異？本研究通過一個極其簡潔的實驗設計——同一組題目分別以有選項和無選項格式測試——精確量化 option bias，並分析其在模型、主題、題目類型三個維度上的分布。

## 核心方法

實驗設計極其直接：每道 CFA 題目以兩種格式呈現給同一模型。Format A (MCQ)：標準選擇題格式，含 A/B/C/D 四個選項，模型輸出選項字母。Format B (Open-ended)：移除所有選項，要求模型直接輸出答案（數值、概念名稱、或判斷）。對 Format B 的答案評判使用 A1a 的 tolerance-aware matching。

核心指標是 option_bias = accuracy_with_options - accuracy_without_options。正值表示選項提供了「拐杖」，數值越大表示模型越依賴選項線索而非真實理解。我們在三個維度上分解 option_bias：(1) per-model：哪些模型最依賴選項？假說是小模型的 option bias 更大；(2) per-topic：哪些 CFA 主題的 option bias 最大？假說是計算題 > 概念題 > 倫理題；(3) per-question-type：計算題 vs 定義題 vs 情境分析題的 bias 差異。

進一步分析 option bias 的來源機制：(a) elimination bias——模型是否使用排除法而非正向推理；(b) anchoring bias——選項的數值是否錨定了模型的計算方向；(c) format familiarity bias——模型在 MCQ 訓練數據上的 overfitting。通過分析模型的 reasoning chain（CoT 輸出），可以部分辨別這三種機制。

## 實驗設計

1. 使用 FinEval-CFA-Easy 全部 1,032 題作為主要測試集
2. 為每道題準備兩個版本：Format A (with options) 和 Format B (without options)
3. Format B 的答案評判：數值題使用 tolerance matching，概念題使用 semantic matching (GPT-4o judge)
4. 對每個模型分別跑 Format A 和 Format B，均使用 temperature=0
5. 計算 overall option_bias 和 per-topic option_bias
6. 按模型規模繪製 option_bias vs model_size 曲線
7. 分析 CoT 推理過程：在 Format A 中有多少比例的推理提及了選項排除策略
8. Paired statistical test: 對每道題的 correct/incorrect 結果做 McNemar's test，確認 bias 的統計顯著性
9. 分析「Format A 對但 Format B 錯」的題目特徵（這些題目最能揭示 option bias 機制）

## 需要的積木
- ✅ FinEval-CFA-Easy dataset (1,032 題) — 已下載，含選項
- ✅ OpenAI API (gpt-4o, gpt-4o-mini) — 兩種 format 的推論
- ✅ Ollama local models — 兩種 format 的推論
- ❌ Option removal script — 需自動從題目中移除選項並格式化為 open-ended prompt
- ❌ Open-ended answer evaluator — 需處理數值 tolerance matching 和概念 semantic matching
- ❌ CoT elimination strategy detector — 需分析推理文本中是否使用了排除法

## 預期產出
- `results/A5_option_bias_overall.json` — 每個模型的 overall option bias
- `results/A5_option_bias_by_topic.csv` — Topic x Model 的 option bias 矩陣
- `results/A5_option_bias_by_type.csv` — Question Type x Model 的 option bias 矩陣
- `results/A5_mcnemar_tests.json` — 每道題的 McNemar's test 結果
- `results/A5_elimination_strategy_rate.json` — CoT 中使用排除法的比例
- `figures/A5_bias_by_model_size.png` — Model size vs option bias 曲線
- `figures/A5_bias_by_topic_heatmap.png` — Topic x Model 的 option bias 熱力圖
- `figures/A5_format_a_only_correct.png` — 「有選項才對」的題目特徵分析
- Table: top-10 highest option bias topics with example questions

## 資料需求
- FinEval-CFA-Easy: 全部 1,032 題（Format A + Format B = 2,064 次推論 per model）
- FinEval-CFA-Challenge: 90 題（hard subset 的 option bias 分析）
- CFA_Extracted: 用於題目類型標註的輔助資訊
- API 費用預估：gpt-4o 2064 x ~500 tokens x N_models，約 $20-50 total

## 模型需求
- OpenAI API: gpt-4o, gpt-4o-mini
- Ollama large: qwen3:32b, qwen3:30b-a3b
- Ollama medium: deepseek-r1:14b, llama3.1:8b
- Ollama small: qwen3:4b, phi3.5:3.8b, llama3.2, gemma3
- 需覆蓋 2B-200B+ 的模型規模以驗證 option bias 與 model size 的關係

## 狀態
Ready — 所有 dataset 與模型已就緒，最簡單的實驗之一，可立即開始

## 可合併的點子
- A1/A1a (open-ended benchmark) — A5 是 A1 的一個聚焦子實驗，A1 的 MCQ vs open-ended 比較直接產出 A5 的數據
- A2 (4-level evaluation) — 可在 Level 0 上同時報告 MCQ 和 open-ended 結果
- A4 (prompt sensitivity) — option bias 和 prompt sensitivity 可能高度相關，值得交叉分析
- A3 (CFA as AGI benchmark) — option bias 的存在可能影響 CFA 與其他 benchmark 的相關性解讀

## 來源筆記
drafts/archive/old-raw-2.md — 「給選項本身就洩漏了答案的分佈方向」、answer-space restriction bias 的詳細討論、GSM8K 去選項後準確率大幅下降的先例引用，以及「選項是拐杖」的核心論點均源自此文件
