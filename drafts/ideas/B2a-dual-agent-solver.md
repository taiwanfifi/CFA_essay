# B2a 雙代理 CFA 解題系統
# Dual-Agent CFA Solver (Knowledge Agent + Calculator Agent)

## 研究問題

CFA 題目同時要求「金融知識檢索」與「數值精確計算」兩種截然不同的能力。單一 LLM 必須同時承擔兩項任務，容易在其中一項上出錯。若將兩種能力拆分為專門的 Agent，由 Orchestrator 動態調度，能否系統性地超越單一 LLM 的表現？此外，每個 Agent 的獨立貢獻能否透過 ablation study 精確量化？

## 核心方法

基於 LangGraph（已有 RAG 實作基礎）建構雙代理系統：

**Knowledge Agent（知識代理）**
- 使用 RAG pipeline 檢索相關 CFA 教材內容
- 負責回答概念性、原則性、倫理判斷類問題
- 從 CFA_Extracted 的 material/scenario 欄位建構知識庫

**Calculator Agent（計算代理）**
- 封裝金融計算器（TVM、Bond pricing、Portfolio statistics 等）
- 負責所有需要精確數值計算的環節
- 接收結構化參數，回傳精確計算結果

**Orchestrator（調度器）**
- 接收題目後判斷需要調用哪個 Agent（或兩者皆需）
- 決策邏輯：分析題目是否包含數值計算需求、是否需要知識檢索
- 可使用 LLM 作為 router，也可使用 rule-based classifier

## 實驗設計

- **Exp 1: Single LLM vs Dual-Agent** — 相同題目上比較單一 LLM (zero-shot / CoT) 與 Dual-Agent 系統的準確率。按題目類型（概念題/計算題/混合題）分析差異。
- **Exp 2: Agent Ablation Study** — (a) 僅 Knowledge Agent (b) 僅 Calculator Agent (c) 完整 Dual-Agent。量化每個 Agent 的獨立貢獻與交互效應。
- **Exp 3: Orchestrator 決策品質** — 評估 Orchestrator 是否正確分派任務。錯誤類型：不該呼叫 Calculator 卻呼叫、該呼叫 Knowledge Agent 卻未呼叫。
- **Exp 4: 不同 RAG backend 對比** — 使用現有 4 個 RAG 實作（LangGraph, LangChain Hybrid, LlamaIndex, LlamaIndex Vector-only）作為 Knowledge Agent 後端進行對比。

## 需要的積木

- ✅ LangGraph 框架 — 已有 RAG 實作，可擴展為 Agent 架構
- ✅ RAG pipeline (x4) — LangGraph, LangChain Hybrid, LlamaIndex, LlamaIndex Vector-only
- ✅ CFA 知識庫 — CFA_Extracted (1,124 條含 material context)
- ✅ 測試資料集 — FinEval-CFA-Challenge (90), CFA-Easy (1,032)
- ❌ Calculator Agent 實作 — 需開發金融計算器工具集（~30hr，可與 B6 共用）
- ❌ Orchestrator routing 邏輯 — LLM-based 或 rule-based 分派器
- ❌ 題目類型標註 — 需標註概念題/計算題/混合題（~15hr）

## 預期產出

- Dual-Agent 系統在計算題上顯著優於 Single LLM（預期 +15-20%）
- 在概念題上 Dual-Agent 與 Single LLM 表現相近
- 混合題（需同時使用知識與計算）為 Dual-Agent 最大優勢場景
- Orchestrator routing accuracy 預期 ~85-90%

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | 困難題測試 | 已就緒 |
| FinEval-CFA-Easy (1,032) | 一般題測試 | 已就緒 |
| CFA_Extracted (1,124) | Knowledge Agent 知識庫 | 已就緒 |
| CRA-Bigdata (1,472) | 擴展測試（可選） | 已就緒 |

## 模型需求

- **Orchestrator**: gpt-4o 或 qwen3:32b（需要較強的 routing 判斷力）
- **Knowledge Agent LLM backend**: 任意模型（測試多種組合）
- **Calculator Agent**: 純程式化工具，不需要 LLM

## 狀態

🔲 尚未開始 — LangGraph Agent 框架可快速搭建，Calculator 開發為主要工作量

## 可合併的點子

- **B2b (Quad-Agent)** — B2a 的自然擴展，加入 Ethics Agent + Verification Agent
- **B6 (ReAct Financial Calculator)** — Calculator Agent 可直接復用 B6 的工具集
- **B1 (5-Stage Pipeline)** — 每個 Stage 可對應不同 Agent 的責任範圍

## 來源筆記

- 新構想，基於現有 LangGraph RAG 實作的自然擴展
- Multi-Agent Systems (MAS) 在 LLM 領域的最新趨勢（AutoGen, CrewAI）
- docs/03 方向 5 的 Tool Augmentation 概念
