# B1 結構化五階段金融推理管道
# Structured 5-Stage Financial Reasoning Pipeline

## 研究問題

LLM 回答 CFA 題目時，失敗究竟發生在認知過程的哪個環節？現有研究（FinDAP、CFA Level III 大規模評估）僅報告最終正確率，無法定位失敗的精確階段。本研究將解題過程拆解為五個獨立可評估的認知階段，建構首個 CFA 領域的 Stage-wise Error Profile。

## 核心方法

設計五階段認知管道（Cognitive Pipeline），模擬 CFA 考生的解題流程：

1. **Concept Identification** — 辨識題目涉及的金融概念（如 Duration, Convexity, Immunization），評估 precision/recall
2. **Formula / Principle Recall** — 根據辨識出的概念回想應適用的公式或原則，評估精確匹配 + 語義等價
3. **Numerical / Condition Extraction** — 從題幹（含 exhibit/scenario）提取結構化數值與條件（JSON 格式），與人工標註比對
4. **Calculation Execution** — 將公式 + 數值代入計算，與正確答案進行數值比較（容許合理精度誤差）
5. **Reasonableness Verification** — 判斷計算結果是否在合理範圍內，評估能否偵測自身計算錯誤

每個 Stage 獨立評估準確率，並計算各 Stage 對最終錯誤的貢獻比例。

## 實驗設計

- **Exp 1: Stage-wise Accuracy Profiling** — 在 FinEval-CFA-Challenge (90) + CFA-Easy (1,032) 上，對每道題目在五個 Stage 分別中斷並評估。測試 GPT-4o、gpt-4o-mini、qwen3:32b、llama3.1:8b 等。
- **Exp 2: Error Attribution Matrix** — 對所有最終答錯的題目，回溯標記首個出錯的 Stage。建立 CFA 主題 x Stage 的 Error Attribution 二維熱力圖。
- **Exp 3: 與現有推理策略嚴格對比** — Baselines: Zero-shot, Few-shot (3/5-shot), Vanilla Chain-of-Thought, Self-Consistency (k=5,10)。Proposed: 5-Stage Pipeline。
- **Exp 4: 教育診斷應用** — 基於 Error Attribution Matrix 為每個 CFA 主題產生學習建議報告。

## 需要的積木

- ✅ CFA 測試資料集 — FinEval-CFA-Challenge (90), CFA-Easy (1,032), CFA_Extracted (1,124)
- ✅ LLM 推論環境 — Ollama local models + OpenAI API
- ✅ Prompt engineering 框架 — 每個 Stage 需要專用 prompt template
- ❌ Stage ground truth annotations — 需要約 200 題 x 5 個 Stage 的人工標註（估計 ~50 小時）
- ❌ Stage pipeline 程式碼 — 五階段管道的 orchestration code（含中斷評估邏輯）
- ❌ 自動化評估腳本 — 各 Stage 輸出的自動比對與計分

## 預期產出

- 首個 CFA 領域的 Stage-wise Error Profile，揭示 LLM 在金融推理中的瓶頸環節
- 預期 Stage 3（數值提取）與 Stage 4（計算執行）為主要失敗點
- 預期 Structured Pipeline 相較於 Vanilla CoT 在準確率上提升 3-8%
- Error Attribution Matrix 熱力圖：哪些 CFA 主題在哪個 Stage 最容易出錯

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | 主測試集（困難題） | 已就緒 |
| FinEval-CFA-Easy (1,032) | 主測試集（一般題） | 已就緒 |
| CFA_Extracted (1,124) | 輔助 ground truth 建構 | 已就緒 |

## 模型需求

- **Local (Ollama)**: llama3.1:8b, qwen3:32b, deepseek-r1:14b（不同規模的對比）
- **API**: gpt-4o, gpt-4o-mini（commercial baseline）

## 狀態

🔲 尚未開始 — 需先完成 Stage ground truth 標註（最大瓶頸）

## 可合併的點子

- **B6 (ReAct Financial Calculator)** — Financial Calculator 可直接插入 Stage 4，取代 LLM 自行計算
- **B3 (Self-Verification)** — Self-Verification 可整合為 Stage 5 的實現方式之一
- **B2a/B2b (Multi-Agent)** — 每個 Stage 可由不同 Agent 負責

## 來源筆記

- docs/03-研究方向深度設計.md 方向 1：Structured Financial Reasoning Decomposition
- 認知心理學的問題解決階段理論（Newell & Simon, 1972）
- FinDAP (EMNLP 2025) 揭示的 LLM 金融推理弱點
