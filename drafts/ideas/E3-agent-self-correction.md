# E3 AI 能否診斷自己的錯誤？
# Agent-Based Error Self-Correction: Meta-Cognitive Capability of Financial LLMs

## 研究問題

當 LLM 在 CFA 題目上答錯後，如果告訴它正確答案，它能否準確地「回頭看」自己的錯誤推理過程，並正確辨識出自己到底是 Knowledge Gap、Misapplication、Calculation Error 還是 Distractor Confusion？這不是關於「修正答案」的研究（答案已經錯了），而是關於 meta-cognitive capability——LLM 是否具備自我診斷的能力。若 AI 能準確自我診斷，它就能主動請求對應的幫助（知識不足就要求 RAG、計算出錯就要求 calculator），這對 agent-based 系統的設計具有根本性意義。

## 核心方法

設計 Self-Diagnosis Protocol，分三步驟：

**Step 1：收集錯誤回答**
- 模型在 CFA 題目上作答，收集所有錯誤回答及完整 reasoning trace

**Step 2：Self-Diagnosis Prompt**
- 向模型展示：(a) 原始題目 (b) 模型自己的錯誤回答與推理過程 (c) 正確答案
- Prompt：「請分析你的回答為何錯誤。你的錯誤屬於以下哪種類型？(1) Knowledge Gap — 缺乏必要知識 (2) Misapplication — 知識正確但應用錯誤 (3) Calculation Error — 計算過程出錯 (4) Distractor Confusion — 被選項誤導。請說明錯誤發生的具體位置。」

**Step 3：Self-Diagnosis Accuracy 評估**
- Ground truth：E1 的人工標註（或 GPT-4o classifier 的分類結果）
- 計算 Self-Diagnosis Accuracy：模型自我診斷的錯誤類型 vs ground truth 的一致率
- 計算 Confusion Matrix：模型最常把哪種錯誤誤判為哪種？

## 實驗設計

**實驗 1：Self-Diagnosis Accuracy 跨模型比較**
- 測試模型：gpt-4o, gpt-4o-mini, qwen3:32b, llama3.1:8b, deepseek-r1:14b
- 每個模型在 CFA-Challenge (90) + CFA-Easy (1,032) 上的錯誤回答
- 核心指標：Self-Diagnosis Accuracy (%), per-Error-Type diagnosis accuracy
- 假說：更大的模型 meta-cognitive 能力更強

**實驗 2：Self-Diagnosis 的 CFA 主題差異**
- 按 CFA 10 大主題分類分析 self-diagnosis accuracy
- 假說：概念性主題（Ethics）的 self-diagnosis 比計算性主題（Derivatives）更容易
- 繪製 CFA Topic x Self-Diagnosis Accuracy heat map

**實驗 3：Cross-Model Diagnosis（模型 A 診斷模型 B 的錯誤）**
- 用 gpt-4o 來診斷 llama3.1:8b 的錯誤，反之亦然
- 比較：Self-Diagnosis vs Cross-Diagnosis 的準確率
- 假說：Cross-Diagnosis（尤其是強模型診斷弱模型）優於 Self-Diagnosis

**實驗 4：Self-Diagnosis 驅動的自動修復選擇**
- 若模型自我診斷為 Knowledge Gap → 自動觸發 RAG
- 若模型自我診斷為 Calculation Error → 自動觸發 Calculator tool
- 評估：基於 self-diagnosis 的自動修復 vs 基於 ground truth 分類的修復 vs 隨機策略選擇
- 核心問題：self-diagnosis 的不完美是否仍然優於無診斷的 blanket approach？

## 需要的積木
- ✅ CFA-Challenge (90) + CFA-Easy (1,032) — 測試題庫已就緒
- ✅ 多模型推論能力 — local Ollama + OpenAI API
- ✅ E1 的錯誤分類結果 — 作為 self-diagnosis 的 ground truth
- ✅ 4 套 RAG 系統 — 實驗 4 的 Knowledge Gap 自動修復
- ❌ Self-Diagnosis Prompt 設計 — 需迭代優化 prompt，約 5-8 小時
- ❌ Financial Calculator tool — 實驗 4 需要（與 E2 共用）

## 預期產出
- 首個關於金融 LLM meta-cognitive capability 的研究
- Self-Diagnosis Accuracy 預期：gpt-4o 約 65-75%，小模型約 45-55%
- 發現模型最常犯的 meta-cognitive 錯誤：預期 Misapplication 最難自我診斷（常誤判為 Knowledge Gap）
- 實證：即使不完美的 self-diagnosis 仍優於 blanket approach（實驗 4）

## 資料需求
- FinEval-CFA-Challenge (90) + FinEval-CFA-Easy (1,032)：已就緒
- E1 的錯誤分類 ground truth：前置依賴
- CFA_Extracted (1,124 含 material)：實驗 4 的 RAG 知識庫

## 模型需求
- 被測模型：gpt-4o, gpt-4o-mini, qwen3:32b, qwen3:4b, llama3.1:8b, deepseek-r1:14b（至少 5 個）
- 不需要 fine-tuning，純 inference。Self-Diagnosis 使用同一模型或不同模型（交叉診斷）

## 狀態
尚未開始。軟性依賴 E1，可先用 GPT-4o 分類結果作為 proxy ground truth 平行推進。

## 可合併的點子
- E1（Error Pattern Atlas）：E1 提供 ground truth，E3 測試 self-diagnosis accuracy
- E2（Targeted Remediation）：E3 的 self-diagnosis 可作為 E2 修復策略的自動選擇機制
- 合併策略：E1 + E3 + E2 →「外部診斷 → 自我診斷 → 自動修復」完整故事
- 獨立策略：E3 單獨聚焦 meta-cognition，投 cognitive science x AI 交叉領域

## 來源筆記
- 新點子，靈感來自 docs/03 方向 4（§4.3 self-correction 實驗）+ 方向 6（§6.2 自動錯誤分類器）
- 與方向 4 的區別：方向 4 涉及 fine-tuning；本研究純 inference，聚焦 meta-cognitive diagnosis
- 學術定位：LLM meta-cognition / introspection，2025-2026 新興方向
