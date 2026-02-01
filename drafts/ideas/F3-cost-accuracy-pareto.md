# F3 CFA AI 系統的 Cost-Accuracy Pareto 分析
# Cost-Accuracy Pareto Analysis for CFA AI Systems

## 研究問題

構建一個能通過 CFA 考試的 AI 系統，需要花多少錢？現有研究僅關注準確率（accuracy），完全忽略了實際部署的經濟面向。然而，不同模型與推論策略的成本差異可達數個 order of magnitude：GPT-4o 的 API 費用 vs 本地 Ollama 的電費、single-pass 的快速推論 vs self-consistency 的多次取樣、zero-shot 的零額外成本 vs RAG 的 embedding + retrieval 成本。本研究將每個「模型 x 推論策略」組合視為一個 solution point，繪製 cost-accuracy Pareto frontier，回答實務問題：「給定預算限制，最佳的 CFA AI 系統配置是什麼？」

## 核心方法

定義四維指標空間：(1) accuracy（CFA 題目正確率）；(2) cost_per_question（每道題的美元成本，API 模型用 token pricing 計算，local 模型用電費 + 硬體折舊估算）；(3) latency_per_question（每道題的推論延遲，秒）；(4) total_cost_for_1000_questions（處理 1,000 題的總成本，模擬真實考試規模）。

每個 solution point 是一個 (model, inference_strategy) 組合。模型涵蓋所有可用模型；inference strategy 涵蓋：
- Zero-shot（baseline，最低成本）
- Chain-of-Thought（中等成本，增加 output tokens）
- Self-Consistency k=3/5/10（成本線性增長）
- RAG（額外 retrieval 成本）
- Agent with tools（多輪互動，成本最高）

核心產出是二維 Pareto chart（x=cost, y=accuracy），標記出 Pareto-optimal solutions（非被支配解）與 dominated solutions。

## 實驗設計

1. **Cost Model 建構**：
   - OpenAI API：根據官方 pricing，input/output token 分別計費
   - Ollama local：測量每道題的 GPU 時間，乘以硬體功耗估算電費（Apple Silicon 功耗 ~30-60W）
   - RAG 額外成本：embedding API call + vector DB query time
2. **Baseline Inference**：所有模型在 CFA-Easy (1,032 題) 上分別執行 zero-shot, CoT, self-consistency (k=3,5,10)
3. **延遲測量**：記錄每道題的 wall-clock time（含 API round-trip 或 local generation time）
4. **Pareto Analysis**：
   - 繪製 cost vs accuracy 二維 Pareto chart
   - 辨識 Pareto frontier 上的非被支配解
   - 計算每個 dominated solution 的 efficiency gap（距 frontier 的距離）
5. **預算情境分析**：
   - "$10 budget"：最佳配置是什麼？
   - "$100 budget"：最佳配置是什麼？
   - "$1000 budget"：最佳配置是什麼？
6. **Sensitivity Analysis**：API pricing 變動 +-20% 時 Pareto frontier 如何移動

## 需要的積木
- ✅ FinEval-CFA-Easy (1,032 題) — 主測試集
- ✅ FinEval-CFA-Challenge (90 題) — Hard subset
- ✅ Ollama local models — 完整規模梯度已安裝
- ✅ OpenAI API — gpt-4o, gpt-4o-mini 可用
- ❌ Cost measurement framework — 需建構 API cost tracker + local inference timer
- ❌ Pareto analysis toolkit — 需實作 Pareto dominance 判定與 frontier extraction
- ❌ Multi-strategy inference pipeline — 需支援 zero-shot / CoT / self-consistency / RAG 的統一執行框架

## 預期產出
- `results/F3_cost_accuracy_raw.csv` — 所有 (model, strategy) 組合的 cost/accuracy/latency 數據
- `results/F3_pareto_frontier.json` — Pareto-optimal solutions 列表
- `figures/F3_pareto_chart.png` — Cost vs Accuracy Pareto frontier 視覺化
- `figures/F3_latency_accuracy_chart.png` — Latency vs Accuracy 二維圖
- `figures/F3_budget_scenarios.png` — 不同預算下的最佳配置推薦
- Table: 各 solution point 的完整指標（accuracy, cost, latency, dominated/non-dominated）
- 實務指南：不同預算下的 CFA AI 系統配置建議

## 資料需求
| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Easy (1,032) | 主測試集 | 已就緒 |
| FinEval-CFA-Challenge (90) | Hard subset（驗證 Pareto 在難題上是否移動） | 已就緒 |

## 模型需求
- **Local (Ollama)**: phi3.5:3.8b, qwen3:4b, llama3.1:8b, deepseek-r1:14b, qwen3:30b-a3b, qwen3:32b
- **API**: gpt-4o (~$2.50/$10.00 per 1M tokens), gpt-4o-mini (~$0.15/$0.60 per 1M tokens)
- 每個模型需跑多種 inference strategy，總 API 成本預估 $50-150

## 狀態
Ready — 需先完成 F2 的 baseline inference（共用推論數據），再疊加 cost/latency 量測

## 可合併的點子
- **F2 (Scaling Law)** — F2 的準確率數據是 F3 的直接輸入
- **C1 (RAG Comparison)** — C1 的四種 RAG 結果可作為 F3 的 RAG strategy data points
- **B1 (Five-Stage Reasoning)** — Structured pipeline 作為高成本高準確率的 solution point 加入 Pareto

## 來源筆記
- OpenAI pricing page (2025): API token pricing 用於成本計算
- Multi-objective optimization 文獻：Pareto frontier 的標準定義與視覺化方法
- docs/03-研究方向深度設計.md — 方向 7 的 cost-benefit 分析思路
