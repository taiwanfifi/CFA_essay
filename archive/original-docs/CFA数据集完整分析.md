# CFA数据集完整深度分析

## 📊 执行摘要

经过深入分析13个CFA相关数据集，发现：
- **所有数据集都不是CFA Institute官方真题**
- **有论文背书的**: FinEval、FinTrain、CFA_Extracted系列 (EMNLP 2025 FinDAP)
- **Level分布**: 主要是Level II (2020年SchweserNotes材料)
- **数据量差异巨大**: 从90样本到147万样本
- ⚠️ **重要发现**: 
  - **flare-cfa** 与 **FinEval-CFA-Easy** 几乎完全相同（可能是重复发布）
  - **CFA_Judgement** 不是CFA题目，而是香港法律判决案例（1997-2022）
  - 两者都**没有论文背书**

---

## 一、数据集详细分析表

| 数据集 | 样本数 | Level | 年份 | 来源类型 | 论文背书 | 真实性 | 推荐度 |
|--------|--------|-------|------|----------|----------|--------|--------|
| **FinEval-CFA-Challenge** | 90 | 未明确 | 2020 | 模拟题/样本题 | ✅ EMNLP 2025 | 非官方真题 | ⭐⭐⭐⭐⭐ |
| **FinEval-CFA-Easy** | 1,032 | 未明确 | - | 模拟题/样本题 | ✅ EMNLP 2025 | 非官方真题 | ⭐⭐⭐⭐⭐ |
| **FinEval-CRA-Bigdata** | 1,472 | 未明确 | - | 大数据任务 | ✅ EMNLP 2025 | 非官方真题 | ⭐⭐⭐⭐ |
| **flare-cfa** | 1,032 | 未明确 | - | 第三方数据集 | ❌ **无论文** | ⚠️ **与FinEval-Easy重复** | ⭐⭐ |
| **CFA_Level_III** | 90 | Level III | 2020 | 2020 Mock PM | ❌ 无论文 | 模拟题 | ⭐⭐ |
| **CFA_Extracted-chunk_0** | 1,124 | **Level II** | **2020** | SchweserNotes | ✅ EMNLP 2025 | 备考材料 | ⭐⭐⭐⭐⭐ |
| **CFA_Extracted-sft** | 2,946 | **Level II** | **2020** | SchweserNotes | ✅ EMNLP 2025 | 备考材料 | ⭐⭐⭐⭐⭐ |
| **FinTrain-cfa_exercise** | 2,946 | **Level II** | **2020** | SchweserNotes | ✅ EMNLP 2025 | 备考材料 | ⭐⭐⭐⭐⭐ |
| **FinTrain-apex_instruct** | 1,472,062 | 未明确 | - | 通用指令数据 | ✅ EMNLP 2025 | 混合来源 | ⭐⭐⭐⭐ |
| **FinTrain-book_fineweb** | 4,500 | 未明确 | - | 书籍网页 | ✅ EMNLP 2025 | 无监督文本 | ⭐⭐⭐ |
| **CFA_Judgement** | 11,099 | 未明确 | **1997-2022** | 判断题库 | ❌ **无论文** | ❌ **非CFA题目（法律案例）** | ⭐ |
| **CFA_Rule** | 1,125 | 未明确 | - | 规则文本 | ❓ 需查证 | 无监督 | ⭐⭐ |
| **CFA_Knowledgeable** | 564 | 未明确 | - | 知识问答 | ❓ 需查证 | 无监督 | ⭐⭐ |

---

## 二、关键发现

### 1. 📚 论文背书情况

#### ✅ 有论文背书 (EMNLP 2025 FinDAP论文)
- **FinEval系列**: Salesforce官方评估框架
  - 论文: "Demystifying Domain-adaptive Post-training for Financial LLMs" (EMNLP 2025)
  - 作者: Zixuan Ke, Yifei Ming, Xuan-Phi Nguyen, Caiming Xiong, Shafiq Joty
  - arXiv: 2501.04961
  
- **FinTrain系列**: Salesforce官方训练数据
  - 与FinEval同一论文支持
  
- **CFA_Extracted系列**: Zixuan Ke (论文第一作者)发布
  - 与FinDAP论文相关

#### ❌ 无论文背书
- **CFA_Level_III** (alvinming个人发布)
- **CFA_Rule** (ZixuanKe个人发布，但可能是论文数据的一部分)
- **CFA_Knowledgeable** (ZixuanKe个人发布)

#### ❓ 需查证
- **flare-cfa** (TheFinAI发布，需查证是否有论文)
- **CFA_Judgement** (xxuan-nlp发布，需查证)

### 2. 🎯 Level分布分析

#### 明确标注Level II
- **CFA_Extracted系列**: "CFA 2020 Level II - SchweserNotes Book 4.txt"
- **FinTrain-cfa_exercise**: 同样来自Level II材料

#### 名称暗示Level III
- **CFA_Level_III**: 名称暗示，但需验证内容

#### 未明确标注
- **FinEval系列**: 未在样本中发现Level信息
- **flare-cfa**: 未发现Level信息
- **其他数据集**: 未发现Level信息

### 3. 📅 年份信息

- **2020年**: 
  - CFA_Extracted系列 (Level II)
  - FinTrain-cfa_exercise (Level II)
  - CFA_Level_III (2020 Mock PM)
  - FinEval-Challenge (部分2020 Mock PM)

- **1997-2022**: 
  - CFA_Judgement (覆盖25年)

- **未明确**: 其他大部分数据集

### 4. 🔍 题目真实性分析

#### ❌ 重要发现：所有数据集都不是官方真题

1. **SchweserNotes来源** (非官方)
   - CFA_Extracted系列
   - FinTrain-cfa_exercise
   - 说明: SchweserNotes是第三方CFA备考材料，题目风格接近但非官方真题

2. **模拟题/样本题** (非官方)
   - FinEval-Challenge: "2020 Mock PM" (模拟考试)
   - FinEval-Easy: 样本题格式
   - CFA_Level_III: "sample_test"来源

3. **第三方数据集** (需验证)
   - flare-cfa: 来源不明确

4. **提取/生成数据** (非官方)
   - CFA_Judgement: 从材料中提取的双语语料
   - CFA_Rule/Knowledgeable: 无监督文本

### 5. 📊 数据量对比

| 规模 | 数据集 | 样本数 |
|------|--------|--------|
| **超大** | FinTrain-apex_instruct | 1,472,062 |
| **大** | CFA_Judgement | 11,099 |
| **中** | FinTrain-cfa_exercise, CFA_Extracted-sft | 2,946 |
| **小** | CFA_Extracted-chunk_0 | 1,124 |
| **很小** | FinEval-Challenge, CFA_Level_III | 90 |

---

## 三、LLM评估/训练建议

### 🎯 评估数据集选择

#### 推荐方案1: FinEval系列 (⭐⭐⭐⭐⭐)
**优势**:
- ✅ 有EMNLP 2025论文背书
- ✅ Salesforce官方评估框架
- ✅ 包含不同难度(Challenge/Easy)
- ✅ 格式规范，易于使用
- ✅ 与FinTrain训练数据配套

**劣势**:
- ⚠️ 样本量较小(Challenge仅90题)
- ⚠️ 非官方真题

**使用场景**: 
- 学术研究论文
- 模型性能评估
- 与其他模型对比

#### 备选方案: flare-cfa (⭐⭐⭐)
**优势**:
- ✅ 样本量较大(1032)
- ✅ 格式规范

**劣势**:
- ⚠️ 需查证来源和论文
- ⚠️ 未明确Level信息

### 🏋️ 训练数据集选择

#### 推荐方案1: FinTrain-cfa_exercise (⭐⭐⭐⭐⭐)
**优势**:
- ✅ 有论文背书
- ✅ 样本量适中(2946)
- ✅ 明确Level II
- ✅ 来自SchweserNotes (接近真实考试风格)
- ✅ 与FinEval评估配套

**使用场景**: 
- 领域特定微调
- 与FinEval评估配套使用

#### 推荐方案2: CFA_Extracted系列 (⭐⭐⭐⭐⭐)
**优势**:
- ✅ 有论文背书
- ✅ GPT-4验证
- ✅ 包含材料上下文(chunk_0)
- ✅ 明确Level II

**使用场景**:
- 需要上下文信息的训练
- RAG相关研究

#### 备选方案: CFA_Judgement (⭐⭐⭐)
**优势**:
- ✅ 覆盖25年(1997-2022)
- ✅ 样本量大(11099)
- ✅ 双语数据

**劣势**:
- ⚠️ 需查证论文
- ⚠️ 是判断题库，非选择题

### 📈 完整训练流程建议

```
阶段1: 预训练/知识注入
├── FinTrain-book_fineweb (无监督，4500样本)
├── CFA_Rule (无监督，1125样本)
└── CFA_Knowledgeable (无监督，564样本)

阶段2: 领域微调
├── FinTrain-apex_instruct (指令微调，147万样本) [可选，通用能力]
├── FinTrain-cfa_exercise (CFA特定，2946样本) [推荐]
└── CFA_Extracted系列 (QA对，1124-2946样本) [推荐]

阶段3: 评估
├── FinEval-CFA-Challenge (挑战级，90题) [主要评估]
├── FinEval-CFA-Easy (简单级，1032题) [辅助评估]
└── flare-cfa (交叉验证，1032题) [可选]
```

---

## 四、重要注意事项

### ⚠️ 1. 题目真实性
- **所有数据集都不是CFA Institute官方发布的真实考试题目**
- 但可以用于评估LLM的金融知识能力
- 建议在论文中明确说明数据来源

### ⚠️ 2. Level信息不完整
- 大部分数据集未明确标注Level
- 只有CFA_Extracted和FinTrain-cfa_exercise明确标注Level II
- 建议手动检查或标注Level信息

### ⚠️ 3. 年份集中
- 大部分数据来自2020年
- 可能无法反映最新考试趋势
- CFA_Judgement覆盖1997-2022，但主要是判断题库

### ⚠️ 4. 数据来源
- **SchweserNotes**: 第三方备考材料，非官方但质量较高
- **Mock PM**: 模拟考试，接近真实但非官方
- **样本题**: 可能是官方样本题或练习题

### ⚠️ 5. 论文引用
- 使用FinEval/FinTrain时，需引用EMNLP 2025 FinDAP论文
- 其他数据集需查证是否有论文支持

---

## 五、研究建议

### 对于学术论文研究

1. **主要评估数据集**: FinEval系列
   - 有论文背书
   - 格式规范
   - 易于复现

2. **主要训练数据集**: FinTrain-cfa_exercise + CFA_Extracted
   - 与评估数据配套
   - 有论文支持

3. **在论文中明确说明**:
   - 数据来源(非官方真题)
   - Level信息(主要是Level II)
   - 年份信息(主要是2020)

### 对于模型开发

1. **组合使用**: FinEval评估 + FinTrain训练
2. **数据增强**: 可结合多个数据集
3. **验证**: 使用flare-cfa进行交叉验证

---

## 六、总结

### ✅ 推荐数据集组合

**评估**: FinEval-CFA-Challenge + FinEval-CFA-Easy
**训练**: FinTrain-cfa_exercise + CFA_Extracted-sft
**验证**: flare-cfa (可选)

### 📝 关键结论

1. **有论文背书的数据集**: FinEval、FinTrain、CFA_Extracted系列
2. **Level信息**: 主要是Level II (2020年SchweserNotes)
3. **真实性**: 所有数据集都不是官方真题，但可用于评估LLM能力
4. **数据量**: 差异巨大，需根据需求选择
5. **推荐度**: FinEval系列和FinTrain系列最值得使用

---

**最后更新**: 2025年1月
**分析基于**: 实际数据集样本检查 + 网络搜索 + 论文信息

