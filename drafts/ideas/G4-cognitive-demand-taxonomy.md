# G4 CFA 題目認知需求分類法
# Cognitive Demand Taxonomy for CFA Exam Questions: An Annotated Dataset and Classification Framework

## 研究問題

CFA 考試題目表面上都是選擇題，但認知需求天差地遠：有的只要背定義，有的需要五步計算，有的要在模糊條件下做整合判斷。現有研究在報告 AI 正確率時從未區分這些層次——把「recall 一個定義」和「在不完整資訊下做投資建議」放在同一個 accuracy 數字裡，嚴重模糊了 AI 的真實能力邊界。本研究建構一套 5-level Cognitive Demand Taxonomy，對全部可用 CFA 題目進行自動分類並以人工驗證，產出一個 annotated dataset 作為公共資源。此分類是多篇後續論文的 building block。

## 核心方法

**5-Level Cognitive Demand Taxonomy**

- Level 1 Recall：直接記憶事實、定義、術語。認知動詞：define, identify, list。
- Level 2 Calculation：將給定數值代入已知公式，公式選擇無歧義。認知動詞：calculate, compute。
- Level 3 Application：在具體情境中選擇正確方法或公式。認知動詞：apply, select, use。
- Level 4 Analysis：多步驟推理、比較替代方案、辨識條件間關係，存在 distractor。認知動詞：analyze, compare, evaluate。
- Level 5 Synthesis：模糊或不完整條件下整合多主題、做帶有不確定性的判斷。認知動詞：integrate, justify, recommend。

**雙階段分類流程**

Stage A（自動分類）：GPT-4o 對每道題目分類。Prompt 包含 taxonomy 定義、每 level 範例、要求輸出分類理由。

Stage B（人工驗證）：隨機抽取 100 題，2 位具 CFA 知識的標註者獨立分類。計算 inter-rater agreement（Cohen's Kappa）與 GPT-4o vs 人工一致性。目標 Kappa >= 0.7。

## 實驗設計

1. **Taxonomy 校準**：在 50 題小樣本上測試可操作性，調整 level 邊界定義直到 agreement 穩定。
2. **大規模分類**：對四個資料集全部題目（CFA-Challenge 90 + CFA-Easy 1,032 + CFA_Extracted 1,124 + CRA-Bigdata 1,472）進行 GPT-4o 自動分類。
3. **人工驗證**：100 題 x 2 annotators。分析分歧集中在哪些 level 邊界（預期 Level 3/4 最模糊）。
4. **分布分析**：報告每個資料集各 level 題目分布。預期 CFA-Easy 以 Level 1-2 為主，CFA-Challenge 以 Level 3-5 為主。
5. **AI Performance by Level**：按 level 重新分析 AI 正確率。預期 Level 1-2 > 90%，Level 5 < 50%。

## 需要的積木
- ✅ CFA-Challenge (90) + CFA-Easy (1,032) + CFA_Extracted (1,124) + CRA-Bigdata (1,472) — 已就緒
- ✅ GPT-4o API — 自動分類
- ✅ Ollama local models — AI Performance by Level 實驗
- ❌ Taxonomy coding guide — 含邊界案例處理規則
- ❌ 人工標註 — 2 位標註者 x 100 題，約 20-30 小時
- ❌ 分類 prompt template — 需設計並迭代

## 預期產出
- **Annotated Dataset**：全部 CFA 題目附 Cognitive Demand Level 標籤（核心貢獻，可公開釋出）
- GPT-4o 自動分類器的驗證報告（per-level precision/recall, confusion matrix）
- AI Performance by Cognitive Demand Level 的衰減曲線——首次展示 AI 能力隨認知需求升高而衰減

## 資料需求
| 資料集 | 題數 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge | 90 | 已就緒 |
| FinEval-CFA-Easy | 1,032 | 已就緒 |
| CFA_Extracted | 1,124 | 已就緒 |
| CRA-Bigdata | 1,472 | 已就緒 |

## 模型需求
- **分類器**：GPT-4o（API）
- **被測模型**：gpt-4o, gpt-4o-mini, qwen3:32b, deepseek-r1:14b, llama3.1:8b
- 不需要 fine-tuning，純 inference

## 狀態
可立即開始 — 不依賴其他論文。建議作為早期 building block 優先執行，因產出被 G1, E1, B1, B7 多篇論文需要。

## 可合併的點子
- **G1 (Ability Matrix)** — G4 的 Level 標註直接對應 G1 的 Ability Type mapping
- **A1 (Open-Ended Numerical)** — A1 聚焦計算題，G4 的 Level 2 是其核心範圍
- **E1 (Error Pattern Atlas)** — 可按 Cognitive Demand Level 分層分析錯誤分布
- **B7 (CoT Faithfulness)** — 預期在不同 Level 觀察到不同 faithfulness

## 來源筆記
- docs/03-研究方向深度設計.md — 方向 1 的認知階段理論啟發 taxonomy 設計
- Bloom's Taxonomy (1956)、Webb's Depth of Knowledge (2002) 為教育測量經典框架
- 定位為 dataset/resource paper，目標：NeurIPS Datasets & Benchmarks Track 或 ACL Resource Paper
