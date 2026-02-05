# POC 實驗結果總覽

> **模型**: gpt-4o-mini | **日期**: 2026-02-04 ~ 02-05 | **資料集**: CFA-Easy (前 5 題) + D1 校準結果 (250 筆)

本文件記錄六個實驗的 POC（Proof of Concept）執行結果。每個 POC 的目的是驗證管道跑通，而非產出統計顯著的結論。完整實驗需放大到全部題目 + 多模型。

---

## 總覽

| 實驗 | N | 核心指標 | 數值 | 管道狀態 |
|------|---|----------|------|---------|
| A5 Option Bias | 5 題 | Option Bias (MCQ - Open) | **-40.0%** | OK |
| I3 Noise | 5 題 × 4 雜訊 | NSI (all types) | **0.000** | OK |
| D4 Overconfident Risk | 250→74→5 | High-risk errors / classified | **5/5 high** | OK |
| A1 Open-Ended | 5 題 | Strict / Lenient accuracy | **60% / 80%** | OK |
| I1 Counterfactual | 5 題 | Memorization Gap | **+10.0%** | OK |
| I2 Behavioral Biases | 10 情境 | Avg Bias Score | **0.500** | OK |

---

## A5: Option Bias

**問題**：MCQ 選項是幫助還是干擾？

| 指標 | 數值 |
|------|------|
| Accuracy WITH options | 60.0% (3/5) |
| Accuracy WITHOUT options | 100.0% (5/5) |
| Option Bias | -40.0%（去選項反而更好） |
| Biased questions (有選項才對) | 0/5 |
| McNemar p-value | 0.4795 (不顯著) |
| Token 用量 | 4,825 |
| 成本 | $0.0018 |

### 逐題結果

| 題目 | MCQ 答案 | MCQ 正確 | Open 正確 | 評判方式 |
|------|---------|---------|----------|---------|
| easy_0 | C | ✓ | ✓ | LLM Judge |
| easy_1 | C | ✓ | ✓ | LLM Judge |
| easy_2 | A | ✓ | ✓ | LLM Judge |
| easy_3 | A (金標 C) | ✗ | ✓ | Numerical Match |
| easy_4 | C (金標 B) | ✗ | ✓ | Numerical Match |

**初步觀察**：gpt-4o-mini 在開放式作答時反而表現更好。easy_3 和 easy_4 在 MCQ 格式下選錯字母，但在開放式計算中數值正確。這暗示 MCQ 選項可能造成「選項干擾」——模型計算能力沒問題，但在字母選擇上出錯。

---

## I3: Noise & Red Herrings

**問題**：注入無關資訊是否影響模型判斷？

| 雜訊類型 | 說明 | 雜訊後正確率 | 翻轉數 | NSI |
|---------|------|------------|--------|-----|
| Clean (基準) | — | 60.0% | — | — |
| N1 | 無關數據注入 | 60.0% | 0/5 | 0.000 |
| N2 | 金融干擾項 | 60.0% | 0/5 | 0.000 |
| N3 | 冗長前言 | 60.0% | 0/5 | 0.000 |
| N4 | 矛盾提示 | 60.0% | 0/5 | 0.000 |

**Intensity**: 2（每題插入 2 條雜訊）

**初步觀察**：5 題小樣本中 gpt-4o-mini 完全不受四種雜訊影響——對的題仍然對，錯的題仍然錯。需要放大樣本量才能偵測到 NSI > 0 的情況，尤其是 N4（矛盾提示）在更多題目中可能展現效果。

---

## D4: Overconfident Risk

**問題**：D1 校準實驗中，高信心錯誤的金融風險有多嚴重？

| 指標 | 數值 |
|------|------|
| D1 總結果數 | 250 筆 |
| 高信心錯誤 (≥80%) | 74 筆 (29.6%) |
| 平均錯誤信心 | 89.0% |
| 已分類筆數 | 5 (POC 限制) |
| 集體幻覺 | 0 題 |

### 風險分類結果 (前 5 筆)

| 題目 | 信心 | 風險等級 | 風險類別 |
|------|------|---------|---------|
| challenge_6 | 100% | high | decision-making risk |
| challenge_12 | 100% | high | decision-making risk |
| challenge_14 | 100% | high | decision-making risk |
| challenge_15 | 100% | high | decision-making risk |
| challenge_23 | 100% | high | decision-making risk |

**初步觀察**：近三成 (29.6%) 的 D1 結果屬於高信心錯誤。被分類的 5 筆全部信心 100% 且判定為 high 風險——這些是最危險的案例：模型完全確信自己正確，但答案是錯的。完整分類需要跑全部 74 筆。

---

## A1: Open-Ended Benchmark

**問題**：去掉 MCQ 選項後，用三層判定（精確 / 方向 / 錯誤）評估表現如何？

| 指標 | 數值 |
|------|------|
| Level A (Exact) | 3/5 (60.0%) |
| Level B (Directional) | 1/5 (20.0%) |
| Level C (Incorrect) | 1/5 (20.0%) |
| Strict accuracy (A only) | 60.0% |
| Lenient accuracy (A+B) | 80.0% |

### 逐題結果

| 題目 | Level | 金標數值 | 模型數值 | 自動/裁判 | 錯誤歸因 |
|------|-------|---------|---------|----------|---------|
| easy_0 | A (Exact) | 概念題 | — | LLM Judge | — |
| easy_1 | B (Directional) | 概念題 | — | LLM Judge | — |
| easy_2 | C (Incorrect) | 365 | 4.07 | Auto (數值) | incomplete_reasoning |
| easy_3 | A (Exact) | 113,733 | 111,817 | Auto (±2%) | — |
| easy_4 | A (Exact) | 97,532 | 97,561 | Auto (±2%) | — |

**初步觀察**：三層判定機制運作正常。數值型題目（easy_2~4）使用自動容差匹配，概念型題目（easy_0~1）使用 LLM 裁判。easy_2 被判為 Level C 是因為模型輸出的數值（4.07）與金標（365）差異太大——這是一題關於複利頻率的題目，模型可能計算了不同的目標值。

---

## I1: Counterfactual Testing

**問題**：模型是在推理還是在記憶？改變數值後還能答對嗎？

| 指標 | 數值 |
|------|------|
| 原題正確率 | 60.0% (3/5) |
| 微擾題正確率 (Level 1) | 50.0% (2/4) |
| Memorization Gap | +10.0% |
| Robust Accuracy | 40.0% (2/5) |
| Memorization Suspect | +20.0% |
| 微擾生成失敗 | 1/5 |

### 逐題結果

| 題目 | 原題 | Level 1 微擾 | 分類 |
|------|------|-------------|------|
| easy_0 | ✓ | ✓ | Robust Correct |
| easy_1 | ✓ | FAIL (生成失敗) | — |
| easy_2 | ✓ | ✗ | **Memorization Suspect** |
| easy_3 | ✗ | ✗ | Robust Incorrect |
| easy_4 | ✗ | ✓ | Improved |

**初步觀察**：

- **easy_2** 原題答對但微擾版答錯 → 記憶嫌疑最高
- **easy_4** 原題答錯但微擾版答對 → 有趣的反轉案例
- 微擾生成有 20% 失敗率（easy_1），完整實驗中需追蹤此比率
- Robust Accuracy (40%) < Original Accuracy (60%) → 約 1/3 的「正確」可能是記憶而非推理

---

## I2: Behavioral Biases

**問題**：LLM 是否展現行為金融學偏誤？

| 指標 | 數值 |
|------|------|
| 測試情境數 | 10 |
| 偏誤類型 | Loss Aversion, Anchoring |
| 平均偏誤分數 (bias-inducing) | 0.500 |
| 平均偏誤分數 (neutral) | 0.300 |
| 平均去偏效果 | +0.200 |

### 按偏誤類型

| 偏誤類型 | N | Bias Score | Neutral Score | 去偏效果 |
|---------|---|-----------|--------------|---------|
| Loss Aversion | 5 | 0.500 | 0.300 | +0.200 |
| Anchoring | 5 | 0.500 | 0.300 | +0.200 |

### 逐題偏誤分數

| 情境 | 偏誤類型 | Bias | Neutral | 去偏 |
|------|---------|------|---------|------|
| la_01 | Loss Aversion | 0.50 | 0.00 | +0.50 |
| la_02 | Loss Aversion | 0.50 | 0.50 | +0.00 |
| la_03 | Loss Aversion | 0.50 | 0.50 | +0.00 |
| la_04 | Loss Aversion | 0.50 | 0.00 | +0.50 |
| la_05 | Loss Aversion | 0.50 | 0.50 | +0.00 |
| an_01 | Anchoring | 0.50 | 0.50 | +0.00 |
| an_02 | Anchoring | 0.50 | 0.00 | +0.50 |
| an_03 | Anchoring | 0.50 | 0.50 | +0.00 |
| an_04 | Anchoring | 0.50 | 0.50 | +0.00 |
| an_05 | Anchoring | 0.50 | 0.00 | +0.50 |

**初步觀察**：

- 所有 bias-inducing 版本都得到 0.50 分（半理性半偏誤），顯示 gpt-4o-mini 在誘導性情境中傾向「兩邊都提」而非明確偏向一方
- 中性框架可將偏誤降至 0.30——約 40% 的情境（4/10）在中性框架下完全理性（0.00）
- 去偏效果呈二元分布：要麼完全去偏（+0.50），要麼完全無效（+0.00）
- 尚未測試 framing、recency、disposition effect 三種偏誤

---

## 管道驗證結論

| 檢查項目 | 結果 |
|---------|------|
| API 呼叫 → 回應 | ✓ |
| 答案提取 (regex) | ✓ |
| 數值提取 | ✓ |
| LLM-as-Judge | ✓ |
| 容差匹配 (±2%) | ✓ |
| McNemar 檢定 | ✓ |
| JSON 輸出格式 | ✓ |
| 雜訊注入 (4 類) | ✓ |
| 微擾生成 (GPT 驅動) | ⚠ 80% 成功率 |
| 偏誤評分 | ✓ |
| D1 結果讀取 + 篩選 | ✓ |
| 風險分類 | ✓ |

**全部 6 個管道已驗證跑通**。可以進入完整實驗階段。

---

## 下一步

1. **放大樣本**：全部 CFA-Easy (1,032 題) + CFA-Challenge (90 題)
2. **多模型比較**：gpt-4o, qwen3:32b, llama3.1:8b, deepseek-r1:14b
3. **I2 補齊**：跑剩餘 4 種偏誤（framing, recency, disposition, overconfidence）
4. **D4 完整分類**：分類全部 74 筆高信心錯誤
5. **I1 多層微擾**：加入 Level 2 (雙參數) 和 Level 3 (結構性) 微擾
6. **跨實驗整合**：將 A5 + A1 結合分析 MCQ vs Open-Ended 完整圖景
