# D1 金融 LLM 的信心校準與選擇性預測
# Calibration and Selective Prediction for Financial LLMs

## 研究問題

當一個 LLM 回答 CFA 題目時表示「我有 90% 的信心」，這個信心值是否可靠？在高風險的金融決策場景中，模型的 calibration（信心校準）至關重要——過度自信（overconfidence）可能導致錯誤的投資建議被採納，而過度保守則會降低系統的實用性。本研究系統性地評估多種 confidence estimation 方法在 CFA 考試場景下的校準品質，並探索 selective prediction（選擇性預測）的可行性：**模型能否可靠地「知道自己不知道什麼」？**

## 核心方法

四種 confidence estimation 方法的比較框架：

1. **Verbalized Confidence**：直接在 prompt 中要求模型自評信心分數（0-100%）
2. **Self-Consistency Variance**：對同一題目重複 sampling k=10 次（temperature > 0），計算答案分布的 agreement ratio 作為信心指標
3. **Ensemble Disagreement**：多個不同模型回答同一題目，以多數決的 agreement ratio 作為信心指標
4. **Logit-based Confidence**：透過 Ollama 的 logprobs API 取得 token-level 機率，計算答案選項的 probability mass

## 實驗設計

**實驗 1：Calibration Evaluation**
- 測試集：CFA-Challenge（90）+ CFA-Easy（1,032）+ CRA-Bigdata（1,472）
- 模型：gpt-4o-mini, qwen3:32b, llama3.1:8b, deepseek-r1:14b
- 每種模型 × 每種 confidence method 的組合
- 指標：Expected Calibration Error（ECE）、Maximum Calibration Error（MCE）、Brier Score
- 視覺化：Reliability Diagram（10 bins）

**實驗 2：Topic-level Calibration Analysis**
- 按 CFA 主題分組，計算各主題的 ECE
- 辨識 calibration 最差的主題（系統性 overconfidence 或 underconfidence）
- 分析：計算密集型主題（Quant, Fixed Income）vs 記憶密集型主題（Ethics, Regulation）的校準差異

**實驗 3：Confidence as Correctness Predictor**
- 計算 AUROC：以 confidence score 預測答案正確性
- 比較四種 confidence method 的 AUROC
- 哪種方法最能區分「模型會答對的題」與「模型會答錯的題」？

**實驗 4：Coverage-Accuracy Tradeoff**
- 設定不同信心閾值 θ，只回答 confidence ≥ θ 的題目
- 繪製 coverage（回答比例）vs accuracy（回答題目的準確率）曲線
- 分析：在何種 coverage 水準下，模型可達到接近人類 CFA 及格率的準確度？

## 需要的積木
- ✅ Ollama models（llama3.1:8b, qwen3:32b, deepseek-r1:14b） — 本地已安裝
- ✅ OpenAI API（gpt-4o-mini） — 已設定
- ✅ FinEval-CFA-Challenge / CFA-Easy / CRA-Bigdata — 已就緒
- ❌ Verbalized confidence prompt template — 需設計，預計 0.5 天
- ❌ Self-consistency sampling pipeline — 需實作 k=10 repeated sampling
- ❌ Logprobs extraction（Ollama API） — 需實作 API 呼叫與 probability 計算
- ❌ Calibration 統計分析工具 — ECE/MCE/Brier Score 計算 + Reliability Diagram 繪製

## 預期產出

- 四種 confidence estimation 方法在 CFA 場景的完整比較
- 各模型 × 各主題的 Reliability Diagram 集合
- Coverage-Accuracy tradeoff curve
- AUROC 排名：哪種信心估計方法最具預測力
- 「金融 LLM 信心校準」的最佳實踐建議

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | Hard test set | ✅ 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | ✅ 已就緒 |
| CRA-Bigdata (1,472) | Large-scale test set | ✅ 已就緒 |

## 模型需求

- **Cloud**: gpt-4o-mini（OpenAI）
- **Local**: qwen3:32b, llama3.1:8b, deepseek-r1:14b（Ollama，需 logprobs 支援）
- 無需 GPU 訓練，**純統計分析**，是所有點子中計算資源需求最低的

## 狀態

🟢 **最快產出的論文** — 無需 GPU 訓練，無需建構複雜系統，核心是統計分析。可與其他論文平行進行。預估 2-3 週完成實驗與初稿。

## 可合併的點子

- **D2**（Cross-Model Consensus）：D1 的 Ensemble Disagreement 方法就是 D2 的核心概念
- **D3**（Abstention Mechanism）：D1 的 coverage-accuracy curve 直接提供 D3 所需的 abstention threshold
- **D4**（Overconfident AI）：D1 辨識出的 "high confidence + wrong answer" cases 就是 D4 的分析對象
- **C3**（Parametric vs Retrieved）：D1 可在 with/without RAG 條件下分別做 calibration

## 來源筆記

- 本倉庫 `docs/03` 方向 2（LLM Calibration in Finance）
- Kadavath et al. (2022) "Language Models (Mostly) Know What They Know"
- Guo et al. (2017) "On Calibration of Modern Neural Networks"
- Geifman & El-Yaniv (2017) "Selective Prediction" — coverage-accuracy framework
