# H3 CFA Level III 申論題評估：從選擇題到建構式回答

## 研究問題

CFA Level III 的核心特色是**申論題 (Constructed Response / Essay Questions)**，佔考試約 50% 比重。考生需要：
- 撰寫完整的投資政策聲明 (Investment Policy Statement, IPS)
- 論述資產配置理由
- 計算並解釋退休規劃
- 評估倫理案例並撰寫分析

然而，現有所有 CFA + LLM 研究（包括 FinDAP、arXiv 2507.02954、本專案所有 A-G 系列）**都只評估選擇題 (MCQ)**。連 CFA_Level_III 資料集也只有 MCQ（文件明確記載「含 Level III MCQ，無申論」）。

這意味著我們對 LLM「能否通過 CFA Level III」的回答只有一半的證據。申論題測試的是更高層次的能力：整合判斷、書面溝通、結構化論述、個案分析——正是 G1 Ability Matrix 中「AI-Resistant」能力的核心。

### 核心假說

1. **LLM 在申論題上的表現遠低於 MCQ**：MCQ 有選項提示和消去法，申論題完全開放
2. **不同申論題類型的難度差異極大**：「計算+解釋」型 vs「純判斷」型 vs「IPS 撰寫」型
3. **評分一致性是核心挑戰**：LLM 生成的申論回答，人工評分和自動評分的一致性會是多少？

## 技術方法

### Phase 1：申論題基準建構

來源：
- CFA Institute 官方公開的 Past Exam Questions（Level III 過去 10 年的部分題目公開）
- SchweserNotes 的 Practice Essay Questions
- 自行設計的代表性申論題（參考 CFA Curriculum 結構）

題目分類（4 類）：
- **Type C (Calculate & Explain)**：「計算退休需求並解釋假設」
- **Type J (Justify)**：「選擇 A 或 B 策略並論述理由」
- **Type E (Evaluate)**：「評估此投資顧問是否違反倫理準則」
- **Type W (Write)**：「為此客戶撰寫 IPS」

### Phase 2：多維度評分框架

每道申論題用 5 個維度評分（each 1-5）：
1. **Technical Accuracy**：金融計算和概念是否正確
2. **Completeness**：是否涵蓋所有被問到的要點
3. **Reasoning Quality**：論證邏輯是否嚴謹
4. **Communication Clarity**：表達是否清晰、結構化
5. **Professional Judgment**：是否展現金融專業判斷力（vs 泛泛而談）

評分者：
- GPT-4o 自動評分（用 detailed rubric）
- 人工評分（2 位 CFA charterholder 或候選人）
- 計算 GPT-4o vs 人工的 Cohen's Kappa

### Phase 3：MCQ vs Essay 差距分析

選擇覆蓋相同知識點的 MCQ 和 Essay 題目配對，量測：
`essay_gap = acc_mcq - score_essay (normalized to 0-100)`

## 實驗設計

### 實驗 1：Essay 基線評估
- 50-80 道申論題 × 4-6 個模型
- 多維度評分框架
- 報告各維度和各題型的表現

### 實驗 2：MCQ vs Essay 配對比較
- 同主題的 MCQ 和 Essay 配對
- 量化 essay gap 在不同主題和認知層級上的分佈

### 實驗 3：自動評分可靠性
- GPT-4o 作為 essay 評分者的信效度
- 與人工評分的一致性（Cohen's Kappa）
- 哪些評分維度的自動化最可靠？哪些最不可靠？

### 實驗 4：提升策略
- CoT Prompting 對 essay 品質的影響
- Role-playing (CFA candidate / senior advisor) 對 essay 品質的影響
- RAG (提供相關教材) 對 essay 品質的影響

## 預期結果

1. LLM 在 Type C (計算+解釋) 表現最好（接近 MCQ 水準），Type W (IPS 撰寫) 表現最差
2. essay gap 在 Ethics 和 Portfolio Management 主題上最大
3. GPT-4o 自動評分在 Technical Accuracy 和 Completeness 上較可靠（Kappa > 0.7），但在 Professional Judgment 上較差（Kappa < 0.5）
4. Role-playing as senior advisor 在 essay 上的提升比 MCQ 上更顯著

## 新穎貢獻

1. **首個 CFA 申論題 LLM 評估**：填補現有研究最大的空白
2. **多維度申論題評分框架**：可推廣到其他專業考試（醫師、律師）
3. **自動評分信效度分析**：為 LLM-as-Judge 在專業教育的應用提供實證
4. **MCQ vs Essay 差距量化**：直接回答「MCQ 準確率能代表真實能力嗎？」

## 目標投稿場所

- ACL / EMNLP（NLG Evaluation track）
- AAAI（AI in Education）
- Assessment in Education: Principles, Policy & Practice
- Journal of Financial Education

## 依賴關係

- 與 G1 能力矩陣核心互補：Essay 題目測試的就是 G1 認為的「AI-Resistant」能力
- 與 A1 開放式數值推理互補：A1 去掉選項但仍是數值答案，H3 連答案格式都開放
- 與 F4 角色扮演互補：角色扮演對 essay 的影響可能比對 MCQ 更大
- 與 B7 CoT 忠實度互補：essay 的推理過程更可見，更適合忠實度分析
- 需要高品質的申論題目和評分基準（主要瓶頸）

## 時間與資源

- 基準建構：3-4 週（最花時間：設計題目和 rubric）
- 模型推論：1-2 週
- 人工評分：3-4 週（需要 CFA 背景的評分者）
- 分析撰寫：2 週
- 不需要 GPU 訓練
