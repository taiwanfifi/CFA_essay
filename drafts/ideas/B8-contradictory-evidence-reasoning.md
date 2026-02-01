# B8 矛盾證據下的金融推理：LLM 如何處理衝突信號

## 研究問題

真實的金融分析幾乎永遠面對矛盾信號：
- 基本面說「買入」但技術面說「賣出」
- P/E 偏低但 ROE 也偏低
- 總經指標正面但產業前景負面
- 公司財報良好但公司治理有疑慮

CFA 考試（尤其 Level II 和 III）會刻意設計包含矛盾線索的題目，測試考生的綜合判斷能力。然而，現有 LLM 研究從未系統性測試模型面對矛盾證據時的推理行為。

### 核心假說

1. **LLM 傾向過度依賴最顯著的單一信號**，忽略矛盾證據（anchoring bias）
2. **不同模型對矛盾的處理策略不同**：大模型可能嘗試整合，小模型可能忽略矛盾
3. **矛盾證據的呈現順序影響結果**（primacy / recency effect）
4. **CoT 在矛盾場景下可能反而有害**：迫使模型提前「選邊站」

## 技術方法

### Phase 1：矛盾證據題庫建構

三種矛盾類型：
- **Type V (Value Conflict)**：不同估值指標指向不同方向
  - 例：「P/E = 8（便宜）但 P/B = 0.5（可能有資產減損問題）」
- **Type S (Signal Conflict)**：不同分析框架結論不同
  - 例：「DCF 估值 $50 但 comparable company 估值 $35」
- **Type T (Temporal Conflict)**：短期和長期信號矛盾
  - 例：「短期技術面超買但長期基本面看好」

每道矛盾題附有：
- 正確答案（CFA 參考答案，通常要求考生「acknowledge both sides and explain weighting」）
- 矛盾強度標註（mild / moderate / severe）
- 預期正確的權衡邏輯

### Phase 2：矛盾處理策略分類

分析模型的回答，分類其矛盾處理策略：
- **Ignore**：完全忽略矛盾信號之一
- **Acknowledge-but-dismiss**：提到矛盾但輕描淡寫
- **Weight-and-integrate**：明確權衡兩方並做出有理由的判斷（最佳）
- **Paralysis**：列出矛盾但無法做出判斷
- **Confabulate**：編造不存在的論點來消解矛盾

### Phase 3：順序效應與提示策略實驗

- 矛盾信號的呈現順序（正面先 vs 負面先）
- 明確提示「請注意可能的矛盾信號」vs 不提示
- CoT vs Zero-shot 在矛盾場景的比較

## 實驗設計

### 實驗 1：矛盾處理基線
- 60-80 道矛盾證據題 × 6-8 個模型
- 分析矛盾處理策略分佈
- 與非矛盾對照題的準確率比較

### 實驗 2：矛盾強度效應
- Mild / Moderate / Severe 三級矛盾強度
- 預期：矛盾強度增加，準確率下降，但大模型的衰退幅度較小

### 實驗 3：順序效應
- 相同題目，矛盾信號順序互換
- 量化 primacy / recency effect 的強度

### 實驗 4：提示策略
- Baseline (zero-shot) vs CoT vs "Be aware of potential conflicts" prompt vs "List all evidence before making judgment" prompt
- 預期："List all evidence first" 策略最有效

## 預期結果

1. 小模型 (< 10B) 70%+ 使用 Ignore 策略；大模型 40-50% 使用 Weight-and-integrate
2. 矛盾題的準確率比非矛盾題低 15-25%
3. 顯著的順序效應（翻轉率 10-20%）
4. CoT 在矛盾場景下的提升幅度 < 非矛盾場景（可能甚至有害）

## 新穎貢獻

1. **首個金融矛盾推理基準**：填補 LLM 評估中的重要空白
2. **矛盾處理策略分類法**：5 種策略的系統性分類
3. **順序效應的量化**：連結到行為金融學的 anchoring bias 和 framing effect
4. **對 RAG 系統的啟示**：當 RAG 檢索到矛盾的知識片段時，系統應如何處理？

## 目標投稿場所

- ACL / EMNLP（Reasoning Track）
- AAAI（Cognitive Science + AI）
- Journal of Behavioral Finance（跨領域）

## 依賴關係

- 與 B1 五階段管道互補：矛盾處理發生在 Stage 5（合理性驗證）
- 與 E1 錯誤圖譜互補：「矛盾忽略」是一種新的錯誤類型
- 與 D1 校準互補：矛盾題上的過度自信是否更嚴重？
- 與 G4 認知需求互補：矛盾題通常為 Level 4-5
- 不需要 GPU 訓練

## 時間與資源

- 題庫建構：2-3 週（需要金融背景）
- 實驗執行：2 週
- 分析撰寫：2 週
