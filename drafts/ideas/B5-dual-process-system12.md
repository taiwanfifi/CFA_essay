# B5 雙過程金融推理系統
# Dual-Process Financial Reasoning (System 1 / System 2)

## 研究問題

受 Daniel Kahneman 的 Dual-Process Theory 啟發：人類的認知分為快速直覺的 System 1 與緩慢深思的 System 2。在 CFA 考試情境中，簡單的概念題或定義題只需 System 1（快速 zero-shot），而複雜的多步計算題或多概念整合題需要 System 2（完整的 RAG + CoT + 工具）。核心問題是：能否設計一個自適應系統，根據題目難度動態分配計算資源？最佳的信心閾值（觸發 System 2 的門檻）在哪裡？準確率與計算成本之間的 Pareto frontier 長什麼樣？

## 核心方法

**System 1: Fast Intuition（快思考）**
- 直接使用 LLM 進行 zero-shot 回答
- 同時輸出信心估計（使用 Self-Consistency Variance: 快速採樣 k=3 次，計算一致性）
- 若信心 >= threshold theta → 直接輸出答案（快速路徑）
- 若信心 < theta → 觸發 System 2（慢速路徑）

**System 2: Deliberate Reasoning（慢思考）**
- Step 1: RAG 知識檢索 — 使用現有 RAG pipeline 從 CFA_Extracted 檢索相關教材
- Step 2: Chain-of-Thought — 結構化逐步推理
- Step 3: Financial Calculator Tools — 如需計算，調用金融計算器
- Step 4: Self-Verification — 對推理結果進行合理性驗證

**Adaptive Threshold Optimization**
- 在 validation set 上掃描 theta 從 0.3 到 0.95
- 對每個 theta 計算：(a) System 1 分配比例 (b) 總準確率 (c) 總 token 成本
- 繪製 Pareto frontier：accuracy vs compute cost
- 找到 Pareto 最優的 theta 值

## 實驗設計

- **Exp 1: System 1 vs System 2 vs Dual-Process** — System 1 Only（全部 zero-shot）、System 2 Only（全部走完整 pipeline）、Dual-Process（自適應分配）。報告 Accuracy、Total Tokens、Accuracy-per-Token、Latency。
- **Exp 2: Threshold Sensitivity Analysis** — 掃描 theta 從 0.3 到 0.95（步進 0.05）。對每個 theta 報告 System 1 分配比例、準確率、token 消耗。繪製三軸圖。找到 Pareto 最優點。
- **Exp 3: 信心估計方法對比** — 作為 System 1 觸發器的信心估計：(a) Self-Consistency Variance (k=3) (b) Verbalized Confidence (c) Logit-based (僅 local 模型)。分析哪種信心估計最適合做 routing decision。
- **Exp 4: 題目難度 vs System 分配** — 人工標註題目難度（easy/medium/hard），分析 Dual-Process 系統是否確實將 hard 題分配給 System 2。計算 routing accuracy（是否「需要 System 2 的題目」確實被路由到 System 2）。

## 需要的積木

- ✅ RAG pipeline — 現有 4 種 RAG 實作（LangGraph, LangChain, LlamaIndex x2）
- ✅ CFA 測試資料集 — FinEval-CFA-Challenge (90), CFA-Easy (1,032)
- ✅ CFA 知識庫 — CFA_Extracted (1,124)
- ✅ LLM 推論環境 — Ollama local + OpenAI API
- ❌ 信心估計模組 — Self-Consistency Variance (k=3) 的快速實作
- ❌ Financial Calculator Tools — 至少需要 TVM、Bond calculator（可與 B6 共用）
- ❌ Threshold optimizer — 在 validation set 上自動搜尋最優 theta
- ❌ System 2 完整 pipeline — 整合 RAG + CoT + Calculator + Verification 的端到端流程
- ❌ 題目難度標註 — easy/medium/hard 分類（~15hr）

## 預期產出

- Dual-Process 系統準確率接近 System 2 Only（差距 < 2%），但計算成本降低 40-60%
- 預期約 50-60% 的 CFA 題目可由 System 1 正確回答
- Pareto frontier 圖：清晰展示 accuracy-cost trade-off 的最優邊界
- 最佳 theta 值預期在 0.6-0.8 之間（取決於模型與信心估計方法）
- Routing accuracy 分析：System 2 未被觸發卻答錯的題目（漏報分析）

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | 困難題測試 | 已就緒 |
| FinEval-CFA-Easy (1,032) | 主測試集（劃分 80% test / 20% validation） | 已就緒 |
| CFA_Extracted (1,124) | RAG 知識庫 | 已就緒 |

## 模型需求

- **System 1 LLM**: qwen3:32b 或 gpt-4o（需足夠強以在 zero-shot 時就有合理準確率）
- **System 2 LLM**: 同上（加上 RAG + Tool augmentation）
- **信心估計**: 需支援 temperature sampling（Ollama 與 OpenAI 皆可）

## 狀態

🔲 尚未開始 — 此為整合型研究，依賴多個積木的完成（RAG, Calculator, Confidence）

## 可合併的點子

- **B4 (Self-Consistency)** — Self-Consistency 的 agreement rate 直接作為 System 1 的信心估計
- **B6 (ReAct Financial Calculator)** — Calculator tools 作為 System 2 的計算組件
- **B3 (Self-Verification)** — Self-Verification 作為 System 2 最後一步的驗證機制
- **B2a (Dual-Agent)** — System 2 可以是一個完整的 Dual-Agent 系統

## 來源筆記

- docs/03-研究方向深度設計.md 方向 7：Dual-Process Financial Reasoning
- Kahneman, D. (2011). Thinking, Fast and Slow.
- Adaptive Computation in LLMs（Schuster et al., 2022; Del Corro et al., 2023）
