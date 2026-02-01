# D4 過度自信的金融 AI：風險分析與監管啟示
# Overconfident AI in Finance: Risk Analysis and Regulatory Implications

## 研究問題

在所有 LLM 錯誤中，最危險的不是「不知道」，而是「高度自信地給出錯誤答案」。在金融場景中，這種 overconfident error 可能導致投資人接受錯誤的資產配置建議、基金經理人依據錯誤的風險評估做出決策、或合規人員忽略實際存在的監管風險。本研究聚焦於 **"high confidence + wrong answer" 案例的系統性分析**：哪些 CFA 主題最容易產生危險的過度自信？這對金融 AI 監管意味著什麼？

## 核心方法

從 D1 的 calibration 實驗結果中，篩選出 **overconfident errors**（confidence ≥ 80% 但答案錯誤的案例），進行多維度的系統性分析：

**分析維度**：
1. **Topic Distribution**：哪些 CFA 主題的 overconfident error rate 最高？
2. **Error Pattern Taxonomy**：overconfident errors 的類型分類（概念混淆、公式錯誤、數值提取失誤、推理邏輯錯誤）
3. **Risk Severity Assessment**：若這些錯誤發生在實際金融決策中，可能造成的後果嚴重程度
4. **Cross-Model Consistency**：同一題目是否讓多個模型都 overconfidently wrong？（集體幻覺）

**CFA Ethics 框架連結**：
- Standard I(C): Misrepresentation — AI 高信心但錯誤的回答是否構成 misrepresentation？
- Standard V(A): Diligence and Reasonable Basis — 依賴 overconfident AI 是否違反 due diligence？
- Standard III(C): Suitability — overconfident AI 推薦不適合的產品

## 實驗設計

**實驗 1：Overconfident Error Profiling**
- 從 D1 實驗數據中篩選：confidence ≥ 80% 且答案錯誤的所有案例
- 統計：overconfident error 佔所有錯誤的比例（across models）
- 繪製 overconfident error rate by CFA topic 的熱力圖

**實驗 2：Error Taxonomy Construction**
- 對所有 overconfident errors 進行人工分類
- 類別：Conceptual Confusion（概念混淆）、Formula Misapplication（公式誤用）、Numerical Extraction Error（數值提取錯誤）、Logical Reasoning Flaw（推理邏輯缺陷）、Outdated Knowledge（過時知識）
- 各類別的分布統計與代表性案例展示

**實驗 3：Collective Hallucination Detection**
- 辨識「所有模型都 overconfidently wrong」的題目
- 這些 collective hallucination cases 的共同特徵分析
- 這些案例是否可被任何現有方法（RAG, self-consistency）挽救？

**實驗 4：Risk Scenario Mapping**
- 將 overconfident errors 對應到實際金融場景
- 例：Fixed Income duration 計算錯誤 → 利率避險失敗 → 投資組合損失
- 例：Ethics 判斷錯誤 → 合規建議失誤 → 監管處罰
- 建構 "AI Risk Severity Matrix"（likelihood × impact）

**實驗 5：Regulatory Implications Analysis**
- 對照現有金融 AI 監管框架（EU AI Act, SEC AI guidance, MAS AI guidelines）
- 分析：CFA Ethics Standards 如何適用於 AI 系統？
- 提出：金融 AI 系統應具備的 minimum calibration requirements

## 需要的積木
- ✅ D1 的 calibration 實驗結果 — 需先完成 D1
- ✅ CFA Ethics 教材內容 — 作為分析框架
- ✅ FinEval 測試集（含題目主題分類） — 已就緒
- ❌ Overconfident error 篩選與分類 pipeline — 需實作
- ❌ Risk scenario mapping 模板 — 需設計金融情境對應
- ❌ 監管框架文獻整理 — 需研讀 EU AI Act, SEC guidance 相關條款

## 預期產出

- Overconfident error rate 的跨模型 × 跨主題全景分析
- Error Taxonomy：overconfident errors 的類型分類與分布
- Collective hallucination cases 的深度分析
- AI Risk Severity Matrix（金融場景風險對應）
- 監管建議：金融 AI 系統的 minimum calibration standards 提案
- **跨領域論文**：同時對 CS（NLP/AI）與 Finance/Policy 讀者有價值

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| D1 實驗結果 | Confidence scores + correctness labels | ❌ 需先完成 D1 |
| FinEval-CFA-Challenge (90) | Hard test set | ✅ 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | ✅ 已就緒 |
| CRA-Bigdata (1,472) | Large-scale test set | ✅ 已就緒 |

## 模型需求

- 直接使用 D1 收集的模型輸出，無需額外 inference
- 本研究的核心工作為**定性分析與政策論述**，非技術實驗

## 狀態

🟡 **依賴 D1，但獨特定位** — 技術部分依賴 D1 的實驗數據，但本研究的主要貢獻在於金融風險分析與監管啟示。適合投稿金融科技或 AI policy 相關場所。D1 完成後約 2-3 週可完成。

## 可合併的點子

- **D1**（Calibration）：D4 完全建立在 D1 的實驗數據之上
- **D3**（Abstention）：D3 的棄權機制是解決 D4 所揭示問題的技術方案
- **D2**（Cross-Model Consensus）：collective hallucination 分析需要 D2 的多模型數據
- **C2**（KG-RAG）：可分析 KG-RAG 是否能降低 overconfident error rate

## 來源筆記

- 新構想，為 D1 的政策導向衍生
- CFA Institute Code of Ethics and Standards of Professional Conduct
- EU AI Act (2024) — 高風險 AI 系統的要求
- Bommasani et al. (2021) "On the Opportunities and Risks of Foundation Models"
- 本倉庫 `docs/03` 方向 2 的延伸（從技術 calibration 到政策影響）
