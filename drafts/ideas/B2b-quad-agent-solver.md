# B2b 四代理 CFA 解題系統
# Quad-Agent CFA Solver (Knowledge + Calculator + Ethics + Verification)

## 研究問題

B2a 的雙代理架構（Knowledge + Calculator）僅覆蓋知識檢索與數值計算。然而 CFA 考試有兩個額外的獨特需求：(1) Ethics 與 Professional Standards 題目需要規範性判斷而非事實性推理，(2) 所有答案都需要合理性驗證以避免明顯錯誤。能否透過加入 Ethics Agent 與 Verification Agent，建構完整的四代理系統？更重要的是，能否透過系統性的 ablation study（1/2/3/4-agent 組態）精確量化每個 Agent 的邊際貢獻？

## 核心方法

在 B2a 基礎上擴展為四代理架構：

**Knowledge Agent（知識代理）** — 同 B2a，使用 RAG 檢索 CFA 教材知識

**Calculator Agent（計算代理）** — 同 B2a，封裝金融計算器工具

**Ethics Agent（倫理代理）**
- 專門處理 CFA Ethics & Professional Standards 題目
- 內建 CFA Institute Code of Ethics 與 Standards of Professional Conduct (I-VII) 的結構化知識
- 使用 rule-based + LLM hybrid 判斷：先匹配相關 Standard，再由 LLM 推理具體情境

**Verification Agent（驗證代理）**
- 接收其他 Agent 的回答，進行獨立驗證
- 三項檢查：(a) 數值合理性（結果是否在合理範圍）、(b) 邏輯一致性（推理步驟是否自洽）、(c) 選項排除（是否能排除明顯錯誤選項）
- 若驗證失敗，觸發 retry（要求原 Agent 重新作答）

**Enhanced Orchestrator** — 根據題目特徵決定調用哪些 Agent 及調用順序

## 實驗設計

- **Exp 1: Full Ablation Study (核心實驗)**
  - 1-agent configs: K-only, C-only, E-only, V-only
  - 2-agent configs: K+C (=B2a), K+E, K+V, C+V, C+E, E+V
  - 3-agent configs: K+C+E, K+C+V, K+E+V, C+E+V
  - 4-agent config: K+C+E+V (full system)
  - 量化每個 Agent 的邊際貢獻（Shapley value 分析）
- **Exp 2: Ethics Agent 專項評估** — 在 Ethics 類題目子集上，比較有/無 Ethics Agent 的準確率差異。
- **Exp 3: Verification Agent 效果分析** — 統計 Verification Agent 的介入頻率、修正成功率、false alarm rate。
- **Exp 4: Agent 間通訊成本分析** — 測量 total tokens、latency、API cost。分析 agent 數量增加的邊際成本 vs 邊際收益。

## 需要的積木

- ✅ LangGraph 框架 — 已有基礎，支援多 Agent 編排
- ✅ RAG pipeline — 現有 4 種實作可作為 Knowledge Agent 後端
- ✅ CFA 知識庫與測試資料 — CFA_Extracted, FinEval 系列
- ❌ Calculator Agent — 金融計算器工具（與 B2a/B6 共用開發）
- ❌ Ethics Agent — CFA Code of Ethics 結構化知識庫 + 規範推理 prompt
- ❌ Verification Agent — 合理性驗證邏輯（數值範圍、邏輯一致性、選項排除）
- ❌ Ethics 題目標註 — 需標記哪些題目屬於 Ethics & Professional Standards（~5hr）
- ❌ Shapley value 計算腳本 — 用於量化各 Agent 貢獻

## 預期產出

- 完整的 Agent ablation 結果表（~15 種組態），展示每個 Agent 的邊際貢獻
- 預期 Verification Agent 修正成功率 ~30-50%（在被攔截的錯誤中）
- 預期 Ethics Agent 在 Ethics 題目上帶來 +10-15% 準確率提升
- 計算成本分析：4-agent 系統約為 single LLM 的 3-5 倍 token 消耗
- Shapley value 分析揭示各 Agent 的相對重要性排序

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | 困難題測試 | 已就緒 |
| FinEval-CFA-Easy (1,032) | 一般題測試 | 已就緒 |
| CFA_Extracted (1,124) | Knowledge Agent + Ethics Agent 知識庫 | 已就緒 |
| CRA-Bigdata (1,472) | 擴展測試 | 已就緒 |

## 模型需求

- **Orchestrator**: gpt-4o（需要最強的路由判斷能力）
- **各 Agent LLM**: qwen3:32b 或 llama3.1:8b（測試不同規模）
- **Verification Agent**: 可使用與原 Agent 不同的模型（cross-model verification）

## 狀態

🔲 尚未開始 — 建議先完成 B2a 再擴展至 B2b

## 可合併的點子

- **B2a (Dual-Agent)** — B2b 是 B2a 的直接擴展，實驗結果互相對照
- **B3 (Self-Verification)** — Verification Agent 可視為外化版的 Self-Verification
- **B1 (5-Stage Pipeline)** — Agent 分工可對應五階段的不同 Stage

## 來源筆記

- B2a 的自然擴展構想
- CFA Ethics 在考試中佔比 15-20%，值得專門處理
- Shapley value 在 explainable AI 中的應用（Lundberg & Lee, 2017）
