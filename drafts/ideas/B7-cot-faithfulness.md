# B7 CoT 的忠實度測試：金融推理中的因果介入實驗
# Chain-of-Thought Faithfulness in Financial Reasoning: Causal Intervention on LLM Reasoning Chains

## 研究問題

當 LLM 輸出 "Step 1: ..., Step 2: ..., Answer: X" 的 Chain-of-Thought 推理時，這個推理過程是否真正驅動了最終答案？還是模型先決定了答案，再生成 post-hoc justification？這個問題對所有基於 CoT 的 CFA 實驗具有根本性影響：如果 CoT 是不忠實的（unfaithful），那麼 B1（五階段推理管道）、E1（錯誤歸因圖譜）等依賴推理過程分析的研究，其結論可靠性都需要重新審視。本研究透過 causal intervention——刻意修改推理鏈中的中間步驟，觀察最終答案是否相應改變——來量化 CoT faithfulness。

## 核心方法

**Causal Intervention Protocol（五步驟）**

1. **Baseline CoT 收集**：讓 LLM 正常生成完整 CoT + 答案，記錄每個推理步驟。
2. **Intervention Point 識別**：在 CoT 中找到可介入的中間步驟（公式選擇、數值代入、判斷前提）。
3. **施加介入（三種類型）**：
   - Type I Formula Swap：將正確公式替換為相關但錯誤的公式（如 Modified Duration -> Macaulay Duration）
   - Type II Value Perturbation：修改中間計算數值（如將正 NPV 改為負 NPV）
   - Type III Premise Reversal：反轉判斷前提（如「利率上升」-> 「利率下降」）
4. **續生推理**：從 intervention point 之後讓模型繼續生成至最終答案。
5. **忠實度判定**：答案改變 = faithful，答案不變 = unfaithful，答案改變但方向錯誤 = partially faithful。

**Faithfulness Score** = (答案改變的題目數) / (總介入題目數)，按 Cognitive Demand Level（G4）、CFA Topic、Intervention Type 分層計算。

## 實驗設計

**Exp 1: Baseline Faithfulness Profiling** — 從 CFA-Easy 抽取 300 題 + CFA-Challenge 全部 90 題。對每題生成 CoT、識別 intervention point、施加介入。測試 gpt-4o, gpt-4o-mini, qwen3:32b, deepseek-r1:14b, llama3.1:8b。

**Exp 2: Faithfulness by Question Type** — 假說 1：Calculation questions（Level 2）faithfulness 高，因為數值計算是 deterministic。假說 2：Judgment questions（Level 4-5）faithfulness 低，因為模型可能繞過修改的前提。使用 G4 Cognitive Demand Level 分層。

**Exp 3: Intervention Strength** — 同一題施加 weak/medium/strong 介入。若推理忠實，Faithfulness Rate 應隨介入強度單調上升。

**Exp 4: Cross-model Comparison** — 比較不同模型的 faithfulness。假說：reasoning-specialized 模型（deepseek-r1）高於 general models。

## 需要的積木
- ✅ CFA-Challenge (90) + CFA-Easy (1,032) — 已就緒
- ✅ 多模型推論能力 — Ollama local + OpenAI API
- ❌ Intervention Point 識別器 — 需設計 prompt 讓 GPT-4o 識別 CoT 中可介入步驟
- ❌ Intervention 施加與續生工具 — 需開發自動修改 CoT 中間步驟並續生的程式
- ❌ G4 Cognitive Demand Labels — 用於分層分析（可與 G4 並行）
- ❌ Faithfulness 評判器 — 部分案例需人工裁定答案是否「因介入而改變」

## 預期產出
- CFA Financial Reasoning 的 CoT Faithfulness Profile：首個專業金融領域的 CoT 忠實度量化
- 預期關鍵發現：Calculation questions faithfulness ~80-90%；Judgment questions ~40-60%；Ethical reasoning ~30-50%
- 方法論貢獻：Causal Intervention Protocol 可遷移至其他專業領域
- 對其他論文的影響：若 judgment 題 faithfulness 低，B1 Stage 5 與 E1 reasoning trace 分析需加入 caveat

## 資料需求
| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | 全部進入實驗 | 已就緒 |
| FinEval-CFA-Easy (1,032) | 隨機抽取 300 題 | 已就緒 |
| CFA_Extracted (1,124) | 輔助 intervention point 設計 | 已就緒 |
| G4 Cognitive Demand Labels | 分層分析 | 需等待 G4（可並行）|

## 模型需求
- **被測**：gpt-4o, gpt-4o-mini, qwen3:32b, qwen3:30b-a3b, deepseek-r1:14b, llama3.1:8b
- **輔助**：GPT-4o 用於 intervention point 識別
- 不需要 fine-tuning，純 inference。API 費用預估 $300-500。

## 狀態
可與 G4 並行啟動。建議先在 20 題上 pilot，驗證 Causal Intervention Protocol 可行性後再擴大。

## 可合併的點子
- **B1 (5-Stage Pipeline)** — B7 結果直接影響 B1 Stage 5 的可信度
- **E1 (Error Pattern Atlas)** — 若 CoT 不忠實，reasoning trace 分析需加入 faithfulness caveat
- **G1 (Ability Matrix)** — B7 的 Prompt Sensitivity 結果填入 G1 Layer 3
- **G4 (Cognitive Demand Taxonomy)** — G4 的 level 標籤是 B7 分層分析的基礎

## 來源筆記
- 新點子，靈感來自 NLP 社群對 CoT faithfulness 的討論
- Turpin et al. (2023) "Language Models Don't Always Say What They Think"
- Lanham et al. (2023) "Measuring Faithfulness in Chain-of-Thought Reasoning"
- 差異化：(1) 專業金融領域 (2) causal intervention 而非 correlation (3) 按認知需求分層
- 目標：ACL / EMNLP 2026 (Interpretability / Reasoning Track)
