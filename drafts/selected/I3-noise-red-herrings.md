# I3 雜訊與紅鯡魚：金融 LLM 的資訊過濾能力
# Noise and Red Herrings: Measuring Information Filtering in Financial LLMs

## 研究問題

真實金融工作場景充滿雜訊：一份 earnings call transcript 可能長達 20 頁但關鍵資訊只有 3 段、一份研究報告中夾雜大量無關的產業背景描述、同事轉寄的分析信件附帶冗長的免責聲明。CFA 考試本身也有意設計 red herrings（紅鯡魚）——題目中刻意提供無關或誤導性的資訊，測試考生能否辨別並忽略它們。

然而，現有所有金融 LLM 評估都使用**乾淨的、精確的題目文本**，完全不測試模型在噪音環境下的表現。本研究通過系統性注入不同類型與強度的雜訊，量化 LLM 的 **Noise Sensitivity**（雜訊敏感度）——即模型在乾淨 vs 噪音環境下的表現差距。

## 核心方法

### 四類雜訊設計

**Type N1 — 無關數據（Irrelevant Data Injection）**
- 在題目中插入與解題無關但看似相關的數值
- 例如：Bond pricing 題目中額外提供公司的「員工人數」、「成立年份」、「ESG 評分」
- 模型需忽略這些數據，只使用 coupon rate、yield、maturity 等相關資訊
- 雜訊強度控制：1/2/3/5 個額外無關數據點

**Type N2 — 誤導性陳述（Misleading Statements）**
- 插入表面上相關但實際會誤導推理的文字
- 例如：在計算 portfolio return 時插入「根據市場共識，該產業預期成長率為 15%」（這與 portfolio 歷史回報計算無關）
- 模型需辨別：哪些資訊是 relevant 的 context，哪些是 red herrings

**Type N3 — 格式噪音（Format Noise）**
- 模擬真實文檔的格式問題：多餘的空行、重複段落、不完整的表格、混亂的數字格式（$1,000 vs 1000 vs 1,000.00）
- 測試模型的 data extraction robustness
- 雜訊強度控制：輕度（格式不一致）→ 重度（表格斷裂、數字模糊）

**Type N4 — 矛盾資訊（Contradictory Information）**
- 在題目中提供兩段互相矛盾的資訊
- 例如：前文說「利率上升」，後文的表格顯示利率下降
- 測試：模型如何處理矛盾？是否能識別並選擇正確的資訊源？
- 這模擬了真實金融報告中常見的數據不一致問題

### 核心指標

- **Noise Sensitivity Index (NSI)** = (acc_clean - acc_noisy) / acc_clean
  - 0 = 完全不受雜訊影響，1 = 雜訊下完全失效
- **Per-type NSI**：四種雜訊類型各自的敏感度
- **Noise Dose-Response Curve**：隨雜訊強度增加，準確率如何衰退
- **Signal Extraction Rate**：模型在 CoT 中正確識別關鍵資訊的比例

## 實驗設計

**實驗 1：Clean vs Noisy 基線對照**
- 從 CFA-Easy (1,032) 中選取 300 道題
- 每道題製作 Clean 版本 + 4 種 Noisy 版本 = 1,500 次推論 per model
- 計算 overall NSI 和 per-noise-type NSI
- 使用 McNemar's test 確認差異顯著性

**實驗 2：Noise Dose-Response**
- 針對 Type N1（無關數據注入），控制雜訊強度：0/1/2/3/5/8 個無關數據點
- 繪製每個模型的 dose-response curve
- 識別 tipping point：幾個雜訊點開始顯著影響準確率？

**實驗 3：CoT vs Direct Answer 的雜訊過濾能力**
- 假說：Chain-of-Thought 推理模型的雜訊過濾能力更強，因為 CoT 過程中可以 explicitly 辨別 relevant vs irrelevant
- 對比：Direct Answer 模型 vs CoT 模型的 NSI
- 分析 CoT 文本：模型是否在推理過程中提及了 red herring 資訊？提及後是否正確排除？

**實驗 4：RAG 系統的雜訊交互效應**
- RAG retrieval 可能引入額外雜訊（retrieved 的文檔未必都 relevant）
- 對比：Clean prompt / Noisy prompt / RAG-augmented prompt 三種情境的準確率
- 分析：RAG 是增加了有用 signal 還是引入了額外 noise？

**實驗 5：跨模型雜訊耐受力比較**
- 假說：更大的模型雜訊耐受力更強
- 繪製 Model Size vs NSI 曲線
- 辨識：是否存在特定的模型規模閾值，超過後雜訊過濾能力顯著提升？

## 需要的積木
- ✅ FinEval-CFA-Easy (1,032 題) — 已就緒
- ✅ OpenAI API + Ollama local models — 被測模型
- ✅ RAG 系統（4 套實作） — 用於 RAG 交互效應實驗
- ❌ 雜訊注入 pipeline — 需設計四類雜訊的自動生成模板
- ❌ 金融 red herring 素材庫 — 需收集看似相關但實際無關的金融數據片段
- ❌ Signal extraction 評估器 — 需從 CoT 文本中自動判斷模型是否正確識別了關鍵資訊

## 預期產出
- `results/I3_noise_sensitivity.json` — 每個模型的 overall NSI 與 per-type NSI
- `results/I3_dose_response.csv` — Noise intensity × Model 的準確率矩陣
- `results/I3_cot_vs_direct.csv` — CoT vs Direct Answer 的 NSI 對比
- `results/I3_rag_interaction.json` — RAG 系統與雜訊的交互效應
- `figures/I3_dose_response_curve.png` — 雜訊劑量-反應曲線
- `figures/I3_nsi_by_model_size.png` — 模型規模 vs 雜訊敏感度
- `figures/I3_noise_type_radar.png` — 四類雜訊的敏感度雷達圖
- `figures/I3_signal_extraction_sankey.png` — CoT 中資訊辨別流程圖
- Table: Most noise-sensitive CFA topics and question types

## 資料需求
- FinEval-CFA-Easy: 300 道題（× 5 版本 = 1,500 推論 per model）
- FinEval-CFA-Challenge: 90 題（高難度子集的雜訊敏感度分析）
- 自建 red herring 素材庫：~200 條金融雜訊片段
- API 費用預估：gpt-4o 1,500 × ~800 tokens × N_models，約 $30-60 total

## 模型需求
- OpenAI API: gpt-4o, gpt-4o-mini
- Ollama large: qwen3:32b, deepseek-r1:14b（CoT 模型）
- Ollama medium: llama3.1:8b
- Ollama small: qwen3:4b, phi3.5:3.8b
- Direct Answer vs CoT 對比需要相同模型的兩種推理模式

## 狀態
Ready — 所有 dataset 已就緒。核心工作是雜訊注入 pipeline 的設計。建議先以 Type N1（無關數據注入）進行 pilot study（50 題 × 3 雜訊強度），驗證方法可行性。

## 可合併的點子
- **I1** (Counterfactual)：I1 的微擾與 I3 的雜訊是互補的 stress test 維度——I1 改變 signal，I3 添加 noise
- **A1** (Open-ended)：雜訊環境下的 open-ended 回答更能暴露模型的弱點
- **E1** (Error Atlas)：雜訊誘發的錯誤是否有獨特的 error pattern？可以擴展 E1 的 taxonomy
- **C1-C4** (RAG 系列)：實驗 4 的 RAG 交互效應直接與 RAG 研究線接軌

## 來源筆記
- 靈感來自 NLP 領域的 adversarial robustness 研究：Jia & Liang (2017) "Adversarial Examples for Evaluating Reading Comprehension Systems"
- 金融領域的 noise trader 理論：Black (1986) "Noise"
- Red herring 設計參考 CFA 考試命題原則：題目中的 distractor information 是刻意設計的能力測試
- 目標投稿場所：ACL/EMNLP (Robustness track), NeurIPS (Datasets & Benchmarks), Journal of Financial Data Science
