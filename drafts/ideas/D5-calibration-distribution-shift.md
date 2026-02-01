# D5 分佈偏移下的信心校準穩定性

## 研究問題

D1 在特定題目分佈上測量校準，但真實部署時，題目分佈會改變：
- CFA 考試每年更新題庫，主題權重調整
- 不同客戶的問題分佈不同（零售 vs 機構、股票 vs 固收為主）
- 市場環境變化帶來新類型的問題

**核心問題**：模型在分佈 A 上的校準品質，能推廣到分佈 B 嗎？如果不能，「我們測出的 ECE 分數」對真實部署有多少參考價值？

這是一個對金融 AI 部署**至關重要但完全未被研究**的問題。EU AI Act 要求高風險 AI 系統的可靠性，但如果校準在分佈偏移下不穩定，那麼靜態的校準測試就不足以保證部署安全。

### 核心假說

1. **校準在同質偏移（量的變化）下相對穩定**：改變主題比例但不改變主題本身
2. **校準在異質偏移（質的變化）下嚴重衰退**：引入訓練分佈外的新主題或新難度
3. **Verbalized confidence 在偏移下最不穩定**，Self-Consistency 最穩定
4. **大模型的校準穩定性 > 小模型**

## 技術方法

### Phase 1：偏移類型定義

設計 5 種分佈偏移場景：
- **Shift 1 — Topic Reweight**：改變 CFA 主題的比例（如從均勻分佈變成 Fixed Income 佔 50%）
- **Shift 2 — Difficulty Shift**：只用 CFA-Challenge（難題）vs 只用 CFA-Easy（簡單題）
- **Shift 3 — Level Shift**：Level I 題 → Level II/III 題
- **Shift 4 — Format Shift**：MCQ → 開放式數值（用 A1 的 benchmark）
- **Shift 5 — Novel Topic**：加入 CRA-Bigdata 的股價預測題（非傳統 CFA 題型）

### Phase 2：校準穩定性量測

在每種偏移場景下重新計算 D1 的所有校準指標：
- ECE, MCE, Brier Score
- AUROC（信心預測正確性的能力）
- Coverage-Accuracy 曲線

核心指標：`calibration_stability = 1 - |ECE_shifted - ECE_original| / ECE_original`

### Phase 3：穩健校準策略

測試哪些校準方法在偏移下最穩健：
- Verbalized confidence
- Self-consistency
- Logit-based
- Ensemble consensus (D2)
- Temperature scaling (post-hoc calibration)
- Platt scaling with held-out validation

## 實驗設計

### 實驗 1：偏移基線
- 在原始分佈上測量 ECE（D1 的結果）
- 在 5 種偏移場景下重新測量 ECE
- 4 個模型 × 5 種偏移 × 4 種校準方法 = 80 組實驗

### 實驗 2：偏移嚴重度梯度
- 對 Shift 1（Topic Reweight）做連續梯度偏移
- 從原始分佈逐步偏移到極端分佈
- 繪製 ECE vs 偏移強度曲線

### 實驗 3：Post-hoc 校準的遷移性
- 在分佈 A 上擬合 temperature scaling 參數
- 在分佈 B 上測試是否仍有效
- 結論：post-hoc 校準是否需要對每個部署場景重新擬合？

### 實驗 4：最穩健的信心估計策略
- 在所有偏移場景中，哪種信心估計方法的校準穩定性最高？
- 預期排名：Self-Consistency > Ensemble > Logit > Verbalized

## 預期結果

1. Shift 1（Topic Reweight）對校準影響最小（ECE 變化 < 0.02）
2. Shift 4（Format Shift）和 Shift 5（Novel Topic）對校準影響最大（ECE 變化 > 0.08）
3. Verbalized confidence 在所有偏移場景下最不穩定
4. Self-Consistency 是最穩健的信心估計方法
5. Post-hoc 校準（temperature scaling）在同質偏移下遷移良好，異質偏移下需要重新擬合

## 新穎貢獻

1. **首個金融 LLM 校準穩定性研究**：填補「靜態校準 vs 動態部署」的差距
2. **5 種分佈偏移的系統性分類**：為未來研究提供標準化的偏移場景
3. **穩健校準策略推薦**：哪種信心估計方法最適合需要分佈穩健性的金融部署
4. **對金融 AI 監管的直接啟示**：靜態校準測試是否足夠？需要怎樣的持續監控？

## 目標投稿場所

- NeurIPS / ICML（Robustness / Uncertainty track）
- ACL（Evaluation track）
- Journal of Financial Regulation and Compliance

## 依賴關係

- **硬依賴 D1**：需要 D1 的基準校準結果
- 與 D4 互補：偏移下的過度自信風險是否更嚴重？
- 與 A1 互補：Format Shift 使用 A1 的開放式基準
- 與 H2 互補：時效性衰退可以視為一種特殊的分佈偏移
- 不需要 GPU 訓練

## 時間與資源

- 偏移場景建構：1 週
- 實驗執行：2-3 週（大量推論）
- 分析撰寫：2 週
- 建議在 D1 完成後啟動
