# D3 AI 何時該說「我不知道」？金融問答的棄權機制
# When Should AI Say "I Don't Know"? Abstention Mechanism for Financial QA

## 研究問題

在金融顧問場景中，一個錯誤但自信的回答可能比承認不確定更加危險。現有 LLM 系統傾向於「永遠給出答案」，缺乏拒絕回答的能力。本研究設計並評估一套 **abstention mechanism**（棄權機制），使金融 AI 在信心不足時主動拒絕作答，並系統性地分析：**什麼樣的信心閾值能在回答覆蓋率與準確率之間取得最佳平衡？不同 CFA 主題是否需要不同的棄權閾值？**

## 核心方法

基於 D1 建立的 confidence estimation 基礎，設計一套可調節的 abstention framework：

**核心公式**：
- 給定 confidence score c(q) 與閾值 θ
- 若 c(q) ≥ θ → 回答
- 若 c(q) < θ → 棄權（"I'm not confident enough to answer this question"）

**進階設計**：
1. **Global Threshold**：所有題目使用同一 θ
2. **Topic-adaptive Threshold**：每個 CFA 主題有獨立的 θ_topic（某些主題需要更高信心才回答）
3. **Cascaded Abstention**：先用小模型嘗試，不確定時升級至大模型，仍不確定則棄權
4. **Consensus-based Abstention**：結合 D2 的跨模型共識，低共識則棄權

## 實驗設計

**實驗 1：Coverage-Accuracy Pareto Frontier**
- 對每種 confidence method（D1 的四種），掃描 θ ∈ [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
- 繪製 coverage（回答比例）vs accuracy（所回答題目的準確率）曲線
- 計算 AUC（Area Under Coverage-Accuracy Curve）作為單一指標

**實驗 2：Topic-adaptive Threshold Optimization**
- 對每個 CFA 主題獨立優化 θ_topic
- 目標函數：在 accuracy ≥ 85% 的約束下最大化 coverage
- 比較：topic-adaptive θ vs global θ 的整體表現差異

**實驗 3：Cascaded Abstention Pipeline**
- 階段 1：qwen3:4b（最快）→ 高信心則回答
- 階段 2：qwen3:32b（較強）→ 高信心則回答
- 階段 3：gpt-4o-mini（最強）→ 高信心則回答
- 階段 4：棄權
- 評估：此 cascade 是否在維持高準確率的同時降低平均成本與延遲？

**實驗 4：Human-in-the-Loop Simulation**
- 模擬場景：AI 回答有信心的題目，棄權的題目交由「人類專家」
- 假設人類準確率 = 70%（CFA 考試的及格率附近）
- 計算 AI + Human 混合系統的總體準確率
- 分析：在什麼 θ 設定下，混合系統表現最佳？

## 需要的積木
- ✅ D1 的 confidence estimation pipeline — 需先完成 D1
- ✅ Ollama models（多種尺寸供 cascade 使用） — 本地已安裝
- ✅ OpenAI API（gpt-4o-mini） — 已設定
- ✅ FinEval 測試集 — 已就緒
- ❌ Abstention framework — 需實作 threshold-based 決策模組
- ❌ Topic-adaptive optimization — 需實作 per-topic threshold 搜尋
- ❌ Cascade pipeline — 需實作多模型逐級升級邏輯

## 預期產出

- Coverage-Accuracy Pareto frontier 圖表（跨模型、跨 confidence method）
- Topic-adaptive threshold map（各 CFA 主題的最佳 θ）
- Cascaded abstention 的成本-品質分析
- Human-AI 混合系統的模擬分析
- 金融 AI abstention 機制的設計指南

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | Hard test set | ✅ 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | ✅ 已就緒 |
| CRA-Bigdata (1,472) | Large-scale test set | ✅ 已就緒 |

## 模型需求

- **Cloud**: gpt-4o-mini（OpenAI）
- **Local**: qwen3:4b, qwen3:30b-a3b, qwen3:32b, llama3.1:8b, deepseek-r1:14b（Ollama）
- 無需 GPU 訓練

## 狀態

🟡 **依賴 D1** — 本研究的核心建立在 D1 的 confidence scores 之上。D1 完成後，D3 的增量工作量約 2 週。可視為 D1 的自然延伸。

## 可合併的點子

- **D1**（Calibration）：D3 完全依賴 D1 的 confidence estimation 結果
- **D2**（Cross-Model Consensus）：consensus-based abstention 是 D3 的進階版本
- **D4**（Overconfident AI）：D3 的 abstention 機制正是解決 D4 所揭示的 overconfidence 風險的方案
- **C4**（Local vs Cloud）：cascaded abstention 與 local-to-cloud escalation 的概念相互呼應

## 來源筆記

- 新構想，為 D1 的自然衍生
- Geifman & El-Yaniv (2017) "Selective Classification for Deep Neural Networks"
- Kamath et al. (2020) "Selective Question Answering under Domain Shift"
- 金融監管中「適合度義務」(Suitability Obligation) 的啟發：不確定時不應給出建議
