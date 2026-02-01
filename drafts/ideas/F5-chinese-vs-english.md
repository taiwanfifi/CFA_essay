# F5 中英文金融推理能力的跨語言比較
# Chinese vs English Financial Reasoning: Cross-Lingual Performance Gap in LLMs on CFA

## 研究問題

CFA 考試原文為英文，而大量華語圈金融從業者日常使用中文進行專業溝通與決策。當 LLM 以繁體中文接收相同的 CFA 題目時，其金融推理能力是否會下降？現有跨語言 NLP 研究主要集中在通用任務（翻譯、摘要、常識推理），但金融推理涉及精確的技術術語、公式符號與數值計算，語言轉換可能產生獨特的失敗模式。本研究系統性地比較 LLM 在英文原題與繁體中文翻譯題上的表現差異，回答：(1) 語言轉換造成多大的準確率落差？(2) 哪些 CFA 主題受語言影響最大？(3) 中文強勢模型（Qwen3）與英文強勢模型（Llama3.1）的跨語言 gap 是否不同？

## 核心方法

建構 CFA 題目的雙語平行語料（English-Traditional Chinese parallel corpus），在相同模型上進行 controlled bilingual evaluation。

**翻譯管道**：使用 GPT-4o 將 CFA 英文原題翻譯為繁體中文，遵循以下原則：
- 金融專有名詞保留英文或使用標準繁體中文譯名（如 Duration → 存續期間, Yield Curve → 殖利率曲線）
- 數值與公式符號不翻譯
- Exhibit/scenario 中的表格格式保持一致
- 選項翻譯但保留原始選項標號（A/B/C/D）

**品質控制**：隨機抽取 100 題進行人工翻譯品質審查，確保翻譯不引入額外歧義或資訊損失。

**核心比較**：對每個模型，分別在英文版與中文版上執行相同的推論，計算 accuracy gap = acc_en - acc_zh。

## 實驗設計

1. **翻譯建構**：
   - 使用 GPT-4o 翻譯 CFA-Easy (1,032 題) 與 CFA-Challenge (90 題) 為繁體中文
   - 建立翻譯品質評估 rubric（忠實度、流暢度、術語一致性）
   - 人工審查 100 題（~10%），計算翻譯品質分數與常見問題分類
2. **雙語推論**：
   - 每個模型在英文版與中文版上分別推論，temperature=0, zero-shot
   - 模型選擇：qwen3:32b（中文強勢）, qwen3:4b（小型中文模型）, llama3.1:8b（英文強勢）, gpt-4o（多語言 SOTA）, gpt-4o-mini
3. **Overall Gap 分析**：
   - 計算每個模型的 overall accuracy gap
   - Paired McNemar's test 檢定 gap 是否顯著
4. **Topic-level Gap 分析**：
   - 按 CFA 10 大主題分組計算 gap
   - Hypothesis: 純文字推理主題（Ethics）gap 較大，數值計算主題（Quantitative Methods）gap 較小（因數字與公式不受語言影響）
5. **Error Type 分析**：
   - 對「英文答對但中文答錯」的題目進行 error classification
   - 分類：terminology confusion（術語混淆）、instruction misunderstanding（指令誤解）、reasoning degradation（推理退化）、extraction error（數值提取錯誤）
6. **Cross-model Gap 比較**：
   - Qwen3（中文預訓練資料多）vs Llama3.1（英文為主）的 gap 差異
   - 驗證假設：中文預訓練資料量越大，跨語言 gap 越小

## 需要的積木
- ✅ FinEval-CFA-Challenge (90 題) — 英文原題已就緒
- ✅ FinEval-CFA-Easy (1,032 題) — 英文原題已就緒
- ✅ OpenAI API (gpt-4o) — 用於翻譯與推論
- ✅ Ollama local models — qwen3:32b, qwen3:4b, llama3.1:8b
- ❌ 繁體中文翻譯語料 — 需使用 GPT-4o 翻譯 ~1,100 題（API 成本預估 $15-25）
- ❌ 翻譯品質評估框架 — 需設計 rubric 並進行人工審查
- ❌ 跨語言 error classification pipeline — 需設計 prompt 進行中英文錯誤差異分析

## 預期產出
- `datasets/CFA_ZhTW/cfa_easy_zh.json` — CFA-Easy 繁體中文版（1,032 題）
- `datasets/CFA_ZhTW/cfa_challenge_zh.json` — CFA-Challenge 繁體中文版（90 題）
- `results/F5_bilingual_accuracy.csv` — 所有模型在中英文版上的準確率對比
- `results/F5_topic_gap_analysis.json` — 主題層級的跨語言 gap 分析
- `figures/F5_gap_heatmap.png` — Model x Topic 的 accuracy gap 熱力圖
- `figures/F5_error_type_distribution.png` — 中文特有錯誤類型的分布圖
- Table: paired McNemar's test 結果（per model, per topic）
- 實務結論：華語圈金融從業者使用 LLM 進行中文金融推理的可靠性評估

## 資料需求
| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Easy (1,032) | 英文原題 + 翻譯來源 | 已就緒 |
| FinEval-CFA-Challenge (90) | Hard subset | 已就緒 |
| CFA_ZhTW（待建構） | 繁體中文翻譯版 | 需建構 |

## 模型需求
- **中文強勢**: qwen3:32b, qwen3:4b（中文預訓練資料豐富）
- **英文強勢**: llama3.1:8b（英文為主要預訓練語言）
- **多語言 SOTA**: gpt-4o, gpt-4o-mini（官方宣稱多語言能力強）
- 翻譯成本：~1,100 題 x GPT-4o ≈ $15-25

## 狀態
Ready — 翻譯管道建構為首要步驟（~1 天），之後可立即開始雙語推論實驗

## 可合併的點子
- **F1 (Domain vs General)** — 可在跨語言維度上疊加 domain vs general 分析（Llama-Fin-8b 的中文能力？）
- **F4 (Role-Playing)** — 中文 role prompt 是否與英文 role prompt 效果一致？
- **B1 (Five-Stage Reasoning)** — 可分析語言轉換在哪個認知階段造成最大影響
- **A1 (Open-Ended Numerical)** — 在 open-ended 格式上重複跨語言比較，觀察語言對數值提取的影響

## 來源筆記
- Shi et al. (2023) "Language Is Not All You Need: Aligning Perception with Language Models" — 多模態多語言研究
- Lai et al. (2023) "ChatGPT Beyond English" — ChatGPT 的跨語言表現差異
- docs/01-數據集完整手冊.md — CFA 題目格式與欄位說明
- 台灣 CFA 考生社群的實際中文金融術語使用慣例
