# C1 四種 RAG 架構系統性比較：CFA 金融問答場景
# Systematic Comparison of 4 RAG Architectures for CFA Financial QA

## 研究問題

Retrieval-Augmented Generation（RAG）已成為增強 LLM 領域知識的主流方法，但現有文獻缺乏在**同一金融考試資料集、同一生成模型**條件下，對不同 RAG 架構進行公平且全面的比較。本研究利用已實作完成的四套 RAG 系統，在 CFA 考試題目上進行 controlled comparison，回答：不同 retrieval 策略與 orchestration 架構如何影響金融問答的準確率、延遲與成本？

## 核心方法

對四種已建構完成的 RAG 架構進行 head-to-head 比較：

1. **LangGraph Multi-turn Agent**：具 state machine 的多輪對話代理，可動態決定是否需要額外 retrieval
2. **LangChain BM25+Vector Hybrid + Reranking**：結合稀疏檢索（BM25）與稠密檢索（vector），加上 cross-encoder reranking
3. **LlamaIndex Standard**：完整 LlamaIndex pipeline，含 node parsing、indexing、query engine
4. **LlamaIndex Vector-only**：純向量檢索的精簡版本，作為最簡 baseline

關鍵控制變數：所有系統使用相同的 embedding model、相同的 generation model（gpt-4o-mini）、相同的 chunk size 與 overlap 設定。

## 實驗設計

- **資料準備**：改寫 `data_loader.py`，將 thelma2 格式轉換為 CFA 格式，載入 CFA_Extracted（1,124 題含 material/scenario/exhibit）
- **Retrieval 評估**：Precision@k、Recall@k、MRR（Mean Reciprocal Rank），k ∈ {3, 5, 10}
- **End-to-end 評估**：CFA-Challenge（90 題）、CFA-Easy（1,032 題）上的最終答題準確率
- **效率評估**：平均每題延遲（seconds）、平均每題 token 消耗量、估算 API 成本
- **Ablation**：關閉 reranking、關閉 BM25、調整 top-k，觀察各組件的邊際貢獻

## 需要的積木
- ✅ LangGraph multi-turn agent RAG — 已實作完成
- ✅ LangChain BM25+Vector hybrid RAG — 已實作完成
- ✅ LlamaIndex standard RAG — 已實作完成
- ✅ LlamaIndex vector-only RAG — 已實作完成
- ❌ CFA 格式 data_loader.py — 需從 thelma2 格式改寫，預計 1-2 天
- ✅ CFA_Extracted 資料集（1,124 題） — 已就緒
- ✅ FinEval-CFA-Challenge / CFA-Easy — 已就緒
- ✅ OpenAI API（gpt-4o-mini, text-embedding-3-small） — 已設定

## 預期產出

- 四種 RAG 架構在 CFA 上的完整 benchmark 表格（accuracy、retrieval metrics、latency、cost）
- 各架構在不同 CFA 主題上的細粒度表現差異分析
- Retrieval 品質與最終準確率之間的相關性分析
- RAG 架構選擇建議指南（針對金融 QA 場景）

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| CFA_Extracted (1,124) | RAG knowledge base + 測試題 | ✅ 已就緒 |
| FinEval-CFA-Challenge (90) | Hard test set | ✅ 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | ✅ 已就緒 |

## 模型需求

- **Embedding**: text-embedding-3-small（OpenAI）
- **Generation**: gpt-4o-mini（統一使用，控制變數）
- **Reranking**: cross-encoder（LangChain pipeline 專用）
- 無需 GPU 訓練，純 inference + API 呼叫

## 狀態

🟢 **最容易啟動的論文** — 四套系統已全部實作完成，僅需統一資料格式與設計評估流程。預估 2-3 週可完成實驗與初稿。

## 可合併的點子

- **C4**（Local vs Cloud RAG）：本研究確立 cloud baseline 後，C4 直接替換為 local model 進行對比
- **C3**（Parametric vs Retrieved）：本研究的 RAG 準確率可作為 C3 的 "with RAG" 條件
- **D1**（Calibration）：可在四種 RAG 上分別測量 calibration，觀察 retrieval 是否改善信心校準

## 來源筆記

- 四套 RAG 系統實作經驗（thelma2 專案）
- Lewis et al. (2020) "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- 本倉庫 `docs/03` 方向 3（RAG for Financial QA）
