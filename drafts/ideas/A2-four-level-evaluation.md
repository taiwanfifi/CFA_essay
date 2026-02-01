# A2 四層級評估框架：從純 LLM 到 Agent+Tools
# 4-Level Evaluation Framework: From Pure LLM to Agent+Tools on CFA

## 研究問題

在評估 LLM 的 CFA 解題能力時，「模型本身的能力」與「系統整體的能力」被普遍混淆。Self-verification prompting、Chain-of-Thought、RAG 檢索、工具輔助計算——每加一層 inference-time augmentation，測量的對象就發生質變。但現有文獻幾乎不區分這些層級，導致不同論文的結果無法公平比較。更關鍵的發現是：Agent 框架（如 Aider、OpenHands）對小模型 (8-20B) 的 MCQ accuracy 幾乎沒有正向提升，甚至可能下降——因為它們解決的是完全不同類型的問題。本研究提出一個嚴格的四層級評估框架（Level 0-3），在相同模型、相同題目上系統性比較每個層級的效果，揭示各層級的「真實貢獻」與「適用邊界」。

## 核心方法

四個層級的嚴格定義如下。Level 0 (Pure LLM)：題目直接輸入模型，zero-shot，single-pass 輸出答案——這是最乾淨的 benchmark，測的是模型內建知識與即時推理能力。Level 1 (LLM + CoT)：加入 step-by-step reasoning prompt，但仍無外部工具、無額外回饋——學界普遍仍視為 LLM 推理能力的測量。Level 2 (LLM + Self-Verification)：模型先解題再自我檢查邏輯或重新驗算，但驗算仍為 LLM 自身用文字進行（非 deterministic tool）——這是 inference-time compute 的增加，性質介於 model 與 agent 之間。Level 3 (LLM + Agent + Tools)：模型可以呼叫外部工具（Python 計算器、RAG 檢索），有多輪互動，有 feedback loop——此時測量的是「模型 + 系統」的整合能力，不再是模型本身。

關鍵原則：accuracy 在每個 Level 獨立計算，不允許跨 Level 的資訊流動。Level 2 的 self-verification 如果修正了答案，修正前和修正後的答案都要記錄，但 accuracy 以修正後為準（因為 self-verification 本身就是 Level 2 的定義）。

## 實驗設計

1. 選定測試集：FinEval-CFA-Easy (1,032 題) + FinEval-CFA-Challenge (90 題)
2. 對每個模型，在 4 個 Level 上分別跑完整測試集：
   - Level 0: zero-shot, temperature=0, single-pass
   - Level 1: CoT prompt ("Let's think step by step"), temperature=0
   - Level 2: CoT + self-verification prompt ("Check your reasoning and correct if needed"), temperature=0
   - Level 3: ReAct agent with Python calculator tool + self-correction loop (max 3 iterations)
3. 記錄每個 Level 的 accuracy, token count, latency, cost
4. 計算 Level-over-Level lift: (accuracy_L(n) - accuracy_L(n-1)) per model per topic
5. 特別分析小模型 (< 10B) 在 Level 3 的表現是否下降（驗證 agent framework 對小模型的劣化效應）
6. 按 CFA 主題分析各 Level 的貢獻差異（計算題 vs 概念題 vs 倫理題）
7. 計算 accuracy-per-dollar 和 accuracy-per-token 的 efficiency frontier
8. 建立決策樹：給定模型規模與題目類型，推薦最佳 Level

## 需要的積木
- ✅ FinEval-CFA-Easy + CFA-Challenge datasets — 已下載
- ✅ OpenAI API (gpt-4o, gpt-4o-mini) — Level 0-3 均可使用
- ✅ Ollama local models — Level 0-2 直接可用
- ✅ 4 個 RAG 實作 (LangGraph Agent, LangChain Hybrid, LlamaIndex Standard, LlamaIndex Vector-only) — Level 3 的 RAG 組件
- ❌ 標準化 Level 2 self-verification prompt — 需設計不同的 verification strategy 並選定最佳版本
- ❌ Level 3 ReAct agent — 需整合 Python calculator + RAG 為統一 agent
- ❌ Cost/latency 計量工具 — 需精確記錄每次推論的 token 數與時間

## 預期產出
- `results/A2_level_comparison.json` — 4 Level x N models x M topics 的完整 accuracy 矩陣
- `results/A2_level_lift.json` — Level-over-Level lift 分析
- `results/A2_efficiency_frontier.json` — accuracy-per-dollar / accuracy-per-token 數據
- `figures/A2_level_comparison_bar.png` — 各模型在 4 Level 上的 accuracy 柱狀圖
- `figures/A2_small_model_degradation.png` — 小模型在 Level 3 的劣化效應圖
- `figures/A2_efficiency_frontier.png` — Pareto frontier 圖
- Table: decision matrix (model size x question type -> recommended Level)

## 資料需求
- FinEval-CFA-Easy: 全部 1,032 題
- FinEval-CFA-Challenge: 全部 90 題
- 每道題需標註題目類型（計算題/概念題/倫理題/分析題），可使用 GPT-4o 自動標註後人工校驗

## 模型需求
- OpenAI API: gpt-4o (大模型代表), gpt-4o-mini (中模型代表)
- Ollama large: qwen3:32b, qwen3:30b-a3b (本地大模型)
- Ollama medium: deepseek-r1:14b, llama3.1:8b (本地中模型)
- Ollama small: qwen3:4b, phi3.5:3.8b, llama3.2, gemma3 (小模型，驗證劣化效應)

## 狀態
Ready — 所有 dataset 與模型已就緒，需開發標準化 prompt template 與 Level 3 agent

## 可合併的點子
- A1/A1a (open-ended benchmark) 可作為 Level 0-3 的替代評測格式（MCQ vs open-ended 的 cross-comparison）
- A5 (MCQ option bias) 的 with/without options 可加入為 Level 0 的變體
- A4 (prompt sensitivity) 可分析每個 Level 的 prompt sensitivity 差異

## 來源筆記
drafts/archive/old-raw-2.md — Level 0-3 框架的完整定義源自此文件，包含「Agent 在 CFA benchmark 上幾乎不帶來正向提升」的關鍵洞察以及「你在測 agent 還是 model」的區分原則
