# F4 角色扮演 Prompt 對金融推理的影響
# Role-Playing Prompts for Financial Reasoning: Does Identity Shape LLM Performance on CFA?

## 研究問題

Prompt engineering 文獻已證實 system prompt 中的角色設定會影響 LLM 的回答品質，但現有研究多集中於通用任務（寫作、程式設計），缺乏在 domain-specific 高難度推理任務上的系統性研究。本研究聚焦一個直覺但未被驗證的問題：當 LLM 被賦予不同金融角色身份時（如 CFA 考生、資深分析師、金融學教授），其 CFA 題目作答表現是否存在顯著差異？更深入地，哪種角色在哪類主題上表現最佳？這不僅是 prompt engineering 的實證貢獻，也觸及 LLM 如何利用 role identity 調整其 reasoning strategy 的理論問題。

## 核心方法

設計五種角色 prompt（含一個無角色 baseline），在完全相同的題目上進行 controlled experiment：

1. **Baseline（無角色）**：直接提問，不設定任何角色身份
2. **Student Role**："You are a CFA Level II candidate preparing for the exam. Think step by step as you would during the actual exam."
3. **Expert Role**："You are a senior investment analyst with 20 years of experience in portfolio management. Apply your professional expertise."
4. **Professor Role**："You are a finance professor at a top university. Explain your reasoning as if teaching a class, then provide your answer."
5. **Advisor Role**："You are a financial advisor explaining the answer to a client who has basic financial literacy. Be clear and precise."

每種角色的 prompt 長度與資訊量經過控制，僅改變角色身份描述，不改變任務指令。測量三個維度：(1) accuracy（最終答案正確率）；(2) reasoning quality（推理過程的邏輯完整性，由 GPT-4o 評分）；(3) explanation clarity（解釋的可讀性與教育價值，由 GPT-4o 評分）。

## 實驗設計

1. **Prompt 設計與預測試**：設計五種角色 prompt，在 20 題 pilot set 上測試確保 prompt 長度均衡且角色差異清晰
2. **主實驗**：對 CFA-Challenge (90 題) 與 CFA-Easy (1,032 題) 進行完整推論
   - 測試模型：gpt-4o, gpt-4o-mini, qwen3:32b, llama3.1:8b, deepseek-r1:14b
   - 每個模型 x 每種角色 = 一組完整推論
   - temperature=0, single pass
3. **Accuracy 分析**：
   - Overall accuracy per role per model
   - Topic-level accuracy：哪種角色在哪個 CFA 主題最強
   - Statistical significance：Cochran's Q test + post-hoc McNemar's test
4. **Reasoning Quality 評估**：
   - 使用 GPT-4o-as-judge，對每個回答的推理過程評分（1-5 scale）
   - 評分維度：logical coherence, formula correctness, completeness of reasoning steps
5. **Explanation Clarity 評估**：
   - 同樣使用 GPT-4o-as-judge，評估解釋的清晰度與教育價值
   - 測試 Professor Role 是否犧牲效率換取更好的解釋
6. **交互效應分析**：Role x Topic x Model 的三因子分析，尋找最佳角色-主題配對

## 需要的積木
- ✅ FinEval-CFA-Challenge (90 題) — 已下載
- ✅ FinEval-CFA-Easy (1,032 題) — 已下載
- ✅ Ollama local models — qwen3:32b, llama3.1:8b, deepseek-r1:14b
- ✅ OpenAI API — gpt-4o（推論 + judge）, gpt-4o-mini（推論）
- ❌ Role prompt template library — 需精心設計五種角色 prompt（已有初稿，需 pilot test 驗證）
- ❌ LLM-as-judge evaluation pipeline — 需實作 GPT-4o 自動評分系統（含 scoring rubric）
- ❌ Statistical analysis script — Cochran's Q, McNemar's test, three-way interaction analysis

## 預期產出
- `results/F4_role_accuracy_matrix.csv` — Role x Model x Topic 三維準確率數據
- `results/F4_reasoning_quality_scores.json` — 推理品質評分（per question, per role, per model）
- `figures/F4_role_accuracy_heatmap.png` — Role x Topic 準確率熱力圖
- `figures/F4_role_radar_chart.png` — 各角色在不同指標上的雷達圖
- `figures/F4_best_role_per_topic.png` — 每個 CFA 主題的最佳角色推薦
- Table: statistical significance 結果
- 實務建議：CFA 考試 AI 輔助系統的最佳角色配置策略

## 資料需求
| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | Hard test set | 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | 已就緒 |

## 模型需求
- **Local (Ollama)**: qwen3:32b, llama3.1:8b, deepseek-r1:14b（三種規模）
- **API**: gpt-4o（推論 + LLM-as-judge）, gpt-4o-mini（推論）
- API 成本預估：5 roles x 2 models x ~1,100 題 x ~$0.01/題 = ~$110；加上 judge 評分 ~$50

## 狀態
Ready — 低技術門檻，主要工作在 prompt 設計與評估框架。可在 1-2 週內完成實驗。

## 可合併的點子
- **F1 (Domain vs General)** — Role prompt 可疊加在 domain vs general 比較之上（是否 domain model + expert role 有加乘效果？）
- **B1 (Five-Stage Reasoning)** — Professor Role 的輸出天然接近 structured reasoning，可與 B1 的 stage-wise 分析交叉比較
- **A4 (Prompt Sensitivity)** — F4 是 prompt sensitivity 的一個特殊子集，聚焦 role identity 這個維度

## 來源筆記
- Zheng et al. (2023) "Judging LLM-as-a-Judge" — LLM-as-judge 方法論的基礎
- Salewski et al. (2024) "In-Context Impersonation Reveals LLMs' Strengths and Biases" — role-playing 對 LLM 表現的影響
- docs/03-研究方向深度設計.md — 方向 4 提及的 prompt engineering 系統性研究
