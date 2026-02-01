# E4 為什麼 Level 3 對 AI 更難？
# CFA Level Difficulty Progression: A Cognitive Complexity Analysis

## 研究問題

o4-mini 在 CFA Level III 達到 79.1% 正確率，GPT-4o 在 FinanceMath 僅達 60.9%（人類 92%）。但我們缺乏對「到底是什麼讓 CFA 題目對 AI 更難」的系統性量化。Level I 側重知識記憶，Level II 強調分析應用，Level III 要求綜合判斷與情境推理——這些直覺觀察能否被精確量化為一個 Cognitive Complexity Index (CCI)？CCI 能否解釋並預測 LLM 在不同題目上的表現？

## 核心方法

設計 Cognitive Complexity Index (CCI)，由五個子維度組成：

**CCI 子維度定義**

| 子維度 | 定義 | 評分方式 |
|--------|------|----------|
| Knowledge Breadth | 題目涉及的獨立知識點數量 | 1-5 個知識點，對應 1-5 分 |
| Reasoning Depth | 從題目到答案所需的推理步驟數 | 1-5 步，對應 1-5 分 |
| Numerical Precision | 數值計算的精確度要求 | 0（無計算）/ 1（簡單）/ 3（中等）/ 5（高精度多步計算） |
| Ambiguity Degree | 題目的模糊程度（是否有多個似乎合理的答案） | 1（明確）到 5（高度模糊） |
| Cross-Topic Integration | 是否需要整合多個 CFA 主題的知識 | 0（單主題）/ 2（雙主題）/ 4（三主題以上） |

**CCI 計算**：CCI = weighted sum of five dimensions（權重由回歸分析 fit 到模型 error rate）

**CCI 標註方式**：使用 GPT-4o 作為 automatic annotator，對每道題目標註五個子維度。在 150 題人工標註樣本上計算 inter-rater reliability。

## 實驗設計

**實驗 1：CCI 分布的跨 Level 比較**
- Dataset mapping：CFA-Easy (1,032 題，混合 L1/L2 難度) / CFA-Challenge (90 題，harder) / CFA_Extracted (1,124 題含 material)
- 對所有題目計算 CCI 及五個子維度
- 繪製：CCI 分布直方圖 by dataset，五個子維度的 box plot by dataset
- 核心假說：CFA-Challenge 的 CCI 顯著高於 CFA-Easy

**實驗 2：CCI 與 LLM Error Rate 的相關性**
- 對每道題收集多模型的 pass/fail 結果
- 計算 Item Difficulty（所有模型中的答錯率）
- 分析 CCI vs Item Difficulty 的相關係數（Pearson r, Spearman rho）
- 回歸分析：哪些 CCI 子維度對 LLM error rate 的預測力最強？
- 假說：Numerical Precision 和 Reasoning Depth 是 LLM 困難度的最強預測因子

**實驗 3：不同模型的 CCI 敏感度曲線**
- 對每個模型繪製 accuracy vs CCI 的 sigmoid 衰減曲線
- 比較：gpt-4o 的衰減起點是否比 llama3.1:8b 更晚？不同模型對哪個子維度最敏感？
- 預期：小模型對 Knowledge Breadth 最敏感，所有模型對 Numerical Precision 都敏感

**實驗 4：CCI 驅動的 adaptive difficulty routing**
- 根據 CCI 預估，低 CCI 題目分配給小模型（qwen3:4b），高 CCI 分配給大模型（gpt-4o）
- 評估：固定 API 成本下，adaptive routing vs 統一使用單一模型的 accuracy

## 需要的積木
- ✅ CFA-Easy (1,032) + CFA-Challenge (90) + CFA_Extracted (1,124) — 已就緒
- ✅ CRA-Bigdata (1,472) — 可選擴充
- ✅ 多模型推論能力 — local Ollama (8 models) + OpenAI API
- ✅ GPT-4o API — 作為 CCI automatic annotator
- ❌ 150 題人工 CCI 標註 — 需 CFA 背景，預計 25-35 小時
- ❌ 統計分析管道 — regression, correlation, visualization（約 10-15 小時）

## 預期產出
- Cognitive Complexity Index (CCI)：首個量化 CFA 題目認知複雜度的指標
- CCI 與 LLM error rate 強相關（預期 Spearman rho > 0.6）
- Numerical Precision 為最強預測因子（呼應 FinanceMath 基準發現）
- 模型間 CCI 敏感度曲線差異分析 + Adaptive routing 等成本下提升 accuracy 5-10%

## 資料需求
- FinEval-CFA-Easy (1,032) + CFA-Challenge (90) + CFA_Extracted (1,124 含 material)：已就緒
- CRA-Bigdata (1,472)：可選擴充

## 模型需求
- 被測模型：gpt-4o, gpt-4o-mini, qwen3:32b, qwen3:4b, llama3.1:8b, deepseek-r1:14b, gemma3, phi3.5:3.8b
- CCI annotator：gpt-4o（API）。不需要 fine-tuning，純 inference + statistical analysis

## 狀態
尚未開始。無硬性依賴，可獨立啟動。建議與 E1 的多模型推論同步進行（共用推論結果）。

## 可合併的點子
- E1（Error Pattern Atlas）：E1 Error Type + E4 CCI → 三維分析（Error Type x CFA Topic x CCI Level）
- E3（Self-Correction）：CCI 高的題目是否更難自我診斷？
- Adaptive routing（實驗 4）可延伸為獨立 multi-agent system 研究
- 論文策略：E4 適合獨立 short paper 或 Findings paper

## 來源筆記
- 新點子，靈感：o4-mini CFA L3 79.1%（arXiv 2507.02954）、FinanceMath GPT-4o 60.9% vs 人類 92%（arXiv 2509.04468）
- 與現有工作差異：現有研究僅報告 per-level accuracy，未量化「是什麼讓題目更難」
- 學術定位：Item Response Theory (IRT) x LLM evaluation 交叉，2025-2026 新興方向
