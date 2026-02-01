# B4 CFA 自一致性投票策略
# Self-Consistency Voting Strategies for CFA

## 研究問題

Self-Consistency（Wang et al., 2023）透過多次採樣並投票來提升 LLM 推理準確率，已在數學推理基準上展示有效性。然而在金融專業考試的情境中，幾個關鍵問題尚未被探究：(1) 最佳採樣數 k 為何？(2) 不同的投票策略（majority vote vs 頻率加權 vs 信心加權）對 CFA 題目的效果差異如何？(3) 哪些 CFA 主題從投票中受益最大、哪些幾乎不受影響？(4) 成本-準確率的 Pareto 最優點在哪裡？

## 核心方法

**採樣設計**
- 對每道 CFA 題目在 temperature=0.7 下採樣 k 個回答
- 測試 k = 3, 5, 10, 15, 20
- 記錄每次採樣的答案選項與推理過程

**投票策略對比**

1. **Majority Vote** — 選擇出現次數最多的答案，最簡單的 baseline
2. **Frequency-Weighted Vote** — 以答案出現頻率作為權重，等價於 majority vote 但提供連續的 confidence score
3. **Confidence-Weighted Vote** — 每次採樣附帶 verbalized confidence (0-100%)，以信心分數加權投票
4. **Reasoning-Consistency Vote** — 分析推理路徑的一致性：相同答案但不同推理路徑 vs 相同推理路徑但不同答案，給予推理一致的答案更高權重
5. **Hybrid Vote** — 結合頻率 + 信心 + 推理一致性的綜合策略

## 實驗設計

- **Exp 1: 投票策略全面對比** — 在 CFA-Challenge (90) + CFA-Easy (1,032) 上，五種投票策略 x 五種 k 值 = 25 組實驗。報告準確率、token 消耗、每組的投票穩定性。
- **Exp 2: 最佳 k 的 Pareto 分析** — 橫軸為 total tokens (proxy for cost)，縱軸為 accuracy。繪製 Pareto frontier，找出 cost-accuracy 最佳平衡點。假說：k=5 或 k=10 為甜蜜點，更大的 k 邊際收益遞減。
- **Exp 3: 按 CFA 主題分析** — 分析哪些主題從 self-consistency 受益最大。假說：計算類主題（Fixed Income, Derivatives）受益較多（計算偶發錯誤可被多數票修正），而 Ethics 題目受益較少（模型對同一倫理問題傾向給出相同錯誤答案）。
- **Exp 4: 模型規模效應** — 比較小模型 (phi3.5:3.8b, qwen3:4b) vs 大模型 (qwen3:32b, gpt-4o) 的 self-consistency 增益。假說：小模型的增益更大（因為小模型的隨機性更高，投票更能糾錯）。

## 需要的積木

- ✅ CFA 測試資料集 — FinEval-CFA-Challenge (90), CFA-Easy (1,032)
- ✅ 多規模模型 — phi3.5:3.8b, qwen3:4b, llama3.1:8b, qwen3:32b (Ollama) + gpt-4o (API)
- ✅ 溫度採樣能力 — Ollama 與 OpenAI API 皆支援 temperature 設定
- ❌ 批次採樣 pipeline — 自動化多次採樣並收集結果
- ❌ 投票策略實作 — 五種投票演算法
- ❌ CFA 主題標註 — 按 CFA 十大主題分類每道題目（~10hr，可與 B1 共用）

## 預期產出

- 五種投票策略的完整對比表，識別出 CFA 領域的最佳投票策略
- 成本-準確率 Pareto frontier 圖，指導實際應用中的 k 值選擇
- 預期 majority vote 即為最佳策略（與一般 NLP 研究一致），但 reasoning-consistency 可能在特定主題上有優勢
- 預期最佳 k 值約為 5-10，k>15 的邊際準確率提升 < 0.5%
- CFA 主題別分析：計算題受益最大（+5-8%），Ethics 受益最小（+0-2%）

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | 困難題測試 | 已就緒 |
| FinEval-CFA-Easy (1,032) | 主測試集 | 已就緒 |
| CRA-Bigdata (1,472) | 擴展驗證（可選） | 已就緒 |

## 模型需求

- **Local (Ollama)**: phi3.5:3.8b, qwen3:4b, llama3.1:8b, qwen3:32b（規模梯度）
- **API**: gpt-4o, gpt-4o-mini（commercial models 的 self-consistency 行為）
- **注意**：k=20 的採樣意味著 20x token 消耗，local 模型可降低成本

## 狀態

🔲 尚未開始 — 概念簡單但需要大量推論計算（每題 k 次採樣）

## 可合併的點子

- **B3 (Self-Verification)** — 先 self-consistency 再 self-verification：投票選出候選後再驗證
- **B5 (Dual-Process)** — Self-consistency 的 agreement rate 可作為 System 1 的信心估計
- **B1 (5-Stage Pipeline)** — 在每個 Stage 分別進行 self-consistency，定位哪個 Stage 最受益

## 來源筆記

- Self-Consistency (Wang et al., 2023) — 原始論文在 GSM8K 等數學基準上驗證
- 新構想：將 self-consistency 系統性應用於金融專業考試
- docs/03 方向 2 中 Self-Consistency Variance 作為信心估計方法的討論
