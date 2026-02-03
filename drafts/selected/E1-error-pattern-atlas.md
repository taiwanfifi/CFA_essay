# E1 金融 AI 錯誤圖譜
# CFA Error Pattern Atlas

## 研究問題

當 LLM 在 CFA 題目上犯錯時，錯誤並非同質的——Knowledge Gap、公式誤用、計算失誤、被 distractor 迷惑，各自需要截然不同的修復手段。然而現有研究只報告整體 accuracy，從未系統性地分類與量化這些錯誤。本研究的目標是：建構一個多維度的 CFA Error Pattern Atlas，讓每一種失敗模式都被精確定位、計數、視覺化。這本身就是一個 data/resource contribution——圖譜即論文的核心貢獻。

## 核心方法

設計三維度錯誤分類體系（Error Taxonomy），對 LLM 所有錯誤回答進行自動分類：

**Dimension 1 — Error Type（錯誤類型，4 大類 12 子類）**
- Knowledge Gap：Concept Unknown / Concept Incomplete / Regulation Outdated
- Misapplication：Wrong Formula / Wrong Condition / Concept Confusion
- Calculation Error：Arithmetic Error / Unit Error / Precision Error
- Distractor Confusion：Partial Truth / Common Misconception / Similar Value

**Dimension 2 — CFA Topic（CFA 學科領域，10 類）**
- Ethics, Quantitative Methods, Economics, Financial Reporting, Corporate Finance,
  Equity, Fixed Income, Derivatives, Alternative Investments, Portfolio Management

**Dimension 3 — Cognitive Stage（認知階段，對應 B1 的 5-stage pipeline）**
- Concept Identification / Formula Recall / Data Extraction / Calculation / Verification

使用 GPT-4o 作為 automatic error classifier：輸入題目 + 模型錯誤回答（含 reasoning trace）+ 正確答案，輸出三個維度的分類標籤。在 200 題人工標註樣本上計算 Cohen's Kappa 以驗證分類器可靠性。

## 實驗設計

**實驗 1：大規模錯誤收集**
- 對 8+ 模型（local Ollama: llama3.1:8b, qwen3:32b, deepseek-r1:14b 等 + API: gpt-4o, gpt-4o-mini）在 CFA-Challenge (90) + CFA-Easy (1032) 上收集所有錯誤回答及完整 reasoning trace

**實驗 2：自動分類 + 人工校驗**
- GPT-4o 對所有錯誤進行三維分類
- 隨機抽取 200 題進行人工標註，計算 inter-annotator agreement 與 Cohen's Kappa

**實驗 3：Error Atlas 視覺化**
- 繪製 CFA Topic x Error Type 二維 heat map（核心圖表）
- 繪製 Error Type x Cognitive Stage 交叉分析
- 跨模型比較：不同模型的錯誤分布是否相似？

**實驗 4：跨模型錯誤遷移分析**
- 計算模型 A 與模型 B 的錯誤模式相似度（Cosine Similarity on error distribution vectors）
- 測試假說：小模型的錯誤是否為大模型錯誤的超集？

## 需要的積木
- ✅ CFA-Challenge (90) + CFA-Easy (1032) — 測試題庫已就緒
- ✅ 多模型推論能力 — local Ollama (8 models) + OpenAI API
- ✅ GPT-4o API — 作為 automatic error classifier
- ✅ 4 套 RAG 系統 — 部分實驗可觀察 RAG 是否改變錯誤分布
- ❌ 200 題人工標註 — 需 CFA 知識背景的標註者，預計 30-40 小時
- ❌ Heat map 視覺化管道 — 需開發（matplotlib/seaborn，約 8-10 小時）

## 預期產出
- CFA Error Pattern Atlas：首個金融 LLM 系統性錯誤圖譜（可公開釋出的 resource）
- 揭示關鍵模式，例如：Derivatives 以 Calculation Error 為主、Ethics 以 Distractor Confusion 為主
- 跨模型錯誤相似度分析，預期 Cohen's Kappa 0.4-0.6（中度相似）
- GPT-4o 自動分類器的驗證結果，為後續研究提供可復用的工具

## 資料需求
- FinEval-CFA-Challenge (90 題) + FinEval-CFA-Easy (1,032 題)：已就緒
- CFA_Extracted (1,124 題含 material context)：用於輔助判斷 Knowledge Gap
- CRA-Bigdata (1,472 題)：可選，用於擴大分析範圍

## 模型需求
- 被測模型：llama3.1:8b, qwen3:32b, qwen3:4b, deepseek-r1:14b, gpt-4o, gpt-4o-mini（至少 6 個）
- 分類器模型：gpt-4o（API）
- 不需要 fine-tuning，純 inference

## 狀態
尚未開始。前置步驟：先完成多模型大規模推論，收集所有錯誤回答。

## 可合併的點子
- E2（Targeted Remediation）：E1 的錯誤分類直接作為 E2 的輸入
- E3（Agent Self-Correction）：E1 的人工分類可作為 E3 self-diagnosis accuracy 的 ground truth
- B1（Structured Reasoning Pipeline）：Dimension 3 直接使用 B1 的 5-stage framework

## 來源筆記
- docs/03-研究方向深度設計.md — 方向 6（Error Pattern Mining and Targeted Remediation）§6.1-6.3
- 本點子聚焦於方向 6 的前半部：錯誤分類與圖譜建構，不含修復策略（修復策略歸 E2）
- 設計為 data/resource contribution paper，圖譜本身即為核心學術貢獻
