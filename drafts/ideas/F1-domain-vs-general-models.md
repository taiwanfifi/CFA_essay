# F1 領域專用模型 vs 通用模型：CFA 主題層級的系統性比較
# Domain-Specific vs General-Purpose Models on CFA: A Topic-Level Systematic Comparison

## 研究問題

金融領域已出現多個 domain-adapted LLM（如 Salesforce 的 Llama-Fin-8b，透過 FinDAP 三階段管道從 Llama-3-8B-Instruct 微調而成），但現有評估僅報告整體 CFA 準確率，未回答一個關鍵問題：領域專用化（domain specialization）是否在所有 CFA 主題上均勻受益？本研究假設：specialization 對 procedural/calculation-heavy 主題（如 Quantitative Methods, Fixed Income, Derivatives）的幫助最大，但對需要 normative judgment 的主題（如 Ethics, Portfolio Management）幫助有限甚至可能退化。透過在 10 個 CFA 主題上進行細粒度比較，本研究旨在揭示 domain adaptation 的真正收益邊界。

## 核心方法

選取一組通用模型（general-purpose）與一個金融領域專用模型（domain-specific），在完全相同的條件下進行 CFA 題目推論，並按 CFA 10 大主題拆解結果。通用模型涵蓋不同規模與架構：Llama-3.1-8B（與 Llama-Fin-8b 同源基座）、Qwen3-32B（大規模通用）、GPT-4o（commercial SOTA）。領域模型為 Llama-Fin-8b（Salesforce FinDAP, EMNLP 2025）。核心分析是計算每個主題上的 accuracy delta = domain_model - general_model，並按主題特性（procedural vs normative, calculation-heavy vs concept-heavy）進行分組統計檢定。

CFA 10 大主題分類：Ethics & Professional Standards, Quantitative Methods, Economics, Financial Statement Analysis, Corporate Issuers, Equity Investments, Fixed Income, Derivatives, Alternative Investments, Portfolio Management。

## 實驗設計

1. 對三個測試集（CFA-Challenge 90 題、CFA-Easy 1,032 題、CRA-Bigdata 1,472 題）進行 topic annotation，確認每題所屬 CFA 主題
2. 使用統一 prompt template，對所有模型進行 zero-shot MCQ 推論（temperature=0, single pass）
3. 收集每道題的模型回答與正確性判定
4. 按 CFA 主題分組計算 accuracy，建立 Model x Topic 二維結果矩陣
5. 計算 accuracy delta（domain - general），進行 McNemar's test 檢定顯著性
6. 將主題按「procedural vs normative」「calculation-heavy vs concept-heavy」進行分組，測試 delta 是否存在系統性差異
7. 視覺化：radar chart（每個模型的主題雷達圖）、grouped bar chart（delta by topic）

## 需要的積木
- ✅ FinEval-CFA-Challenge (90 題) — 已下載
- ✅ FinEval-CFA-Easy (1,032 題) — 已下載
- ✅ CRA-Bigdata (1,472 題) — 已下載
- ✅ Ollama local models — llama3.1:8b, qwen3:32b 等已就緒
- ✅ OpenAI API — gpt-4o, gpt-4o-mini 可用
- ❌ Topic annotation — 需確認每道題的 CFA 主題標籤（部分資料集可能已含，需驗證）
- ❌ Llama-Fin-8b inference — 需 GPU 環境（HuggingFace 上有權重，可透過 vLLM 或 Colab 推論）
- ❌ Batch inference pipeline — 需建構統一的多模型批次推論腳本

## 預期產出
- `results/F1_model_topic_accuracy_matrix.csv` — Model x Topic 準確率矩陣
- `results/F1_accuracy_delta_analysis.json` — Domain vs General 的主題層級 delta 分析
- `figures/F1_radar_chart.png` — 各模型的 CFA 主題雷達圖
- `figures/F1_delta_bar_chart.png` — 主題層級的 specialization delta 視覺化
- Table: McNemar's test p-values per topic
- 結論：哪些主題從 domain adaptation 受益最多、哪些主題通用模型已足夠

## 資料需求
| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | Hard test set | 已就緒 |
| FinEval-CFA-Easy (1,032) | Standard test set | 已就緒 |
| CRA-Bigdata (1,472) | Large-scale test set | 已就緒 |

## 模型需求
- **Domain-specific**: Llama-Fin-8b（需 GPU inference，可使用 vLLM 或 Colab）
- **General-purpose (local)**: llama3.1:8b（同源基座對照）, qwen3:32b, deepseek-r1:14b
- **General-purpose (API)**: gpt-4o, gpt-4o-mini

## 狀態
Ready — 資料集已就緒，Llama-Fin-8b 推論環境為主要瓶頸（需安排 GPU 資源）

## 可合併的點子
- **F2 (Scaling Law)** — F1 的多模型 baseline 數據可直接供 F2 使用
- **F5 (Chinese vs English)** — 可在 domain vs general 分析上疊加語言維度
- **B1 (Five-Stage Reasoning)** — 可進一步分析 domain model 在哪個認知階段優於 general model

## 來源筆記
- FinDAP (EMNLP 2025): Llama-Fin-8b 的訓練方法與評估結果
- docs/04-FinDAP框架解析.md — FinDAP 三階段管道的技術細節
- docs/01-數據集完整手冊.md — 各測試集的主題分布與欄位說明
