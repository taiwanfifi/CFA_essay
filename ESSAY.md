## 問題 2：論文發表順序建議

考量因素：難度、數據量、創新性、發表速度

### 我推薦的順序

| 優先級 | 系列 | 論文題目方向 | 理由 |
|--------|------|-------------|------|
| 1 | E（錯誤分析） | "Where Do LLMs Fail on CFA Exams? A Taxonomy of Financial Reasoning Errors" | 最容易做！用現有實驗結果分析錯誤類型，不用跑新實驗。Negative finding 也能發。 |
| 2 | A1（開放式評估） | "Beyond Multiple Choice: Open-Ended Numerical Reasoning Benchmark for Financial LLMs" | 建 benchmark 的論文容易被引用。把選擇題改開放式，測「真正會算」vs「猜對」的差距。 |
| 3 | D1（信心校準） | "Calibration of LLM Confidence on Financial Reasoning Tasks" | 熱門議題（AI safety 相關）。測 AI 說「我確定」時是不是真的對。 |
| 4 | B（推理策略） | "Tool-Augmented Reasoning for Financial Calculations: Limitations and Lessons" | 我們已經有數據了！但結論是 negative（工具沒用），要包裝成「為什麼沒用」的分析論文。 |
| 5 | G3（抗 AI 考題） | "Designing AI-Resistant Financial Exam Questions" | 有話題性，但需要跟 CFA Institute 或考試機構合作才有公信力。 |

---

### 最快出第一篇的路徑

E 系列（錯誤分析） — 因為：

1. 已經有數據：90 題 × 5 方法 = 450 個答題結果，夠分析了
2. 不用跑新實驗：只需要人工標註錯誤類型
3. Negative finding 也有價值：「LLM 在 X 類題目特別弱」是有用的發現
4. 可以當「前導論文」：後續論文都可以引用這篇的錯誤分類框架

具體做法：

1. 把 90 題按主題分類（倫理、固收、衍生品...）
2. 把錯誤按類型分類（概念錯、計算錯、理解題意錯...）
3. 找出「哪類題目 × 哪種錯誤」的 pattern
4. 寫成論文

---

## E1 定義 vs 我們的 POC

| 方面 | ideas_export.txt 的定義 | 我們的 POC |
|------|------------------------|-----------|
| 維度 1：Error Type | 4 大類 12 子類 | 8 大類 16 子類 ✅ 更細 |
| 維度 2：CFA Topic | 10 類 | 11 類（加了 wealth_planning）✅ |
| 維度 3：Cognitive Stage | B1 的 5-stage pipeline | ❌ 尚未實作 |
| Cross-model 分析 | 8+ 模型 | ❌ 只跑了 gpt-4o-mini |
| Ground truth 驗證 | 200 題人工標註 + Cohen's Kappa | ❌ 尚未做 |

---

### 我們的 POC 發現

```
--- By Error Type ---
  reasoning_premise_error         22 ( 48.9%)  ← 最大宗！
  reasoning_chain_break            9 ( 20.0%)
  calc_arithmetic_error            4 (  8.9%)
  calc_formula_error               3 (  6.7%)
  ...
```

這和原始 E1 設計的預期高度吻合：

- 原始設計的 "Misapplication" 類別對應我們的 `reasoning_premise_error`
- 原始設計的 "Calculation Error" 對應我們的 `calc_*` 系列
- 發現 48.9% 的錯誤是「理解題意錯誤」，而不是計算問題

---

### 下一步：完善 E1 實驗

需要補齊的：

1. 加入 Dimension 3（Cognitive Stage） — 識別錯誤發生在哪個認知階段
2. 跑多模型 — 至少加 gpt-4o, qwen3:32b, llama3.1:8b
3. 人工驗證 100-200 題 — 計算 Cohen's Kappa
4. 視覺化 — 建立 Error Pattern Atlas heat map

---

## E1 完整錯誤分析結果（229 個錯誤，5 種方法）

### 三維度分類結果

#### 維度 1：錯誤類型（Error Type）

| 錯誤類型 | 數量 | 佔比 | 說明 |
|----------|------|------|------|
| reasoning_premise_error | 113 | 49.3% | 搞錯題目在問什麼 |
| reasoning_chain_break | 34 | 14.8% | 推理步驟斷裂 |
| selection_random | 22 | 9.6% | 無理由亂選 |
| calc_arithmetic_error | 20 | 8.7% | 算術錯誤 |
| selection_near_miss | 16 | 7.0% | 算對但選錯 |
| concept_misunderstanding | 10 | 4.4% | 概念完全錯誤 |
| calc_formula_error | 9 | 3.9% | 公式錯誤 |
| concept_incomplete | 5 | 2.2% | 概念不完整 |

核心發現：近半數錯誤（49.3%）是「理解題意錯誤」，只有 12.6% 是計算相關錯誤（算術 + 公式）。

---

#### 維度 2：CFA 主題（Topic）

| 主題 | 錯誤數 | 佔比 |
|------|--------|------|
| ethics | 70 | 30.6% |
| portfolio | 45 | 19.7% |
| fixed_income | 35 | 15.3% |
| wealth_planning | 27 | 11.8% |
| derivatives | 24 | 10.5% |
| economics | 17 | 7.4% |
| alternatives | 7 | 3.1% |
| equity | 4 | 1.7% |

---

#### 維度 3：認知階段（Cognitive Stage）

| 階段 | 數量 | 佔比 | 說明 |
|------|------|------|------|
| identify | 123 | 53.7% | 辨識題目考什麼（Stage 1） |
| verify | 50 | 21.8% | 驗證答案合理性（Stage 5） |
| unknown | 22 | 9.6% | 無法判斷 |
| calculate | 20 | 8.7% | 計算步驟（Stage 4） |
| recall | 14 | 6.1% | 回想公式/規則（Stage 2） |

核心發現：超過一半的錯誤（53.7%）發生在第一階段「辨識題目」，模型沒開始推理就已經走歪了。

---

### 各方法的錯誤特徵比較

| 方法 | 錯誤數 | 主要錯誤類型 | 主要失敗階段 |
|------|--------|-------------|-------------|
| zero_shot | 53 | premise_error (43%) | identify (45%) |
| cot_verify | 46 | premise_error (59%) | identify (61%) |
| cot | 45 | premise_error (49%) | identify (56%) |
| structured | 45 | premise_error (38%) + random (29%) | identify (44%) |
| agent_naive | 40 | premise_error (60%) | identify (65%) |

觀察：

- agent_naive 錯誤最少（40），且錯誤高度集中在 identify 階段
- structured 有異常高的 selection_random（29%）— 可能是分類路由造成的混亂
- 所有方法的主要失敗點都是 identify 階段

---

### 主題 × 錯誤類型 交叉分析

| Topic | reasoning_premise | reasoning_chain | selection_random | calc_arithmetic | selection_near |
|-------|-------------------|-----------------|------------------|-----------------|----------------|
| ethics | 54 | 7 | 0 | 0 | 0 |
| portfolio | 23 | 5 | 6 | 6 | 1 |
| fixed_income | 9 | 3 | 6 | 6 | 6 |
| wealth_planning | 10 | 12 | 1 | 1 | 3 |
| derivatives | 5 | 5 | 4 | 7 | 0 |
| economics | 6 | 0 | 3 | 0 | 6 |

觀察：

- **Ethics**：幾乎 100% 是推理錯誤（premise + chain），沒有計算錯誤 → 工具策略對倫理題完全無用
- **Fixed Income & Derivatives**：計算錯誤比例較高（~20%）→ 這些主題才是工具策略可能有效的地方
- **Wealth Planning**：reasoning_chain_break 異常高（44%）→ 需要多步驟整合判斷的題目

---

## 論文核心 Finding

1. **LLM 在 CFA 考試的主要失敗模式不是計算能力不足，而是「辨識題目在問什麼」的能力不足**（49.3% reasoning_premise_error，53.7% identify stage）
2. **工具策略失敗的原因找到了**：因為主要錯誤是「理解題意」，不是「算不動」。只有 12.6% 的錯誤是計算相關，而這些主要集中在 fixed_income 和 derivatives
3. **不同主題需要不同的修復策略**：
   - Ethics → 需要更好的情境理解能力（不是工具）
   - Fixed Income / Derivatives → 可能受益於計算器工具
   - Wealth Planning → 需要多步驟推理能力

---

### 結果檔案

`experiments/E1_error_analysis/results/error_analysis_all_methods_20260203_230751.json`

這就是 E1 的完整實驗結果！這個發現本身就足以寫一篇論文："Where Do LLMs Fail on CFA Exams? A Taxonomy of Financial Reasoning Errors"
