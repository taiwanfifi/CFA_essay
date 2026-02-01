# C4 本地端 vs 雲端 RAG：成本-品質權衡分析
# Local vs Cloud RAG: Cost-Quality Tradeoff for Financial QA

## 研究問題

現有 RAG 系統大多依賴商用雲端 API（OpenAI embeddings + GPT-4o-mini generation），但這帶來三個實務問題：(1) API 成本限制大規模實驗的可行性，(2) 資料隱私疑慮（金融資料上傳至第三方），(3) 研究可重現性受限於 API 版本變動。本研究系統性地評估：**以開源本地模型完全替代雲端 API 後，CFA 問答的品質損失有多大？延遲變化如何？成本節省多少？** 這對金融 AI 的 democratization 與 reproducibility 具有重要意義。

## 核心方法

在 C1 確定的最佳 RAG 架構上，系統性替換各組件，測量品質與成本的 Pareto frontier：

**Embedding 替換方案**：
| 方案 | 模型 | 維度 | 部署方式 |
|------|------|------|----------|
| Cloud baseline | text-embedding-3-small | 1536 | OpenAI API |
| Local option A | bge-m3 | 1024 | Ollama |
| Local option B | nomic-embed-text | 768 | Ollama |

**Generation 替換方案**：
| 方案 | 模型 | 參數量 | 部署方式 |
|------|------|--------|----------|
| Cloud baseline | gpt-4o-mini | undisclosed | OpenAI API |
| Local option A | qwen3:32b | 32B | Ollama |
| Local option B | qwen3:30b-a3b | 30B (3B active, MoE) | Ollama |
| Local option C | deepseek-r1:14b | 14B | Ollama |
| Local option D | llama3.1:8b | 8B | Ollama |

全組合測試：3 embeddings × 5 generators = 15 種配置。

## 實驗設計

**實驗 1：Accuracy Comparison**
- 15 種配置在 CFA-Challenge（90 題）與 CFA-Easy（1,032 題）上的準確率
- 統計顯著性檢定（McNemar's test）

**實驗 2：Retrieval Quality**
- 不同 embedding model 的 retrieval precision@k 與 recall@k
- 語義相似度在金融領域的表現差異（domain-specific vs general embeddings）

**實驗 3：Latency Profiling**
- 每題平均延遲，分解為：embedding time + retrieval time + generation time
- 本地模型在 Apple Silicon（M-series）上的實際推理速度

**實驗 4：Cost Analysis**
- OpenAI API 實際花費 vs 本地電力成本估算
- 計算「每正確答案的邊際成本」（cost per correct answer）
- 繪製 accuracy vs cost 的 Pareto frontier

## 需要的積木
- ✅ 最佳 RAG 架構 — 由 C1 確定並復用
- ✅ OpenAI API（gpt-4o-mini, text-embedding-3-small） — 已設定
- ✅ Ollama（llama3.1:8b, qwen3:32b, qwen3:30b-a3b, deepseek-r1:14b） — 本地已安裝
- ❌ bge-m3 / nomic-embed-text embedding via Ollama — 需下載與設定
- ❌ 統一的 benchmark harness — 需建構能切換 embedding + generation 組件的框架
- ✅ CFA_Extracted 資料集 — 已就緒
- ✅ FinEval 測試集 — 已就緒

## 預期產出

- 15 種 embedding × generation 配置的完整 benchmark 矩陣
- Accuracy-Cost Pareto frontier 視覺化圖表
- 金融領域 embedding 品質的 domain-specific 分析
- 本地部署 RAG 的最佳配置建議（在可接受的品質損失下最大化成本節省）

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| CFA_Extracted (1,124) | RAG knowledge base | ✅ 已就緒 |
| FinEval-CFA-Challenge (90) | Hard test set | ✅ 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | ✅ 已就緒 |

## 模型需求

- **Cloud**: gpt-4o-mini, text-embedding-3-small（OpenAI）
- **Local generation**: qwen3:32b, qwen3:30b-a3b, deepseek-r1:14b, llama3.1:8b（Ollama）
- **Local embedding**: bge-m3, nomic-embed-text（Ollama）
- 無需 GPU 訓練，純 inference（Apple Silicon 本地推理）

## 狀態

🟡 **中等難度** — 依賴 C1 先確定最佳架構。15 種配置的全量測試需要大量計算時間（本地推理較慢），預估 3-4 週。

## 可合併的點子

- **C1**：C1 的 cloud baseline 直接成為 C4 的比較基準
- **C3**：可額外分析本地模型 vs 雲端模型的 RAG Lift 差異
- **D1**（Calibration）：本地模型是否比雲端模型更（或更不）well-calibrated？

## 來源筆記

- 新構想，受可重現性與可及性議題啟發
- Ollama 本地部署實務經驗
- Muennighoff et al. (2023) "MTEB: Massive Text Embedding Benchmark" — embedding 評估方法論參考
