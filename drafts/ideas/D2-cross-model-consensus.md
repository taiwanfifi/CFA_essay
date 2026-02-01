# D2 跨模型共識作為信心信號
# Cross-Model Consensus as Confidence Signal for Financial QA

## 研究問題

單一 LLM 的自我信心評估（self-reported confidence）往往不可靠，特別是在金融等需要精確知識的領域。本研究提出一個直覺但尚未被系統驗證的假設：**多個異質模型對同一題目的一致性程度（consensus），是否比任何單一模型的自我信心更能預測答案的正確性？** 如果跨模型共識是更強的 correctness predictor，那麼在金融 AI 部署中，「多模型投票」可能比「信賴單一模型的自信」更為可靠。

## 核心方法

建構一個 multi-model ensemble framework，對每道 CFA 題目收集多個模型的答案，計算以下信心指標：

**Individual Confidence Signals**：
- Verbalized confidence（模型自評 0-100%）
- Self-consistency（同一模型 k=5 次 sampling 的 agreement）

**Ensemble Confidence Signals**：
- **Majority Agreement Ratio**：N 個模型中選擇多數答案的比例
- **Weighted Consensus**：以各模型在 validation set 上的歷史準確率加權
- **Disagreement Entropy**：答案分布的 Shannon entropy（低 entropy = 高共識）

核心比較：Individual signals vs Ensemble signals，哪類更能預測 correctness？

## 實驗設計

**實驗 1：Consensus Collection**
- 使用所有可用模型回答 CFA-Challenge（90 題）+ CFA-Easy（1,032 題）
- 模型池：gpt-4o-mini, qwen3:32b, qwen3:30b-a3b, qwen3:4b, deepseek-r1:14b, llama3.1:8b, gemma3, phi3.5:3.8b
- 共 8 個模型 × 1,122 題 = ~8,976 inference runs

**實驗 2：Consensus vs Individual Confidence**
- AUROC 比較：Majority Agreement Ratio vs Verbalized Confidence vs Self-Consistency
- 分別在各模型上計算：以 ensemble consensus 預測該模型答案正確性的 AUROC
- Calibration 比較：哪種信號的 ECE 更低？

**實驗 3：Ensemble Size Sensitivity**
- 從 2 個模型到 8 個模型，逐步增加 ensemble size
- 觀察 consensus signal 的 AUROC 如何隨 ensemble size 變化
- 確定 diminishing returns 的拐點：幾個模型就「夠了」？

**實驗 4：Model Diversity Analysis**
- 同家族模型（如 qwen3 系列）的共識 vs 異家族模型的共識
- 模型大小的影響：大模型之間的共識 vs 大小混合模型的共識
- 辨識最具互補性的模型組合

**實驗 5：Disagreement Case Study**
- 深入分析模型嚴重分歧的題目（entropy 最高的 top-20 題）
- 這些題目是否有共同特徵（某些 CFA 主題、某種題型、模糊的選項）？
- 人類專家判斷：模型分歧是否反映了題目本身的歧義？

## 需要的積木
- ✅ Ollama models（8 個模型） — 本地已安裝
- ✅ OpenAI API（gpt-4o-mini） — 已設定
- ✅ FinEval 測試集 — 已就緒
- ❌ Multi-model evaluation harness — 需實作統一的多模型批次推理框架
- ❌ Consensus metrics 計算模組 — Agreement ratio, weighted consensus, entropy
- ❌ AUROC / ECE 比較分析 pipeline — 需實作統計檢定

## 預期產出

- 跨模型共識 vs 個體信心的 AUROC 比較表
- Ensemble size vs prediction quality 的 scaling curve
- 最佳模型組合建議（互補性最強的 subset）
- 高分歧題目的定性分析報告
- 論證：multi-model consensus 在金融 QA 中是否為 superior confidence signal

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | Hard test set | ✅ 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | ✅ 已就緒 |

## 模型需求

- **Cloud**: gpt-4o-mini（OpenAI）
- **Local**: llama3.2, llama3.1:8b, qwen3:4b, qwen3:30b-a3b, qwen3:32b, deepseek-r1:14b, gemma3, phi3.5:3.8b（全部 Ollama）
- 無需 GPU 訓練，但需要大量 inference runs（~8,976 次）

## 狀態

🟡 **中等難度** — 實驗邏輯直觀，但需要大量推理時間（8 模型 × 1,122 題）。本地較大模型（qwen3:32b）的推理速度將是瓶頸。預估 3-4 週。

## 可合併的點子

- **D1**（Calibration）：D2 的 ensemble confidence 可作為 D1 的第三類 confidence method
- **D3**（Abstention）：使用 ensemble consensus 作為 abstention 的判斷依據
- **D4**（Overconfident AI）：高共識但錯誤的案例 = 集體過度自信，更具風險

## 來源筆記

- 新構想，受 ensemble methods 與 "wisdom of crowds" 啟發
- Wang et al. (2023) "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
- Lakshminarayanan et al. (2017) "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"
