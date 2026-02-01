# C2 CFA 知識圖譜增強式 RAG
# CFA Knowledge Graph Augmented RAG

## 研究問題

傳統 chunk-based RAG 將文本切成固定長度片段，忽略了金融知識之間的結構化關係。例如，理解 "Immunization" 需要同時掌握 Duration、Convexity、Liability Matching 等前置概念及其相互依賴。本研究探問：**以 Knowledge Graph 為骨架的 RAG 是否能比純 chunk-based RAG 更有效地回答需要跨概念推理的 CFA 題目？** 特別針對那些需要整合多個知識節點的複雜題型。

## 核心方法

從 CFA_Extracted 的 material 欄位（1,124 份文件）中抽取結構化知識，建構 CFA Knowledge Graph，並設計三種 retrieval 策略的比較框架：

**節點類型（Node Types）**：
- `Concept`：金融概念（如 Duration, WACC, Black-Scholes）
- `Formula`：量化公式（如 Macaulay Duration 公式）
- `Principle`：定性原則（如 No-Arbitrage Principle）
- `Regulation`：監管規範（如 GIPS Standards, Basel III）

**邊類型（Edge Types）**：
- `prerequisite`：A 是理解 B 的前提
- `applied_in`：概念 A 被應用於場景 B
- `conflicts_with`：原則 A 與原則 B 存在衝突
- `refines`：概念 B 是概念 A 的精細化版本
- `regulated_by`：活動 A 受規範 B 約束
- `quantified_by`：概念 A 由公式 B 量化

## 實驗設計

**Phase 1：Knowledge Graph Construction**
- 使用 GPT-4o 對 1,124 份 material 進行 relation extraction（few-shot prompting）
- 輸出格式：`(head_entity, relation_type, tail_entity, source_doc_id)`
- 人工驗證 200 條 triples 的品質，計算 extraction precision
- 使用 NetworkX 儲存與查詢圖結構

**Phase 2：三種 Retrieval 策略比較**
1. **Chunk-based RAG**（baseline）：現有 C1 中表現最佳的 RAG 架構
2. **Graph-based Retrieval**：根據題目辨識的概念，在 KG 上做 k-hop 子圖擷取，將相關節點與邊轉為 context
3. **Hybrid**：先 graph retrieval 取得結構化 context，再用 chunk retrieval 補充細節文本

**Phase 3：評估**
- 在 CFA-Challenge（90 題）和 CFA-Easy（1,032 題）上比較三種策略
- 按題目複雜度分層分析：單概念題 vs 多概念跨領域題

## 需要的積木
- ✅ CFA_Extracted 資料集（1,124 題含 material） — 已就緒
- ✅ OpenAI API（GPT-4o for extraction, gpt-4o-mini for generation） — 已設定
- ❌ Relation extraction pipeline — 需設計 prompt template + few-shot examples
- ❌ Knowledge Graph 建構與儲存 — NetworkX 實作，預計 1 週
- ❌ Graph-based retrieval 模組 — 需實作 subgraph extraction + context serialization
- ✅ Chunk-based RAG baseline — 由 C1 提供
- ✅ FinEval 測試集 — 已就緒

## 預期產出

- CFA 領域 Knowledge Graph（預估 5,000-10,000 triples）
- 三種 retrieval 策略的準確率比較表
- 分析：哪些 CFA 主題從 KG 結構化檢索中獲益最大
- Graph-based retrieval 的 failure case 分析（何時結構化反而有害）

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| CFA_Extracted (1,124) | KG construction source + test | ✅ 已就緒 |
| FinEval-CFA-Challenge (90) | Hard test set | ✅ 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | ✅ 已就緒 |

## 模型需求

- **Relation Extraction**: GPT-4o（高品質 triple 抽取）
- **Generation**: gpt-4o-mini（統一使用）
- **Graph Storage**: NetworkX（Python library，無需額外基礎設施）
- 無需 GPU 訓練

## 狀態

🟡 **中等難度** — KG 建構需要 prompt engineering 與人工驗證，預估 4-6 週完成實驗。建議在 C1 完成後啟動，以復用其 chunk-based RAG baseline。

## 可合併的點子

- **C1**：直接復用 C1 的最佳 chunk-based RAG 作為 baseline
- **C3**：KG-RAG 提供的結構化知識可能特別有助於模型的 declarative knowledge gaps
- **D1**：觀察 KG-RAG 是否改善模型的 calibration（結構化知識是否讓模型更「知道自己知道什麼」）

## 來源筆記

- 本倉庫 `docs/03` 方向 3（RAG for Financial QA）
- Pan et al. (2024) "Unifying Large Language Models and Knowledge Graphs: A Roadmap"
- CFA_Extracted 資料集 material 欄位的初步分析
