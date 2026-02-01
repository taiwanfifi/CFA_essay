# F2 CFA 表現的 Scaling Law：模型規模與金融推理能力的關係
# CFA Performance Scaling Law: Model Size vs Financial Reasoning Ability

## 研究問題

Scaling law 是 LLM 研究的核心議題之一：模型參數量的增長是否帶來可預測的能力提升？Kaplan et al. (2020) 與 Hoffmann et al. (2022, Chinchilla) 在通用 benchmark 上建立了 power-law 關係，但金融推理領域是否遵循相同的 scaling 行為仍未被系統性研究。本研究利用本地 Ollama 可用的完整模型規模梯度（3.8B 到 32B）加上 OpenAI API 模型，繪製首條 CFA 考試的 scaling curve，並分析：(1) 金融推理的 scaling 是平滑的還是存在 phase transition？(2) 不同 CFA 主題是否展現不同的 scaling 行為？(3) CFA scaling curve 與通用 benchmark（MMLU 等）的 scaling curve 有何差異？

## 核心方法

建構一條完整的 model size vs CFA accuracy 曲線。利用可用模型形成的規模梯度：

- phi3.5:3.8b (3.8B) — 微軟小模型
- qwen3:4b (4B) — 阿里通義小模型
- llama3.1:8b (8B) — Meta 標準模型
- deepseek-r1:14b (14B) — DeepSeek CoT specialist
- qwen3:30b-a3b (30B MoE, active 3B) — MoE 架構特例
- qwen3:32b (32B) — 阿里通義大模型
- gpt-4o-mini (estimated medium) — OpenAI 中階模型
- gpt-4o (estimated large) — OpenAI 旗艦模型

對每個模型在三個 CFA 測試集上執行 zero-shot inference，統一 prompt template 與 temperature=0。對 MoE 模型（qwen3:30b-a3b）特別標記，分析其 total params vs active params 在 scaling curve 上的位置差異。

## 實驗設計

1. **統一推論**：所有模型使用相同的 zero-shot MCQ prompt，在 CFA-Challenge (90)、CFA-Easy (1,032)、CRA-Bigdata (1,472) 上完成推論
2. **Overall Scaling Curve**：以 log(params) 為 x 軸、accuracy 為 y 軸，繪製散點圖並擬合 power-law / sigmoid / piecewise-linear 模型
3. **Topic-level Scaling**：對 CFA 10 大主題分別繪製 scaling curve，觀察是否存在主題間的 scaling 差異（hypothesis: Quantitative Methods 可能 scale 更陡，Ethics 可能 plateau 更早）
4. **Phase Transition 檢測**：使用 changepoint detection 方法（如 Bayesian changepoint analysis）測試是否存在突變點——即某個模型規模後準確率突然躍升
5. **MoE 分析**：qwen3:30b-a3b 有 30B total / 3B active params，分析其表現是更接近 3B 模型還是 30B 模型，揭示 MoE 在金融推理上的效率
6. **Cross-benchmark 比較**：收集相同模型在 MMLU、MMLU-Pro 等通用 benchmark 的公開分數，與 CFA scaling curve 疊合比較
7. **Difficulty Stratification**：CFA-Challenge (hard) vs CFA-Easy (standard) 的 scaling 行為可能不同——hard 題目可能需要更大模型才能看到改善

## 需要的積木
- ✅ FinEval-CFA-Challenge (90 題) — 已下載
- ✅ FinEval-CFA-Easy (1,032 題) — 已下載
- ✅ CRA-Bigdata (1,472 題) — 已下載
- ✅ Ollama local models — 完整規模梯度已安裝（phi3.5 到 qwen3:32b）
- ✅ OpenAI API — gpt-4o, gpt-4o-mini 可用
- ❌ Batch inference pipeline — 需建構統一的多模型批次推論與結果收集腳本
- ❌ Scaling curve fitting toolkit — 需實作 power-law / sigmoid / changepoint 擬合工具
- ❌ 通用 benchmark 公開分數收集 — 需從論文與 leaderboard 收集 MMLU 等分數

## 預期產出
- `results/F2_scaling_raw_data.csv` — 所有模型 x 所有資料集的準確率原始數據
- `results/F2_scaling_curve_fits.json` — 各種擬合模型的參數與 goodness-of-fit
- `figures/F2_overall_scaling_curve.png` — CFA overall scaling curve（含 confidence band）
- `figures/F2_topic_scaling_curves.png` — 10 個 CFA 主題的分主題 scaling curves
- `figures/F2_cfa_vs_mmlu_scaling.png` — CFA vs 通用 benchmark 的 scaling 比較
- Table: phase transition analysis 結果（changepoint location, significance）
- 核心發現：金融推理的 scaling 是否比通用推理更陡峭或更平緩

## 資料需求
| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | Hard test set | 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | 已就緒 |
| CRA-Bigdata (1,472) | Large-scale test set | 已就緒 |
| MMLU / MMLU-Pro 公開分數 | Cross-benchmark 比較 | 需收集 |

## 模型需求
- **Local (Ollama)**: phi3.5:3.8b, qwen3:4b, llama3.1:8b, deepseek-r1:14b, qwen3:30b-a3b, qwen3:32b
- **API**: gpt-4o, gpt-4o-mini
- 無需 GPU 訓練，純 inference

## 狀態
Ready — 可直接從 baseline inference 開始，是所有 F 系列點子中最快能產出結果的一個

## 可合併的點子
- **F1 (Domain vs General)** — F1 的多模型 baseline 與 F2 共用相同的推論數據
- **F3 (Cost-Accuracy Pareto)** — F2 的準確率數據直接進入 F3 的 Pareto 分析
- **A1 (Open-Ended Numerical)** — 可在 open-ended 格式上重複 scaling 分析，觀察 MCQ vs open-ended 的 scaling 差異

## 來源筆記
- Kaplan et al. (2020) "Scaling Laws for Neural Language Models"
- Hoffmann et al. (2022) "Training Compute-Optimal Large Language Models" (Chinchilla)
- docs/03-研究方向深度設計.md — 方向 7 提及的 model comparison baseline
- docs/01-數據集完整手冊.md — 三個測試集的完整欄位與規模說明
