# E2 對症下藥的 AI 修復策略
# Targeted Error Remediation for Financial LLMs

## 研究問題

LLM 在 CFA 題目上犯的錯誤各有不同成因，但現有改進方法多為「一體適用」：無差別地套用 Chain-of-Thought 或 RAG，不分青紅皂白。這等於用同一種藥治所有病。本研究的核心問題是：若已知錯誤類型（來自 E1 的分類），針對每種錯誤類型設計專屬修復策略，是否能顯著超越通用修復方法？以及，哪種錯誤類型最容易被修復、哪種最頑固？

## 核心方法

基於 E1 的四大錯誤類型，設計四種對應的 targeted remediation strategy：

| 錯誤類型 | 修復策略 | 機制 |
|---------|---------|------|
| Knowledge Gap | RAG retrieval | 從 CFA_Extracted 的 material 欄位檢索缺失知識，注入 context 後重新回答 |
| Calculation Error | Financial Calculator tool | 使用 Python 實現的金融計算器（TVM, Bond pricing 等），以 ReAct 框架調用 |
| Misapplication | Few-shot demonstration | 提供 3 個同主題、同公式的正確應用範例，引導模型修正概念適用 |
| Distractor Confusion | Option-by-option analysis | 強制模型逐一分析每個選項的正確性與錯誤原因，消除 distractor 干擾 |

關鍵對比：Targeted Remediation（對症下藥）vs Blanket CoT（通用 Chain-of-Thought）vs Blanket RAG（通用知識檢索）。

## 實驗設計

**實驗 1：單策略修復效果（Ablation Study）**
- 對 E1 分類出的每種錯誤類型，分別施加四種修復策略
- 計算 Fix Rate（修復成功率）：修復後答對 / 原始答錯的題數
- 核心假說：matched strategy（對應策略）的 Fix Rate > mismatched strategy

**實驗 2：Targeted vs Blanket 比較**
- Blanket CoT baseline：所有錯誤題目統一套用 CoT 重新回答
- Blanket RAG baseline：所有錯誤題目統一套用 RAG 重新回答
- Targeted：根據 E1 分類結果，每道題使用對應策略
- 評估指標：Overall Fix Rate, Fix Rate per Error Type, 修復後的 accuracy

**實驗 3：Cascaded Remediation Pipeline**
- 設計串聯修復：先嘗試低成本策略（Option Analysis），失敗則升級（Few-shot），再失敗則（RAG + Calculator）
- 在固定 API 預算下，比較 Cascaded Pipeline vs Single Best Strategy 的總修復率

**實驗 4：修復策略的跨模型通用性**
- 在 gpt-4o 上有效的修復策略，在 llama3.1:8b 或 qwen3:32b 上是否同樣有效？
- 分析：不同能力層級的模型，各策略的 Fix Rate 差異

## 需要的積木
- ✅ E1 的錯誤分類結果 — E1 完成後直接獲得（本研究的前置依賴）
- ✅ 4 套 RAG 系統 — Knowledge Gap 修復策略的基礎
- ✅ CFA_Extracted (1,124 題含 material) — RAG 的知識來源
- ✅ GPT-4o / gpt-4o-mini API — 修復推論
- ✅ Local Ollama 模型 — 跨模型通用性實驗
- ❌ Financial Calculator tool — 需開發 Python 金融計算器（TVM, Bond, Statistics），約 30-40 小時
- ❌ Few-shot example bank — 需為每個 CFA 主題建構 3-5 個 demonstration examples，約 15-20 小時

## 預期產出
- Targeted Remediation 的 Fix Rate 顯著高於 Blanket 方法（預期 60-70% vs 30-40%）
- Knowledge Gap 的修復最容易（RAG 直接補充缺失知識，預期 Fix Rate 70-80%）
- Distractor Confusion 最頑固（即使逐項分析，模型仍可能被誤導，預期 Fix Rate 40-50%）
- 可視化：Error Type x Remediation Strategy 的 Fix Rate matrix

## 資料需求
- E1 的完整錯誤分類輸出（前置依賴）
- FinEval-CFA-Challenge (90) + FinEval-CFA-Easy (1,032)：已就緒
- CFA_Extracted (1,124 含 material context)：RAG 知識庫
- Few-shot examples：需從 FinTrain-cfa_exercise (2,946) 中挑選示範案例

## 模型需求
- 被修復模型：至少 4 個（gpt-4o, gpt-4o-mini, llama3.1:8b, qwen3:32b）
- RAG embedding model：現有 RAG 系統已配備
- 不需要 fine-tuning，純 inference + tool use

## 狀態
尚未開始。硬性依賴 E1 的完成（需要錯誤分類結果作為輸入）。

## 可合併的點子
- E1（Error Pattern Atlas）：E1 提供分類，E2 提供修復，兩者構成完整的「診斷—治療」閉環
- E3（Agent Self-Correction）：E3 的 self-diagnosis 可作為 E2 的自動化前端——若模型能自我診斷，就能自動選擇修復策略
- B6（Calculator Tool）：E2 中 Calculation Error 的修復策略直接使用 B6 的金融計算器
- 論文策略：E1 + E2 可合併為一篇完整論文（診斷 + 修復），對標 docs/03 方向 6 的完整設計

## 來源筆記
- docs/03-研究方向深度設計.md — 方向 6（Error Pattern Mining and Targeted Remediation）§6.2-6.5
- 本點子聚焦方向 6 的後半部：修復策略設計與 ablation study
- 核心學術貢獻：「Targeted > Blanket」的實證，以及修復難度的 Error Type 排序
