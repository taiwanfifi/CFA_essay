# G1 CFA 能力 x AI 可複製性 x 鑑別力矩陣
# CFA Ability Matrix: Cognitive Skill Mapping, AI Replicability, and Signaling Value Retention

## 研究問題

CFA 認證測量了哪些認知能力？這些能力在多大程度上可被 AI 穩定地複製？當特定能力被 AI 低成本複製後，該能力作為 labor market signal 的鑑別力如何變化？本研究的目標不是測試任何單一模型，而是建構一個三層矩陣——CFA Level x Ability Type x AI Replicability Metrics——作為整個博士論文群的核心數據產品（central data product）。此矩陣由其他論文的實驗結果填充，G1 本身是一篇 aggregation paper，負責整合、解讀、並展示全景圖。

## 核心方法

矩陣的三層結構：

**Layer 1: CFA Level（考試層級）**
- Level 1：知識與基礎技能（Declarative + Procedural）
- Level 2：分析與應用（Analytical + Conditional Reasoning）
- Level 3：判斷、整合與責任（Integrative + Normative + Interpersonal）

**Layer 2: Ability Type（能力類型，6 大類）**
- Declarative Knowledge（陳述性知識）：定義、術語、規則
- Procedural / Algorithmic Skill（程序與計算技能）：公式套用、數值計算
- Analytical Decomposition（分析拆解）：多步驟推理、條件比較
- Integrative Judgment（整合判斷）：跨主題、模糊條件下的決策
- Normative / Ethical Reasoning（規範與倫理推理）：道德灰色地帶、受託責任
- Interpersonal / Stakeholder Reasoning（人際與利害關係推理）：客戶目標平衡、溝通說服

**Layer 3: AI Replicability Metrics（由其他論文實驗填入）**
- AI Performance Level：該能力上 AI 的整體表現水準
- Cross-model Stability：不同模型間的表現一致性（來自 E1 Error Pattern Atlas 的跨模型分析）
- Prompt Sensitivity：對 prompt 變化的敏感度（來自 B7 CoT Faithfulness 等實驗）
- Signaling Value Retention：綜合判斷——該能力的證照鑑別力是否保留

## 實驗設計

本研究自身不執行新實驗，而是進行 meta-aggregation：

1. **能力標註階段**：對全部 CFA 題目（CFA-Challenge 90 + CFA-Easy 1,032 + CFA_Extracted 1,124）進行 Ability Type 標註。使用 GPT-4o 自動分類，在 100 題人工標註樣本上計算 Cohen's Kappa 驗證可靠性。此標註可復用 G4 Cognitive Demand Taxonomy 的結果。
2. **數據匯入階段**：從其他已完成論文中提取每個 Ability Type 的 AI Performance、Cross-model Stability、Prompt Sensitivity 指標，填入矩陣 Layer 3。
3. **矩陣分析階段**：計算每個 cell 的 Signaling Value Retention score，繪製完整矩陣的 heat map，識別「高 AI 表現 + 高穩定性 = 低鑑別力」與「低 AI 表現 + 高不穩定性 = 高鑑別力」的能力群。
4. **趨勢預測**：基於模型規模 scaling 趨勢，推估未來 1-3 年各能力的 AI Replicability 變化方向。

## 需要的積木
- ✅ CFA 題庫 — CFA-Challenge (90), CFA-Easy (1,032), CFA_Extracted (1,124), CRA-Bigdata (1,472)
- ✅ Ability Type 分類框架 — 6 大類已定義
- ❌ 題目能力標註 — 需對全部題目進行 Ability Type 標註（可復用 G4 產出）
- ❌ 其他論文的實驗結果 — 需等待 B1, B7, E1 等論文完成後匯入數據
- ❌ Meta-aggregation 管道 — 需開發數據匯整與矩陣視覺化程式

## 預期產出
- CFA Ability Matrix：首個將專業認證題目系統性映射為人力資本能力並量化 AI 可複製性的矩陣
- 矩陣 heat map（核心圖表）：一張圖展示整個 PhD 的發現
- Signaling Value Retention 排序：哪些能力的證照鑑別力最先崩解、哪些最具韌性
- 為 G2（Signaling Theory）與 G3（AI-Resistant Assessment）提供實證基礎

## 資料需求
| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | 高難度題能力標註 | 已就緒 |
| FinEval-CFA-Easy (1,032) | 主體題能力標註 | 已就緒 |
| CFA_Extracted (1,124) | 含 material/scenario 輔助標註 | 已就緒 |
| CRA-Bigdata (1,472) | 擴大分析範圍 | 已就緒 |
| 其他論文實驗結果 | 填入 Layer 3 指標 | 需等待 |

## 模型需求
- GPT-4o（API）：用於自動能力標註
- 本研究不直接執行模型推論——所有 AI performance 數據來自其他論文

## 狀態
最後撰寫 — 本論文依賴其他所有論文的實驗結果，是整個 PhD 的彙整論文。能力標註框架可先行建立，但矩陣 Layer 3 需等待其他論文完成。

## 可合併的點子
- **G4 (Cognitive Demand Taxonomy)** — G4 的題目分類是 G1 能力標註的直接輸入
- **G2 (Signaling Theory)** — G1 的矩陣是 G2 理論分析的實證基礎
- **G3 (AI-Resistant Assessment)** — G1 的 Signaling Value Retention 直接導出 G3 的政策建議
- **E1 (Error Pattern Atlas)** — E1 的跨模型分析提供 Cross-model Stability 數據
- **B7 (CoT Faithfulness)** — B7 的結果影響 Prompt Sensitivity 指標

## 來源筆記
- drafts/archive/old-1-signaling-framework.md — 矩陣三層結構的完整設計（Step 1-6）
- docs/03-研究方向深度設計.md — 七個研究方向的技術依賴圖，G1 位於匯整層
- Spence (1973) signaling model、Becker (1964) human capital theory、Autor et al. (2003) task-based automation framework
