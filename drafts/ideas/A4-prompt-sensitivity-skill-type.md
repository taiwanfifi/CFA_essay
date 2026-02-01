# A4 Prompt 敏感度作為技能類型測量
# Prompt Sensitivity as Measurement of Skill Type on CFA

## 研究問題

同一道 CFA 題目，僅改變 prompt 的表述方式（如「請用 CFA 考生口吻回答」vs「請用資深投資顧問口吻回答」vs「直接給答案不要解釋」），模型的準確率可能出現劇烈波動——某些題目從 90% 掉到 40%，而另一些題目不受影響。這種 prompt sensitivity 的差異不是噪音，而是一個有意義的信號：穩定的準確率意味著模型掌握的是 explicit/formalizable skill（如公式計算），不穩定的準確率意味著模型面對的是 tacit/context-dependent skill（如倫理判斷、情境推理）。本研究利用 prompt sensitivity 作為 operationalized measure，系統性地將 CFA 題目分類為 explicit skill vs tacit skill，並直接產出 CFA Ability Matrix 的核心數據。

## 核心方法

核心實驗設計是 multi-prompt evaluation：對同一道 CFA 題目使用 5+ 種不同的 prompt format，記錄每種 format 下的正確率。Prompt 變體包括：(P1) Zero-shot direct：只給題目，要求直接回答；(P2) CoT explicit：加入 "Let's think step by step"；(P3) Role-play CFA candidate：「你是一位正在準備 CFA 考試的考生」；(P4) Role-play senior analyst：「你是一位擁有 20 年經驗的資深投資分析師」；(P5) Minimal：「Answer with just the letter」；(P6) Adversarial reframe：改寫題目表述但保持語義不變。

對每道題目計算 prompt sensitivity score = std_dev(accuracy across prompts)。Score 接近 0 表示高度穩定（explicit skill），score 遠離 0 表示高度不穩定（tacit skill）。然後以 topic-level aggregation 觀察：哪些 CFA 主題整體上屬於 explicit skill（如 Quantitative Methods, Fixed Income 計算題），哪些屬於 tacit skill（如 Ethics, Portfolio Management 情境題）。

這個分析直接銜接人力資本理論（Becker, Spence）：explicit skill 是「可被 AI 低成本複製」的能力，tacit skill 是「即使 AI 也難以穩定複製」的能力。Prompt sensitivity 因此成為「專業證照鑑別力是否仍然存在」的實證證據。

## 實驗設計

1. 設計 6 種 prompt 變體（P1-P6），確保語義等價但表述風格不同
2. 對每個模型 x 每道題目 x 每種 prompt 進行推論（total: ~N_models x 1032 x 6 次推論）
3. 對於 API 模型使用 temperature=0；對於 local 模型使用 greedy decoding
4. 計算 per-question prompt sensitivity score = std(correct_P1, correct_P2, ..., correct_P6)
5. 計算 per-topic prompt sensitivity score = mean(per-question scores within topic)
6. 建立 CFA Ability Matrix: Topic (rows) x {mean_accuracy, prompt_sensitivity, skill_type} (columns)
7. 使用 clustering（k-means 或 hierarchical）將題目自動分群為 explicit vs tacit
8. 對比不同模型的 prompt sensitivity profile——大模型是否比小模型更穩定？
9. 交叉驗證：人工評估 50 題的 explicit/tacit 分類，與自動分群結果比對

## 需要的積木
- ✅ FinEval-CFA-Easy dataset (1,032 題) — 已下載，含主題標籤
- ✅ OpenAI API (gpt-4o, gpt-4o-mini) — 用於多 prompt 推論
- ✅ Ollama local models — 多 prompt 推論
- ❌ Multi-prompt evaluation harness — 需開發自動化腳本，對每道題跑 6 種 prompt 並記錄結果
- ❌ Prompt sensitivity 計算模組 — 需實作 per-question 和 per-topic 的 sensitivity 指標
- ❌ CFA topic classification — 需為每道題標註 CFA 主題（可用 GPT-4o 自動標註）

## 預期產出
- `results/A4_multi_prompt_raw.json` — 完整的 model x question x prompt 結果矩陣
- `results/A4_prompt_sensitivity_scores.csv` — 每道題和每個 topic 的 sensitivity score
- `results/A4_ability_matrix.csv` — CFA Ability Matrix (topic x accuracy x sensitivity x skill_type)
- `results/A4_clustering_results.json` — explicit vs tacit 自動分群結果
- `figures/A4_sensitivity_by_topic.png` — 各 CFA 主題的 prompt sensitivity 柱狀圖
- `figures/A4_sensitivity_vs_accuracy.png` — Sensitivity vs Mean Accuracy 的散點圖
- `figures/A4_model_size_vs_stability.png` — 模型規模 vs prompt stability 圖
- Table: CFA Ability Matrix (可直接放入論文)

## 資料需求
- FinEval-CFA-Easy: 全部 1,032 題（6 prompt x N models = 大量推論）
- FinEval-CFA-Challenge: 90 題（作為 hard subset 的 sensitivity 分析）
- API 費用預估：gpt-4o 1032 x 6 prompts x ~500 tokens = ~3M tokens，約 $15-30 per run

## 模型需求
- OpenAI API: gpt-4o（大模型）, gpt-4o-mini（中模型）
- Ollama local: qwen3:32b, deepseek-r1:14b, llama3.1:8b（本地模型對比）
- Ollama small: qwen3:4b, phi3.5:3.8b（小模型，預期 sensitivity 更高）
- 至少 5 個模型以確保 cross-model 分析的統計力

## 狀態
Ready — 所有 dataset 與模型已就緒，需開發 multi-prompt evaluation harness

## 可合併的點子
- A3 (CFA as AGI benchmark) 的能力維度分析可直接使用本研究的 CFA Ability Matrix
- A2 (4-level evaluation) 可在每個 Level 上分別計算 prompt sensitivity，觀察 Level 是否影響 stability
- A5 (MCQ option bias) 的 option bias 可與 prompt sensitivity 交叉分析（高 sensitivity 題目是否也有高 option bias）
- 本研究的 CFA Ability Matrix 直接服務於人力資本論文（drafts/archive/old-raw-1.md 中的 G1 方向）

## 來源筆記
drafts/archive/old-raw-1.md — 「找出 AI 表現高度不穩定、對 prompt 敏感的能力 → 論證後者更接近 tacit skills」的方法論，以及完整的 CFA 能力矩陣設計（Layer 1-3），均源自此文件
