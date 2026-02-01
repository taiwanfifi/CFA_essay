# B3 金融推理自我驗證提示法
# Self-Verification Prompting for Financial Reasoning

## 研究問題

LLM 回答 CFA 題目後，若要求它「回頭檢查自己的答案」，能否發現並修正自身的錯誤？這種純文字層面的 self-verification（不使用任何外部工具）在金融推理中的效果如何？哪些類型的錯誤能被 self-verification 成功捕捉，哪些無法？Self-verification 的成本（額外 token 消耗）與收益（準確率提升）之間的 trade-off 如何？

**關鍵區分**：本研究屬於 LLM-only 的推理增強（inference-time prompting），不涉及 Agent 架構或外部工具調用，與 B2a/B2b/B6 的 Agent+Tool 方法形成清晰的方法論對比。

## 核心方法

設計多種 Self-Verification 策略並嚴格對比：

**Strategy 1: Simple Re-check**
- LLM 先回答，然後被要求「請重新檢查你的答案是否正確」
- 最低成本的 self-verification

**Strategy 2: Structured Critique**
- LLM 回答後，被要求從三個角度自我批判：(a) 使用的概念是否正確？(b) 計算步驟是否有誤？(c) 最終答案是否合理？
- 結構化的 critique prompt

**Strategy 3: Devil's Advocate**
- LLM 回答後，被要求「假設這個答案是錯的，找出可能的錯誤」
- 強制模型尋找反面論證

**Strategy 4: Option-by-Option Verification**
- LLM 回答後，被要求逐一分析每個選項為何正確或錯誤
- 特別適合 MCQ 題型

## 實驗設計

- **Exp 1: 四種 Self-Verification 策略對比** — 在 CFA-Challenge (90) + CFA-Easy (1,032) 上測試。Baseline: Direct answer (no verification)。報告每種策略的準確率提升與額外 token 消耗。
- **Exp 2: Self-Verification 的修正行為分析** — 統計：(a) 原答案正確 → 驗證後仍正確（True Positive Retain）(b) 原答案錯誤 → 驗證後修正（True Correction）(c) 原答案正確 → 驗證後改錯（False Correction，最危險）(d) 原答案錯誤 → 驗證後仍錯（Failed Correction）
- **Exp 3: 模型規模對 Self-Verification 效果的影響** — 比較 phi3.5:3.8b → llama3.1:8b → deepseek-r1:14b → qwen3:32b → gpt-4o。假說：較大模型的 self-verification 效果更好（metacognition 能力更強）。
- **Exp 4: 成本效益分析** — 以 tokens-per-question 為成本指標，繪製 cost vs accuracy 曲線。與 Self-Consistency (k=5) 比較：哪個方法在相同 token 預算下更有效？

## 需要的積木

- ✅ CFA 測試資料集 — FinEval-CFA-Challenge (90), CFA-Easy (1,032)
- ✅ 多規模模型 — phi3.5:3.8b, llama3.1:8b, deepseek-r1:14b, qwen3:32b (Ollama) + gpt-4o (API)
- ✅ Prompt templates — 四種 verification 策略的 prompt 設計
- ❌ 自動化評估 pipeline — 需要解析 LLM 輸出並判斷是否修改了答案
- ❌ Token 計數工具 — 精確計算每種策略的 token 消耗

## 預期產出

- 預期 Structured Critique (Strategy 2) 效果最佳，準確率提升 2-5%
- 預期 False Correction rate 約 5-10%（self-verification 的主要風險）
- 預期大模型 (gpt-4o, qwen3:32b) 的 self-verification 效果顯著優於小模型
- 成本效益分析：self-verification (1 次額外呼叫) vs self-consistency (k=5 次採樣)
- 錯誤類型分析：計算錯誤較難被 self-verification 捕捉（因為 LLM 的計算能力本身有限）

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | 困難題測試 | 已就緒 |
| FinEval-CFA-Easy (1,032) | 主測試集 | 已就緒 |

## 模型需求

- **Local (Ollama)**: phi3.5:3.8b, llama3.1:8b, deepseek-r1:14b, qwen3:32b（規模梯度實驗）
- **API**: gpt-4o, gpt-4o-mini（commercial baseline + 成本對比）

## 狀態

🔲 尚未開始 — 實作門檻最低的研究之一，僅需 prompt engineering + 統計分析

## 可合併的點子

- **B4 (Self-Consistency Voting)** — 可與 self-verification 結合：先投票選出候選答案，再 self-verify
- **B1 (5-Stage Pipeline)** — Self-Verification 可作為 Stage 5 (Reasonableness Verification) 的實現
- **B5 (Dual-Process)** — Self-Verification 可整合進 System 2 的驗證環節

## 來源筆記

- drafts/archive 中 Level 2 討論（LLM-only 推理增強 vs Level 3 Agent+Tool）
- Self-Refine (Madaan et al., 2023) — iterative refinement without external feedback
- LLM self-correction 的限制性研究（Huang et al., 2024）
