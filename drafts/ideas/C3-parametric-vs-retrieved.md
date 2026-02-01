# C3 參數化知識 vs 檢索知識：CFA 領域的知識來源分析
# Parametric Knowledge vs Retrieved Knowledge for CFA Financial QA

## 研究問題

LLM 在預訓練過程中吸收了大量金融知識（parametric knowledge），而 RAG 則在 inference 時注入外部知識（retrieved knowledge）。一個關鍵但尚未被系統研究的問題是：**對於 CFA 考試的各個主題，LLM 的參數化知識是否已經足夠？哪些主題真正需要外部檢索？** 本研究透過同一模型在 with-RAG 與 without-RAG 條件下的表現差異，繪製出 CFA 各主題的「知識來源地圖」。

## 核心方法

對每道 CFA 題目，使用同一 LLM 分別在兩個條件下作答：

1. **Closed-book**（無 RAG）：模型僅依賴自身 parametric knowledge
2. **Open-book**（有 RAG）：模型獲得 CFA_Extracted material 作為 context

計算每個 CFA 主題的 **RAG Lift**（= Open-book accuracy - Closed-book accuracy）：
- RAG Lift 高 → 該主題的知識尚未充分參數化，外部檢索至關重要
- RAG Lift 低或負 → 模型已內化該主題知識，RAG 可能引入噪音反而有害
- RAG Lift 為負 → 檢索到的 context 可能 misleading，值得深入分析

此分析結果可直接對應「CFA Ability Matrix」概念：辨識模型在 CFA 各主題上的 Declarative Knowledge 缺口。

## 實驗設計

**實驗 1：RAG Lift by CFA Topic**
- 測試集：CFA-Challenge（90 題）+ CFA-Easy（1,032 題）
- 模型：gpt-4o-mini, qwen3:32b, llama3.1:8b, deepseek-r1:14b
- 每道題目收集 closed-book 與 open-book 答案
- 按 CFA 主題（Ethics, Quant, Economics, FRA, Corporate Finance, Equity, Fixed Income, Derivatives, Alternative, Portfolio Management）分組統計

**實驗 2：Per-Question Concordance Analysis**
- 四種組合：(closed-book correct, open-book correct), (closed-book wrong, open-book correct), (closed-book correct, open-book wrong), (both wrong)
- 重點分析「closed-book correct, open-book wrong」的 cases — 這代表 RAG 引入了有害噪音

**實驗 3：Cross-Model Consistency**
- 同一題目在不同模型上的 RAG Lift 是否一致？
- 如果不同模型在相同主題上都顯示高 RAG Lift → 該主題本質上需要外部知識
- 如果 RAG Lift 因模型而異 → 差異來自模型的 pretraining data composition

## 需要的積木
- ✅ CFA_Extracted 資料集（1,124 題含 context） — 已就緒，作為 RAG knowledge base
- ✅ RAG pipeline — 由 C1 確定最佳架構後直接復用
- ✅ Ollama models（llama3.1:8b, qwen3:32b, deepseek-r1:14b） — 本地已安裝
- ✅ OpenAI API（gpt-4o-mini） — 已設定
- ❌ Closed-book evaluation harness — 需建構標準化的無 RAG 評估流程
- ❌ Topic classifier — 需為每道題目標註 CFA 主題類別

## 預期產出

- CFA 各主題的 RAG Lift 熱力圖（跨模型 × 跨主題）
- 「知識來源地圖」：哪些主題需要 RAG、哪些不需要
- RAG 有害案例的定性分析（open-book 反而錯誤）
- 對 RAG 系統設計的建議：根據題目主題動態決定是否啟用 retrieval

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| CFA_Extracted (1,124) | RAG knowledge base | ✅ 已就緒 |
| FinEval-CFA-Challenge (90) | Hard test set | ✅ 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | ✅ 已就緒 |

## 模型需求

- **Cloud**: gpt-4o-mini（OpenAI）
- **Local**: qwen3:32b, llama3.1:8b, deepseek-r1:14b（Ollama）
- 無需 GPU 訓練，純 inference

## 狀態

🟡 **中等難度** — 實驗邏輯簡單但需要大量 inference runs（4 模型 × 2 條件 × 1,122 題 = ~8,976 runs）。建議在 C1 完成後啟動。預估 3-4 週。

## 可合併的點子

- **C1**：復用 C1 確定的最佳 RAG 架構作為 open-book 條件
- **D1**（Calibration）：比較 closed-book 與 open-book 條件下的 calibration 差異
- **C2**（KG-RAG）：可增加第三條件 — KG-augmented RAG，觀察結構化知識的額外 lift

## 來源筆記

- 新構想，受 CFA Ability Matrix 概念啟發
- Mallen et al. (2023) "When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories"
- 本倉庫 `docs/03` 方向 3 與方向 7 的交叉點
