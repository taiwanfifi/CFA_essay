---

## 剛才跑了什麼

A5 Option Bias 實驗 POC：用 gpt-4o-mini 對 CFA-Easy 資料集的前 5 題，分別用「有選項」和「無選項」兩種格式測試，量化模型是否依賴選項才能答對。

### POC 結果

| 指標 | 數值 |
|------|------|
| 有選項正確率 | 60%（3/5） |
| 無選項正確率 | 100%（5/5） |
| Option Bias | -40%（去掉選項反而更好） |
| 花費 | $0.0018 |

這個結果很有趣——gpt-4o-mini 在「沒有選項」的情況下反而全部答對（5/5），有選項時反而錯了 2 題（easy_3 和 easy_4 選錯了 A/B/C 字母）。這表示 MCQ 格式可能造成「反向 bias」——選項反而干擾了模型的判斷。

---

## 目前專案總覽：我們有什麼

### 已建好的 6 個新實驗（全部可執行）

| 實驗 | 做什麼 | POC 狀態 |
|------|--------|----------|
| A5_option_bias | 有選項 vs 無選項比較 | 已跑通 |
| I3_noise_red_herrings | 注入雜訊測穩健性（4 類雜訊） | 等跑 |
| D4_overconfident_risk | 從 D1 篩出高信心錯誤，分類風險 | 需 D1 結果 |
| A1_open_ended | 開放式作答 + 三層評判（A/B/C） | 等跑 |
| I1_counterfactual | 數值微擾測記憶 vs 推理 | 等跑 |
| I2_behavioral_biases | 6 種行為金融偏誤（20 個情境題） | 等跑 |

### 已有的 4 個實驗（之前建的）

| 實驗 | 狀態 |
|------|------|
| B1_multistep_agent | 已有程式碼和結果 |
| C1_hybrid_retrieval | 已有 4 種 RAG 實作 |
| D1_confidence_calibration | 已有結果（ECE、Brier Score） |
| E1_error_analysis | 已有錯誤分類結果 |

### 共用模組（shared/）

新建了 4 個共用模組：config.py（模型註冊）、llm_client.py（OpenAI/Ollama 雙後端）、prompts.py（答案提取）、evaluation.py（容差匹配、LLM 裁判、McNemar 檢定）。

### 檔案統計

- 新建/修改：47 個檔案
- 涵蓋 6 個新實驗目錄 + shared 擴充 + findings/ 目錄
- 所有 Python 檔案編譯通過、import 正常

---

## 現在情況

一切正常。A5 的 POC 已驗證整個管道跑通（API 呼叫 → 模型回答 → 答案提取 → 評判 → JSON 輸出 → 統計摘要）。其餘 5 個實驗的程式碼都已就緒，只需依序跑 POC 即可。
