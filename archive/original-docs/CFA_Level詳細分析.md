# CFA Level詳細分析報告

## 📋 CFA考試Level基本知識

### Level 1、2、3的題型差異

| Level | 題型 | 題數 | 特點 |
|-------|------|------|------|
| **Level 1** | 全選擇題 | 180題 | 基礎概念，獨立選擇題 |
| **Level 2** | 題組選擇題 | 88題（22組×4題） | 案例基礎，每組4題 |
| **Level 3** | **申論題 + 題組選擇題** | 各佔50% | **包含申論題（Essay）** |

### 重要區別

- **Level 1 & 2**: 主要是選擇題
- **Level 3**: **包含申論題（Essay Questions）**，要求寫出完整答案

---

## 🔍 數據集Level分析結果

### 1. FinEval-CFA-Challenge

**Level信息**: ❌ **未明確標註**

**題目類型**: 
- ✅ 選擇題（A, B, C）
- ✅ 包含場景（Scenario-based）
- ❌ 不是申論題

**來源**: 
- "sample_test"
- "2020 Mock PM"

**結論**: 
- 很可能是**Level 2或Level 3的選擇題部分**
- 因為有場景描述，更像是Level 2的題組形式
- **不是Level 3的申論題**

---

### 2. FinEval-CFA-Easy

**Level信息**: ❌ **未明確標註**

**題目類型**: 
- ✅ 選擇題（A, B, C）
- ❌ 沒有場景描述
- ❌ 不是申論題

**來源**: 
- 樣本題和練習題

**結論**: 
- 很可能是**Level 1的基礎選擇題**
- 題目較簡單，沒有複雜場景

---

### 3. CFA_Level_III ⚠️ 重要發現

**Level信息**: ✅ **名稱標註為Level III**

**題目類型**: 
- ✅ **選擇題（A, B, C）** ← **重要！**
- ✅ 包含場景（Scenario-based）
- ❌ **不是申論題！**

**實際檢查結果**:
```
樣本0-9全部都是：
- Query: "select the most appropriate answer from the options A, B and C"
- Answer: A/B/C (單個字符)
- 答案長度: 1字符
- 包含選擇項: True
- 可能是申論題: False
```

**來源**: 
- "sample_test"
- "2020 Mock PM"

**年份**: 2020

**結論**: 
- ⚠️ **雖然名稱是CFA_Level_III，但實際內容是選擇題，不是申論題**
- 可能是Level 3考試中的**選擇題部分**（Level 3有50%是選擇題）
- **不是Level 3的申論題部分**
- 樣本量很少（90題）

---

### 4. FinTrain-cfa_exercise

**Level信息**: ✅ **明確標註為Level II**

**題目類型**: 
- ✅ 選擇題
- ✅ 來自SchweserNotes Level II材料

**來源**: 
- "CFA 2020 Level II - SchweserNotes Book 4.txt"

**年份**: 2020

**結論**: 
- ✅ **明確是Level II**
- 來自SchweserNotes備考材料

---

### 5. CFA_Extracted系列

**Level信息**: ✅ **明確標註為Level II**

**題目類型**: 
- ✅ 選擇題和計算題
- ✅ 來自SchweserNotes Level II材料

**來源**: 
- "CFA 2020 Level II - SchweserNotes Book 4.txt"

**年份**: 2020

**結論**: 
- ✅ **明確是Level II**
- 來自SchweserNotes備考材料

---

## 📊 數據集Level分布總結

| 數據集 | Level | 題目類型 | 年份 | 樣本數 | 備註 |
|--------|-------|----------|------|--------|------|
| **FinEval-CFA-Challenge** | ❓ 未明確 | 選擇題（場景題） | 2020 | 90 | 可能是Level 2或3的選擇題部分 |
| **FinEval-CFA-Easy** | ❓ 未明確 | 選擇題（基礎題） | - | 1,032 | 可能是Level 1 |
| **CFA_Level_III** | ✅ Level III | **選擇題**（非申論題） | 2020 | 90 | ⚠️ 是Level 3的選擇題部分，不是申論題 |
| **FinTrain-cfa_exercise** | ✅ Level II | 選擇題 | 2020 | 2,946 | 明確Level II |
| **CFA_Extracted系列** | ✅ Level II | 選擇題/計算題 | 2020 | 1,124-2,946 | 明確Level II |

---

## ⚠️ 重要發現

### 發現1: 沒有真正的Level 3申論題數據

- **CFA_Level_III數據集雖然名稱是Level III，但實際都是選擇題**
- 可能是Level 3考試中的選擇題部分（Level 3有50%是選擇題）
- **沒有找到真正的Level 3申論題數據**

### 發現2: FinEval系列未明確標註Level

- FinEval-CFA-Challenge和CFA-Easy都沒有明確標註Level
- 需要根據題目特點推測：
  - Challenge（場景題）→ 可能是Level 2或3的選擇題
  - Easy（基礎題）→ 可能是Level 1

### 發現3: 主要數據是Level II

- FinTrain-cfa_exercise和CFA_Extracted系列明確是Level II
- 這是我們數據的主要來源

---

## 📚 相關論文研究的Level

### 論文1: "Evaluating Large Language Models for Financial Reasoning: A CFA-Based Benchmark Study"
- **Level**: 未明確說明，但提到"CFA一至三級"
- 可能涵蓋所有Level

### 論文2: "Advanced Financial Reasoning at Scale: A Comprehensive Evaluation of Large Language Models on CFA Level III"
- **Level**: ✅ **明確是Level III**
- 測試多選題和**論述題（Essay）**
- 這是專門研究Level 3的論文

### 論文3: FinDAP (EMNLP 2025)
- **Level**: 根據數據集推測，主要是**Level II**
- FinTrain-cfa_exercise明確是Level II
- FinEval系列未明確，但可能包含Level 1和2

---

## 🎯 對我們研究的影響

### 數據集選擇建議

#### ✅ 有明確Level標註的數據集
1. **FinTrain-cfa_exercise** (Level II) - 推薦
2. **CFA_Extracted系列** (Level II) - 推薦

#### ⚠️ Level未明確的數據集
1. **FinEval-CFA-Challenge** - 可能是Level 2或3的選擇題
2. **FinEval-CFA-Easy** - 可能是Level 1

#### ❌ Level標註有誤導的數據集
1. **CFA_Level_III** - 名稱是Level III，但實際是選擇題，不是申論題

### 研究建議

1. **主要使用Level II數據**
   - FinTrain-cfa_exercise
   - CFA_Extracted系列
   - 這些有明確標註，可信度高

2. **Level 3申論題數據缺失**
   - 當前沒有真正的Level 3申論題數據
   - 如果要做Level 3研究，需要自行收集或生成

3. **在論文中明確說明**
   - 說明數據主要是Level II
   - 說明FinEval系列未明確標註Level
   - 說明CFA_Level_III實際是選擇題，不是申論題

---

## 📝 論文中的說明建議

### 關於Level分布的說明

```
Level分布說明：
1. 主要數據來源是Level II（FinTrain-cfa_exercise, CFA_Extracted系列）
2. FinEval系列未明確標註Level，根據題目特點推測：
   - CFA-Easy可能是Level 1的基礎題
   - CFA-Challenge可能是Level 2或3的選擇題部分
3. CFA_Level_III數據集雖然名稱是Level III，但實際內容是選擇題，
   可能是Level 3考試中的選擇題部分（Level 3有50%是選擇題），
   不是Level 3的申論題部分
4. 當前數據集中沒有真正的Level 3申論題數據
```

### 關於題目類型的說明

```
題目類型說明：
1. 所有數據集都是選擇題（A, B, C），沒有申論題
2. Level 3考試包含50%申論題，但當前數據集只包含選擇題部分
3. 如果要做Level 3申論題研究，需要補充申論題數據
```

---

## ✅ 總結

### Level分布
- **Level I**: 可能（FinEval-Easy推測）
- **Level II**: ✅ 明確（FinTrain-cfa_exercise, CFA_Extracted）
- **Level III**: ⚠️ 部分（CFA_Level_III是選擇題，非申論題）

### 題目類型
- **選擇題**: ✅ 所有數據集都是
- **申論題**: ❌ 沒有找到

### 數據質量
- **有明確Level標註**: FinTrain-cfa_exercise, CFA_Extracted系列
- **Level未明確**: FinEval系列
- **Level標註可能誤導**: CFA_Level_III（名稱是III，但實際是選擇題）

---

**最後更新**: 2025年1月  
**驗證方法**: 實際數據集樣本檢查

