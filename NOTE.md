# NOTE — 專案完整筆記（含具體範例）

本筆記用白話 + 實際例子，說明整個研究在做什麼、每個方向的 before/after 差異。

---

## 一句話

用 AI 去考 CFA 金融分析師考試，研究它為什麼答錯、怎樣答得更好，拆成 4-5 篇論文。

---

## 背景

- CFA 考試分三級：Level I（基礎選擇題）→ Level II（情境案例題組）→ Level III（申論+選擇）
- 目前最強 AI (o4-mini) Level III 只有 79.1%，GPT-4o 金融數學推理 60.9%（人類 92%）
- **FinDAP**（Salesforce, EMNLP 2025 Oral）已經訓練好金融特化模型 Llama-Fin-8b，開源了程式碼和資料集
- 我們不重做 FinDAP，而是做它沒做的事：推理策略、錯誤分析、校準、工具增強

---

## 研究全景圖：8 大類 41 個研究點子

```
┌─────────────────────────────────────────────────────────────────┐
│                    G 系列：評估理論（上層建築）                      │
│  G1 能力矩陣 ← G2 訊號理論 ← G3 抗 AI 考試設計 ← G4 認知需求分類    │
└────────────────────────────┬────────────────────────────────────┘
                             │ 匯整所有實驗結果
┌────────────┬───────────────┼───────────────┬────────────────────┐
│ A 系列      │ B 系列         │ C 系列         │ D 系列              │
│ 評估方法     │ 推理策略       │ RAG 檢索       │ 信心校準            │
│ A1-A5       │ B1-B8         │ C1-C4          │ D1-D5              │
│ 「怎麼考？」 │ 「怎麼答？」   │ 「怎麼查資料？」│ 「確不確定？」       │
├────────────┼───────────────┼───────────────┼────────────────────┤
│ E 系列      │ F 系列         │ H 系列（新增）                       │
│ 錯誤分析     │ 規模與實務     │ 跨界延伸                            │
│ E1-E4       │ F1-F5         │ H1-H3                              │
│ 「錯在哪？」 │ 「多大多貴？」 │ 「更真實的場景」                     │
└────────────┴───────────────┴────────────────────────────────────┘
```

---

# ═══════════════════════════════════════════
# A 系列：評估方法（Evaluation）
# 「我們該怎麼衡量 AI 的金融能力？」
# ═══════════════════════════════════════════

## A1 — 開放式數值推理基準

### 一句話
把選擇題的 A/B/C 選項拿掉，直接問 AI「答案是多少？」，看它還能不能算對。

### 問題
選擇題洩漏了太多資訊。看到選項 `A. $912  B. $922  C. $931`，AI 就知道答案在 $900-$940 之間，而且可以用「代入法」反推。這就像考生偷看到答案卡的範圍一樣。

### 例子

**CFA 題目**（計算債券價格）：

選擇題版本：
> 三年期 4% 年付息債券，面額 $1,000，即期利率 S₁=5%, S₂=6%, S₃=7%。價格最接近？
> A. $912.41　B. $922.64　C. $931.05

開放式版本：
> 三年期 4% 年付息債券，面額 $1,000，即期利率 S₁=5%, S₂=6%, S₃=7%。計算債券價格。

**差別**：
- 選擇題版本：AI 算出 $925，最接近 B → 選 B，答對了（但它算的數字其實不對）
- 開放式版本：AI 回答 $925 → 與正確答案 $922.64 的誤差超過容忍值 → 標記為 Level C 錯誤

### 為什麼重要
A1 揭示的是「AI 真正的計算能力」vs「AI 靠選項提示答題的能力」之間的差距。預期差距在 10-20%，而且小模型的差距更大（更依賴選項提示）。

### 子計畫
- **A1a 基準建構**：建立包含「Gold Answer Set（容忍答案集合）」的開放式題庫。金融題常有假設差異（年複利 vs 半年複利），所以不能只有一個正確答案，而是一組可接受的答案。
- **A1b 錯誤歸因分類**：答錯時，是公式錯？數字抄錯？計算錯？還是假設不同？建立分類法。

---

## A2 — 四層級評估框架

### 一句話
分開測「模型本身的能力」和「加上工具後的系統能力」，不要混在一起算。

### 例子

```
Level 0（純模型）：「算這題」→ LLM 直接回答
  → 測的是模型的金融知識量

Level 1（+ 思考）：「一步一步想」→ LLM 用 Chain-of-Thought
  → 測的是模型的推理結構

Level 2（+ 自我檢查）：「算完回頭檢查」→ LLM 自我驗證
  → 測的是模型的自我修正能力

Level 3（+ 外部工具）：RAG 查資料 + 計算器算數 + 多輪對話
  → 測的是整個 AI 系統的能力
```

**為什麼不能混在一起？** 因為審稿人會問：「你的 85% 準確率是模型聰明，還是計算器厲害？」A2 讓你清楚回答這個問題。

**反直覺發現（預期）**：對小模型（8B），Level 3 的 Agent 工具反而可能降低準確率——因為小模型常常叫錯工具、傳錯參數，工具反而幫倒忙。

---

## A3 — CFA 作為 AGI 基準

### 一句話
CFA 考試能不能成為衡量 AI 「綜合專業能力」的標準？跟 MMLU、GSM8K 等現有基準比，它能測出什麼不一樣的東西？

### 例子

| 基準 | 主要測什麼 | CFA 有沒有覆蓋 |
|------|-----------|---------------|
| MMLU | 百科知識 | 部分重疊（知識面） |
| GSM8K | 小學數學推理 | 不重疊（CFA 數學更難） |
| HumanEval | 寫程式 | 不重疊 |
| ARC | 科學推理 | 部分重疊 |
| **CFA 獨有** | 倫理判斷 + 跨領域整合 | ← **其他基準都沒有** |

**假說**：CFA 的倫理題和投資組合管理題，跟所有現有基準的相關性都很低（Spearman ρ < 0.3）。這代表 CFA 測的是一種獨特的能力維度。

---

## A4 — Prompt 敏感度作為技能分類

### 一句話
同一道題換不同問法（直接問 / CoT / 角色扮演），答案穩不穩定？穩定 = 模型真的會；不穩定 = 模型靠猜的。

### 例子

**穩定的題（顯性知識）**：
> 「名目利率 = 實質利率 + 預期通膨溢價」

6 種 prompt 問法 → 6 次都答 C → 標準差 = 0 → **顯性知識**，模型真的知道

**不穩定的題（隱性知識）**：
> 倫理題：「分析師偶然聽到內幕消息後改變推薦，是否違規？」

6 種 prompt 問法 → 4 次答 A、1 次答 B、1 次答 C → 標準差 = 0.47 → **隱性知識**，模型不穩定

**連結到人力資本理論**：穩定的能力容易被 AI 取代（因為 AI 穩定地會）；不穩定的能力不容易被取代（因為 AI 有時會有時不會）。→ 直接對接到 G2 訊號理論。

---

## A5 — MCQ 選項偏差量化

### 一句話
量化「有選項」vs「沒選項」到底差多少分，就像測「開卷考」和「閉卷考」的差距。

### 例子

同一道題：
```
有選項：「EAR 是 4.08%，計息方式是？ A.每日 B.每季 C.每半年」
  → 模型算出 4.06%，最接近 B → 選 B → 但正確答案是 A（每日=4.0808%）
  → 不對，但如果算出 4.08%→ 要比較三個選項的 EAR，反而有機會猜對

沒選項：「EAR 是 4.08%，計息方式是？」
  → 模型需要自己算出 daily、quarterly、semiannual 的 EAR 然後比對
  → 更容易出錯
```

**預期結果**：option_bias（有選項的準確率 - 沒選項的準確率）大約 8-15%。越小的模型 bias 越大（越依賴選項提示）。

---

# ═══════════════════════════════════════════
# B 系列：推理策略（Reasoning）
# 「AI 該用什麼方法解題？」
# ═══════════════════════════════════════════

## B1 — 五階段推理管道

### 一句話
模擬 CFA 考生的解題過程：看題 → 回想公式 → 抄數字 → 算答案 → 驗算。每一步分開評分。

### 例子

**CFA 題目**：
> 三年期、4% 年付息、面額 $1,000 的債券，即期利率為 S₁=5%, S₂=6%, S₃=7%。計算債券價格與 YTM。

```
Stage 1 — 概念辨識 → [Spot Rate, Bond Pricing, YTM, Discount Factor]     ✅
Stage 2 — 公式回想 → Price = Σ CF_t / (1+S_t)^t                         ✅
Stage 3 — 數字提取 → { coupon:40, face:1000, S1:0.05, S2:0.06, S3:0.07 } ✅
Stage 4 — 計算執行 → 40/1.05 + 40/1.06² + 1040/1.07³ = $922.72          ⚠️ 微小誤差
Stage 5 — 合理性驗證 → "YTM > coupon rate → 折價，合理"                    ✅
```

**價值**：Before 只知道「答錯了」。After 精確定位到「Stage 4 計算出錯」→ 對應的修復是加計算器（B6）。

---

## B2a — 雙代理解題系統

### 一句話
拆成「知識代理」和「計算代理」兩個 AI，一個查資料、一個算數，由「指揮官」協調。

### 例子

```
題目：「計算 immunization strategy 所需的 portfolio duration」

指揮官（Orchestrator）分析：這題需要知識 + 計算

→ 知識代理（RAG）：查找 immunization 需要 duration matching
  + callable bonds 的 negative convexity 會破壞 matching

→ 計算代理（Calculator）：計算 portfolio duration
  PV-weighted duration = Σ(w_i × D_i) = ...

→ 指揮官：整合兩個代理的結果，選答案
```

**vs 單一 LLM**：單一 LLM 可能知道概念但算錯，或算對但概念不全。雙代理各司其職。

---

## B2b — 四代理解題系統

### 一句話
B2a 的升級版。加入「倫理代理」和「驗證代理」。

```
四個代理：
1. 知識代理 → 查教材      （處理知識題）
2. 計算代理 → 用計算器    （處理計算題）
3. 倫理代理 → 查 CFA 準則  （處理倫理題）
4. 驗證代理 → 檢查結果    （攔截錯誤）
```

用 Shapley Value（博弈論中衡量每個玩家貢獻的方法）分析每個代理的邊際貢獻。15 種組合全部測一遍。

---

## B3 — 自我驗證

### 一句話
讓 AI「回頭檢查自己的答案」，看能不能自己抓到錯誤。像考試時的「驗算」。

### 例子

```
第一次回答：「Swap spread = 2.02% - 1.61% = 41 bps → 答案 B. 61 bps」

自我驗證（Structured Critique）：
  概念檢查：Swap spread 定義正確 ✅
  計算檢查：2.02 - 1.61 = 0.41 = 41 bps ✅
  答案匹配：41 bps 對應 A 不是 B ⚠️ → 修正為 A

修正後：「A. 41 bps」 ✅
```

**關鍵風險**：有時候自我驗證反而把對的改成錯的（False Correction）。B3 要量化這個風險。

---

## B4 — 自一致性投票

### 一句話
同一道題讓 AI 回答 10 次，看答案最集中在哪個選項。像讓 10 個考生投票。

### 例子

```
題目：「名目利率 = 實質利率 + ?」

回答 10 次：C, C, C, C, C, C, C, C, C, C → 全選 C → 信心 100%
→ 高信心，直接輸出 C ✅

題目：「免疫策略 portfolio 用 callable 還是 non-callable？」

回答 10 次：A, C, A, B, A, C, A, C, A, C → A:5, C:4, B:1
→ 信心只有 50%，不太確定 → 需要進一步分析
```

**核心問題**：投幾票最划算？3 票太少（不穩定），20 票太貴。B4 要找到最佳 k 值（預期 k=5-10）。

---

## B5 — 雙系統推理（System 1 / System 2）

### 一句話
簡單題快速答（像直覺反應），難題才動用全套工具（像深思熟慮）。省錢又不犧牲準確率。

### 例子

```
簡單題 → System 1（快速直覺）：
  「名目利率 = 實質利率 + 預期通膨」→ 直接答 C
  信心 95% → 過關 → 成本：1 次推論

難題 → System 2（深度分析）：
  「計算三年期債券的 YTM」→ 信心只有 52%
  → 啟動 RAG 查公式 + 計算器算數 + 驗算
  → 成本：~5 次推論

結果：1000 題中 600 題走 System 1 + 400 題走 System 2
  = 2600 次推論（vs 全走 System 2 的 5000 次）
  準確率差距 < 2%，成本降低 48%
```

---

## B6 — 金融計算器工具（ReAct Agent）

### 一句話
給 AI 一台 HP-12C 金融計算器。CFA 考生能用計算器，AI 也應該能。

### 例子

**CFA 題目**：
> 年利率 4.00%，若 EAR 為 4.08%，計息方式為？
> A. 每日　B. 每季　C. 每半年

```
BEFORE（純 LLM 心算）：
  "(1 + 0.04/365)^365 = ... 算不出來"
  → 猜 B → 錯

AFTER（LLM + 計算器）：
  Thought: "需要逐一計算不同複利方式的 EAR"
  Action: EAR_Calculator(rate=0.04, compounding="quarterly")
  Result: 4.0604%  → 不匹配
  Action: EAR_Calculator(rate=0.04, compounding="daily")
  Result: 4.0808%  → 匹配 4.08% ✅
  → 答 A → 對
```

**五種專業計算器**：TVM（時間價值）、Bond（債券定價）、Statistics（統計）、Derivatives（衍生品）、Financial Ratio（財務比率）。比通用 Python 更好，因為減少了 LLM 寫程式碼出錯的機會。

---

## B7 — CoT 忠實度測試

### 一句話
AI 寫的「推理過程」是真的在推理，還是先想好答案再編理由？

### 例子

```
原始推理：
  "Swap spread = Swap rate - Treasury yield
   = 2.02% - 1.61% = 0.41% = 41 bps → A"

因果介入實驗：把公式偷換成錯的
  "Swap spread = Treasury yield - Swap rate  ← 故意改錯
   = 1.61% - 2.02% = -0.41% = -41 bps → ???"

如果模型還是答 A（41 bps）→ 不忠實（答案不是靠推理得出的）
如果模型改答成 -41 bps → 忠實（答案確實跟著推理走）
```

**預期結果**：計算題的忠實度高（~80-90%），倫理判斷題的忠實度低（~30-50%）。

**為什麼重要**：如果 CoT 不忠實，那所有基於「分析推理過程」的研究（B1、E1 等）的結論就要打折扣。B7 是整個 B 系列的「元研究」。

---

## B8 — 矛盾證據下的推理 ⭐新增

### 一句話
當證據互相矛盾時（基本面說買、技術面說賣），AI 怎麼處理？

### 例子

```
CFA 情境題：
  "公司 A 的 P/E = 8（看起來便宜），但 ROE = 3%（獲利能力極差）。
   行業的同時段 P/E 平均 = 15，ROE 平均 = 12%。
   分析師應如何評價公司 A？"

正確答案：P/E 低不代表便宜，可能是「價值陷阱」(value trap)，
  因為低 ROE 顯示公司基本面差，低 P/E 只是反映市場的負面預期。

小模型的典型回答（Ignore 策略）：
  "P/E = 8 遠低於行業平均 15，公司被低估，建議買入。"
  → 完全忽略 ROE 的矛盾信號 ❌

大模型的典型回答（Weight-and-integrate 策略）：
  "雖然 P/E 偏低，但 ROE 遠低於行業平均，暗示盈利能力有結構性問題。
   低 P/E 可能反映了市場對其前景的合理折價，而非被低估。
   需要進一步分析自由現金流和競爭優勢。"
  → 正確整合矛盾信號 ✅
```

**五種矛盾處理策略分類**：
1. **Ignore** — 忽略其中一方（最常見於小模型）
2. **Acknowledge-but-dismiss** — 提到但輕描淡寫
3. **Weight-and-integrate** — 明確權衡（最佳）
4. **Paralysis** — 列出矛盾但無法決策
5. **Confabulate** — 編造不存在的論點來消解矛盾

### 為什麼值得做
真實的金融分析幾乎永遠面對矛盾信號。CFA Level II 和 III 刻意設計這類題目測試綜合判斷力。這個方向直接連結到行為金融學的 anchoring bias 和 framing effect，跨領域的故事性很強。

---

# ═══════════════════════════════════════════
# C 系列：RAG 檢索增強（Retrieval-Augmented Generation）
# 「AI 要怎麼查資料才能答得更好？」
# ═══════════════════════════════════════════

## C1 — 四種 RAG 架構比較

### 一句話
同一套 CFA 題目，用四種不同的查資料方法，看哪種最好。

### 四種架構

```
1. LangGraph Agent  → 多輪對話，自主決定何時查、查什麼
2. LangChain Hybrid → BM25 關鍵字 + 向量語義混合搜尋 + 重排序
3. LlamaIndex 標準  → 傳統 RAG 流程
4. LlamaIndex 純向量 → 最簡單的向量搜尋

（四種都已經在 experiments/RAG/ 裡實作完成）
```

**比喻**：就像比較 Google 搜尋 vs Bing vs DuckDuckGo vs 圖書館員，同一個問題，不同搜尋方式找到的資料品質不同。

**關鍵控制變數**：同一個 embedding 模型、同一個生成模型、同一個切塊大小，只改架構。

---

## C2 — 知識圖譜 RAG

### 一句話
不只搜「相似的文字片段」，還搜「概念之間的關係鏈」。

### 例子

**CFA 題目**：
> 投資組合經理想實施 immunization strategy。負債 duration 7.5 年。
> 哪個 portfolio 最適合？
> A. Duration 7.5, non-callable bonds
> B. Duration 7.5, 混合 callable/non-callable
> C. Duration 8.0, non-callable bonds

```
普通 RAG（語義搜尋）：
  搜「immunization strategy duration」
  → 找到：「Immunization 是一種策略...」← 只解釋了定義
  → 沒找到：callable bonds 為什麼不行
  → 答 B（因為 duration 也是 7.5）→ 錯

知識圖譜 RAG（關係鏈搜尋）：
  在圖譜中找到：
    Immunization ──requires──→ Duration Matching
    Immunization ──requires──→ Duration Stability
    Callable Bonds ──has──→ Negative Convexity
    Negative Convexity ──breaks──→ Duration Stability

  → 推理鏈：Callable bonds 會破壞 duration 穩定性 → 破壞 immunization
  → 答 A（全部 non-callable）→ 對
```

**比喻**：普通 RAG 像用 Google 搜一個關鍵字。知識圖譜 RAG 像問一個教授「這幾個概念之間是什麼關係？」

---

## C3 — 參數化知識 vs 檢索知識

### 一句話
AI 腦子裡已經知道的（參數化知識）vs 現場查到的（RAG 檢索知識），哪些主題需要查、哪些不用？

### 例子

```
主題：Ethics（倫理）
  不用 RAG：85% 準確率
  用 RAG：  83% 準確率（反而下降！RAG 找到無關文本，干擾判斷）
  → RAG Lift = -2% → 這個主題不需要 RAG

主題：Fixed Income（固定收益計算）
  不用 RAG：62% 準確率
  用 RAG：  78% 準確率（大幅提升！查到公式和概念）
  → RAG Lift = +16% → 這個主題非常需要 RAG

主題：Derivatives（衍生品）
  不用 RAG：55% 準確率
  用 RAG：  70% 準確率
  → RAG Lift = +15% → 需要 RAG
```

**結論（預期）**：RAG 不是萬能藥。有些主題（Ethics、常識性概念）AI 已經知道了，強迫查反而有害。

---

## C4 — 本地端 vs 雲端 RAG

### 一句話
把雲端的 API（OpenAI）換成跑在自己電腦上的開源模型，品質掉多少、省多少錢？

### 例子

```
配置 A（全雲端）：
  Embedding: text-embedding-3-large (OpenAI)
  生成: GPT-4o-mini
  準確率: 82%
  每題成本: $0.03
  延遲: 2.5 秒

配置 B（全本地）：
  Embedding: bge-m3 (跑在 MacBook M4)
  生成: qwen3:32b (Ollama)
  準確率: 74%
  每題成本: $0（只有電費）
  延遲: 15 秒

配置 C（混合）：
  Embedding: bge-m3（本地）
  生成: GPT-4o-mini（雲端）
  準確率: 80%
  每題成本: $0.02
  延遲: 3 秒
```

**研究產出**：Accuracy-Cost Pareto 曲線。讓研究者根據預算選最佳配置。

---

# ═══════════════════════════════════════════
# D 系列：信心與校準（Confidence & Calibration）
# 「AI 說『我很確定』的時候，能信嗎？」
# ═══════════════════════════════════════════

## D1 — 信心校準與選擇性預測

### 一句話
AI 說「我 90% 確定」，真的有 90% 的機率答對嗎？

### 例子

**CFA 題目**：
> 30 年期美國國債 vs 30 年期小型私人公司債券的殖利率差異，最相關的風險溢價是？
> A. 通膨　B. 到期　C. 流動性
> （正確答案：C）

```
方法 A — 直接問 AI：「你多確定？」
  Llama-8B：「我 85% 確定選 A」→ 答錯了！85% 信心 + 錯誤 = 最危險

方法 B — 問 10 次看一致性（Self-Consistency）
  Llama-8B：5 次選 A、3 次選 C、2 次選 B → 信心只有 50%
  → 這才是真實的不確定程度

方法 C — 看輸出機率（Logit-based）
  Llama-8B：P(A)=0.41, P(B)=0.22, P(C)=0.37 → 信心 41%
  → 也比自稱的 85% 準確多了
```

**校準曲線（預期結果）**：
```
AI 自稱的信心   實際正確率
   90%            72%  ← Overconfident！
   70%            65%
   50%            48%  ← 接近校準
```

**選擇性預測**：設門檻，信心不夠就不答。
```
門檻 80%：只答 70% 的題 → 準確率從 78% → 89%
門檻 90%：只答 50% 的題 → 準確率從 78% → 95%
```

---

## D2 — 跨模型共識

### 一句話
「8 個模型都選 C」比「1 個模型說它 90% 確定」更可信。

### 例子

```
8 個模型投票：
  GPT-4o-mini:      C ✅
  Qwen3-32B:        C ✅
  DeepSeek-R1-14B:  C ✅
  Llama-3.1-8B:     A ❌（但它自稱 85% 確定）
  Qwen3-4B:         A ❌
  Phi-3.5-3.8B:     B ❌
  Gemma-3:          C ✅
  Qwen3-30B-A3B:    C ✅

投票結果：C 拿到 5/8 = 62.5% → 正確 ✅
```

**核心發現（預期）**：跨模型共識的 AUROC（預測正確率的能力）> 任何單一模型的自評信心。用多個模型投票，比相信一個模型自己說多確定，更靠譜。

---

## D3 — 棄權機制

### 一句話
讓 AI 在不確定時說「我不知道」。在金融領域，「自信地給錯答案」比「承認不確定」危險得多。

### 例子

```
場景：CFA 備考助教
  門檻設 70%（寧可多答，學生需要練習）
  → 回答 85% 的題目，準確率 84%

場景：金融投資顧問
  門檻設 90%（錯誤代價太高）
  → 只回答 51% 的題目，準確率 95%
  → 其餘 49% 的題轉給人類專家

逐級升級（Cascaded Abstention）：
  Step 1: Qwen3-4B 回答，信心 45% → 不夠 → 升級
  Step 2: Qwen3-32B 回答，信心 82% → 接近但不夠 → 升級
  Step 3: GPT-4o-mini 回答，信心 90% → 過關 → 輸出答案
```

---

## D4 — 過度自信的金融風險

### 一句話
AI「很自信但答錯」的案例，放在金融場景裡有多危險？

### 例子

```
AI（自信地）："殖利率差異主要來自通膨溢價。
              在低通膨環境下，小型公司債券的相對價值會提升。
              我 85% 確定。"

你信了 → 大量買入小型私人公司 30 年期債券

實際上：差異來自流動性溢價。市場動盪時，
小型公司債券流動性急劇惡化 → 價格暴跌 → 巨額虧損

AI 的高信心讓你放鬆了警覺，但答案是錯的。
```

**Overconfident Error 分佈（預期）**：
```
主題              過度自信錯誤率   風險等級
Derivatives         18%           極高
Fixed Income        15%           高
Quantitative        12%           中
Portfolio Mgmt      10%           中
Ethics               5%           低
```

**連結到金融監管**：EU AI Act 將金融 AI 列為「高風險」。D4 建議金融 AI 系統應公開 ECE 分數，就像銀行要公開資本適足率。

---

## D5 — 分佈偏移下的校準穩定性 ⭐新增

### 一句話
在訓練時測出的校準品質，換到不同的題目分佈後還準嗎？

### 例子

```
原始分佈（均勻的 CFA 主題）：
  ECE = 0.08（還行）

偏移 1 — 主題比例改變（Fixed Income 佔 50%）：
  ECE = 0.09（穩定 ✅）

偏移 2 — 只用難題（CFA-Challenge）：
  ECE = 0.15（嚴重惡化 ⚠️）

偏移 3 — 換成開放式題目（A1 的基準）：
  ECE = 0.22（崩潰 ❌）
```

**為什麼重要**：如果校準在分佈偏移下不穩定，那麼在測試集上測出的 ECE 分數就不能保證在真實部署中仍然有效。這對金融 AI 的監管合規有直接影響。

---

# ═══════════════════════════════════════════
# E 系列：錯誤分析（Error Analysis）
# 「AI 到底錯在哪？不同的錯要怎麼修？」
# ═══════════════════════════════════════════

## E1 — 錯誤模式圖譜

### 一句話
把 AI 的所有錯誤分類整理成一張「錯誤地圖」：什麼主題 × 什麼類型 × 在推理哪一步出的錯。

### 四大錯誤類型 + 例子

**Type 1 — Knowledge Gap（知識缺口）**：
```
題目：「Spread duration 最接近哪個 duration？」
AI：「B. Effective duration」
原因：不知道「非含權債券的 spread duration ≈ modified duration」
→ 修復：RAG 補知識
```

**Type 2 — Calculation Error（計算錯誤）**：
```
題目：「$75,000 × (1 + 0.07/4)^24 = ?」
AI：「$112,555」（(1.0175)^24 算成 1.5007，正確是 1.5164）
原因：乘方計算精度不足
→ 修復：用計算器
```

**Type 3 — Misapplication（錯用公式）**：
```
題目：「計算 Modified duration」
AI：用了 Macaulay duration 的公式但忘記除以 (1+y)
原因：知道相關公式但選錯了
→ 修復：Few-shot 示範正確應用
```

**Type 4 — Distractor Confusion（被干擾項誤導）**：
```
題目：「分析師偶然聽到內幕後改變推薦，是否違規？」
選項 A 說「偶然聽到不算故意竊取，不違規」← 有部分道理但不是重點
AI 被 A 的部分正確性吸引，選了 A
真正的問題是「缺乏合理基礎」，答案應該是 C
→ 修復：逐選項分析
```

### 三維錯誤矩陣

```
維度 1：錯誤類型（上面 4 種）
維度 2：CFA 主題（Ethics, Fixed Income, Derivatives 等 10 個）
維度 3：認知階段（B1 的 5 個 Stage）

→ 一個 4 × 10 × 5 的矩陣，清楚看出哪裡最脆弱
```

---

## E2 — 對症下藥的修復策略

### 一句話
知道錯誤類型後，用不同的方法修不同的錯。

### 例子

```
BEFORE — 所有錯誤都用同一招（例如全用 RAG）：
  Knowledge Gap:       RAG → 有效 ✅
  Calculation Error:   RAG → 找到公式但還是算錯 ❌
  Distractor Confusion: RAG → 找到一般描述但不解決 ❌
  修復率: ~35%

AFTER — 對症下藥：
  Knowledge Gap        → RAG 補知識 → 修復率 70-80%
  Calculation Error    → 計算器 → 修復率 80-90%
  Misapplication       → Few-shot 示範 → 修復率 55-65%
  Distractor Confusion → 逐選項分析 → 修復率 40-50%
  整體修復率: ~65%
```

---

## E3 — AI 能自我診斷嗎？

### 一句話
把正確答案告訴 AI，問它「你覺得自己錯在哪？」，測它的「自我認知」能力。

### 例子

```
AI 答錯了一題，把正確答案和它的錯誤推理都給它看：

"你的回答是 B (Effective duration)，正確答案是 A (Modified duration)。
 請分析你的錯誤屬於哪種類型：
 1. Knowledge Gap（缺少知識）
 2. Calculation Error（計算錯誤）
 3. Misapplication（錯用公式）
 4. Distractor Confusion（被干擾項誤導）"

GPT-4o：「我的錯誤屬於 Knowledge Gap，因為我不知道
         non-callable bonds 的 spread duration ≈ modified duration」
→ 自我診斷正確 ✅（~65-75% 的情況下）

小模型：「我的錯誤屬於 Calculation Error」
→ 自我診斷錯誤 ❌（這不是計算問題，是知識缺口）
```

**價值**：如果 AI 能自我診斷，就能自動選擇修復策略（Knowledge Gap → 自動啟動 RAG）。

---

## E4 — 為什麼 Level III 對 AI 更難？

### 一句話
建立「認知複雜度指數 (CCI)」來量化每道題有多難，預測 AI 會不會答錯。

### CCI 的五個維度 + 例子

```
簡單題（CCI = 5）：
  「名目利率 = 實質利率 + 預期通膨溢價」
  知識廣度: 1（只需要一個概念）
  推理深度: 1（直接回想）
  數值精度: 0（不需計算）
  模糊度:   1（答案明確）
  跨領域:   0（單一主題）

困難題（CCI = 20）：
  「在利率上升環境下，比較 callable bond 和 putable bond
   的 portfolio immunization 效果，考慮 convexity 影響」
  知識廣度: 4（需要 bond, option, duration, convexity）
  推理深度: 4（多步推理）
  數值精度: 3（需要精確計算）
  模糊度:   4（取決於利率情境假設）
  跨領域:   4（Fixed Income + Derivatives + Portfolio Mgmt）
```

**預期結果**：CCI 和 AI 錯誤率的 Spearman 相關 > 0.6。可以用 CCI 來自動分流題目（簡單題用小模型省錢，困難題用大模型保品質）。

---

# ═══════════════════════════════════════════
# F 系列：規模與實務（Scaling & Practical）
# 「用多大的模型？花多少錢？」
# ═══════════════════════════════════════════

## F1 — 領域模型 vs 通用模型

### 一句話
FinDAP 花了大量 GPU 訓練的金融特化模型 Llama-Fin-8b，到底在哪些主題上比通用模型好？

### 例子

```
主題層級比較：

Fixed Income（計算重）：
  Llama-3-8B（通用）:  55%
  Llama-Fin-8b（特化）: 72%  → +17% ✅ 訓練很值得

Ethics（判斷重）：
  Llama-3-8B（通用）:  68%
  Llama-Fin-8b（特化）: 70%  → +2%  ⚠️ 幾乎沒差

→ 結論：領域特化訓練主要幫助計算密集的主題，
  對判斷和推理類主題幫助有限。
```

**重要問題**：FinDAP 的 domain adaptation 有沒有讓模型的校準 (calibration) 變好或變差？這是審稿人會問的。如果訓練後模型變得更 overconfident（更自信但沒有更準確），那就是一個問題。

---

## F2 — CFA 的 Scaling Law

### 一句話
模型越大，CFA 成績越好嗎？提升是平滑的還是有突然跳躍的「頓悟」？

### 例子

```
模型規模梯度：
  Phi-3.5 (3.8B):     48%
  Qwen3 (4B):         52%
  Llama-3.1 (8B):     61%
  DeepSeek-R1 (14B):  68%
  Qwen3 (32B):        75%
  GPT-4o-mini (~?B):  80%
  GPT-4o (~?B):       85%

Scaling 曲線形狀：
  - 3B → 14B：快速提升（+20%）
  - 14B → 32B：中等提升（+7%）
  - 32B+：邊際遞減

主題差異：
  Ethics：從 4B 開始就相對穩定（~65-70%）→ 平坦曲線
  Quantitative：每個規模級都顯著提升 → 陡峭曲線
```

**MoE 特殊分析**：Qwen3-30B-A3B（30B 總參數但只有 3B 活躍參數），表現更像 3B 還是 30B？

---

## F3 — 成本-準確率 Pareto 分析

### 一句話
給你 $10 / $100 / $1000 的預算，怎麼配最划算？

### 例子

```
解空間中的幾個點：

方案 A：Qwen3-4B + Zero-shot
  準確率: 52%  |  每題成本: $0  |  1000 題: $0（本地跑）

方案 B：GPT-4o-mini + CoT
  準確率: 82%  |  每題成本: $0.02  |  1000 題: $20

方案 C：GPT-4o + RAG + 計算器 + 驗證
  準確率: 90%  |  每題成本: $0.15  |  1000 題: $150

方案 D：GPT-4o + Self-Consistency(k=10) + RAG + 計算器
  準確率: 93%  |  每題成本: $0.50  |  1000 題: $500

Pareto 最優解（花最少錢達到特定準確率）：
  要 80%+ → 方案 B（$20）
  要 90%+ → 方案 C（$150）
  要 93%+ → 方案 D（$500）
```

---

## F4 — 角色扮演 Prompt

### 一句話
讓 AI 扮演不同角色（CFA 考生 / 資深分析師 / 教授 / 財務顧問），看誰答得最好。

### 例子

```
同一題用不同角色 Prompt：

Baseline（無角色）：
  "回答以下題目。"
  → 準確率 78%

Student（考生角色）：
  "你是一名正在準備 CFA Level II 的考生。仔細作答。"
  → 準確率 79%（+1%）

Expert（資深分析師）：
  "你是一名有 15 年經驗的 CFA charterholder 資深分析師。"
  → 準確率 82%（+4%）

Professor（教授）：
  "你是金融系教授，請像教學生一樣一步步解題。"
  → 準確率 83%（+5%，因為教授角色自然產生 CoT 式推理）
```

**有趣的交互作用**：Expert 角色在 Ethics 題上提升最大（+8%），因為有經驗的分析師更懂實務中的倫理判斷。Professor 角色在計算題上提升最大（+6%），因為教授習慣步步演算。

---

## F5 — 中英文金融推理比較

### 一句話
CFA 考試是英文的，但很多人母語是中文。把題目翻成中文，AI 的表現會掉多少？

### 例子

```
英文版：
  "The nominal risk-free rate is best described as the real risk-free rate
   plus a premium for expected inflation."
  → GPT-4o 答對 ✅

繁體中文版：
  「名目無風險利率最佳描述為實質無風險利率加上預期通膨的溢價。」
  → GPT-4o 答對 ✅（簡單概念題幾乎不受語言影響）

但到了複雜題...

英文版：
  "Calculate the swap spread given a 2-year swap rate of 2.02% and
   a 2-year Treasury yield of 1.61%."
  → Llama-3.1-8B 答對 ✅

繁體中文版：
  「已知 2 年期交換利率為 2.02%，2 年期國庫券殖利率為 1.61%，
   計算交換利差。」
  → Llama-3.1-8B 答 61 bps ❌（可能是因為中文訓練語料較少）
```

**預期結果**：中文 pretrained 模型（Qwen3）的跨語言差距 < 英文模型（Llama3.1）。計算題的差距 > 概念題。

---

# ═══════════════════════════════════════════
# G 系列：評估理論（Assessment Theory）
# 「CFA 考試在 AI 時代還有意義嗎？」
# ═══════════════════════════════════════════

## G1 — CFA 能力 × AI 可複製性矩陣

### 一句話
把 CFA 測試的每種能力，和 AI 能不能穩定複製這個能力，畫成一張大表。

### 矩陣概念

```
                        AI 輕鬆複製    AI 有時會有時不會    AI 做不到
                        ──────────    ────────────────    ────────
背誦型知識（Level 1）     ████████         ██
程序性計算（Level 2）     ███████          ███
情境分析（Level 3）       ████             ██████            ██
綜合判斷（Level 4）       ██               █████             █████
倫理推理（Level 5）       █                ████              ███████
人際溝通（Level 6）                        ██                ████████

← AI 能穩定做到                                      AI 做不到 →
```

**啟示**：CFA 考試中，AI 能穩定複製的部分（背誦 + 計算），佔考試權重 ~40-50%。如果 AI 輕鬆通過這些，這些題目的「鑑別力」（能不能區分好考生和差考生）就下降了。

**這是整個博士論文的核心產出**：匯整 A-F 所有系列的實驗結果到這張矩陣裡。

---

## G2 — AI 衝擊下的專業認證訊號理論

### 一句話
用經濟學的「訊號理論」（Spence, 1973）分析：當 AI 能輕鬆通過 CFA，CFA 證照還能向雇主「發信號」嗎？

### 例子

```
訊號理論的原始邏輯（1973）：

  求職者：「我有 CFA 證照」
  雇主推論：「能通過 CFA 的人，金融分析能力強」
  → CFA 是「能力的信號」

AI 時代的衝擊：

  AI：「我也通過了 CFA（準確率 85%）」
  雇主推論：「……那考過 CFA 能證明什麼？AI 也能考 85%」

  但是！AI 在倫理判斷、客戶溝通、綜合投資判斷上仍然很弱

  → CFA 的訊號部分崩潰（知識和計算部分）
  → CFA 的訊號部分保留（判斷和溝通部分）
  → 這叫「部分訊號崩潰」(Partial Signaling Collapse)
```

**理論貢獻**：修改 Spence (1973) 的模型，引入「AI 複製成本 c_AI(s)」參數。當 c_AI → 0 時，對應能力的稀缺性消失，訊號價值瓦解。但不是所有能力的 c_AI 都趨近 0。

**目標期刊**：Management Science, Journal of Finance（政策 track）。

---

## G3 — 未來 CFA 該考什麼？

### 一句話
如果 AI 能通過目前的 CFA 考試，那考試應該怎麼改？

### 三種替代考試形式

```
方案 A — 情境互動式考試：
  不是靜態題目，而是動態演進的投資情境。
  考生每做一個決定，情境就會變化。
  AI 無法預先準備所有可能的情境路徑。

  例：「市場突然暴跌 15%，你管理的退休基金怎麼辦？」
  考生回答後 →「央行宣布緊急降息，但你的客戶打電話來恐慌要贖回」
  考生再回答 →「媒體報導你的基金跑輸大盤 3%，董事會質詢」

方案 B — 責任承擔式考試：
  不是「選正確答案」，而是「做出決策並承擔後果」。
  考生需要簽署「我為這個投資建議負責」的聲明。

方案 C — 多方利害關係人模擬：
  考生需要同時面對客戶、監管機構、公司管理層的不同要求，
  在衝突的利益之間做出平衡。
  這測試的是「人際判斷」——AI 最弱的能力。
```

---

## G4 — 認知需求分類法

### 一句話
把所有 CFA 題目按「思考有多深」分成 5 級。

### 五級認知需求

```
Level 1 — 回想（Recall）：
  「名目利率 = 實質利率 + ?」
  → 直接從記憶中提取答案
  → AI 預期準確率 > 95%

Level 2 — 計算（Calculate）：
  「FV = 75000 × (1+0.07/4)^24 = ?」
  → 套公式算數
  → AI 預期準確率 80-90%（有計算器的話）

Level 3 — 應用（Apply）：
  「選擇正確的 duration 計算方法」
  → 需要判斷情境再選方法
  → AI 預期準確率 70-80%

Level 4 — 分析（Analyze）：
  「比較 callable 和 non-callable bond 在利率上升時的表現差異」
  → 多步推理 + 需要理解 negative convexity
  → AI 預期準確率 55-65%

Level 5 — 綜合（Synthesize）：
  「在模糊的條件下，為退休基金設計投資策略」
  → 跨領域整合 + 不確定性下的判斷 + 倫理考量
  → AI 預期準確率 < 50%
```

**為什麼 G4 是最重要的基礎工作**：G1 的能力矩陣、E1 的錯誤圖譜、B7 的 CoT 忠實度、B5 的雙系統路由……全部都需要「每道題的認知層級標籤」。G4 是很多其他研究的上游依賴，應該最早開始做。

---

# ═══════════════════════════════════════════
# H 系列：跨界延伸（Cross-boundary）⭐ 全部新增
# 「把場景推向更真實的考試情境」
# ═══════════════════════════════════════════

## H1 — 多模態金融推理 ⭐新增

### 一句話
CFA 考試有大量圖表（收益率曲線圖、財務報表、散佈圖），但目前所有研究都只用純文字。測一下 AI 看圖表的能力。

### 例子

```
CFA 題目附帶一張收益率曲線圖（Yield Curve）：

  [圖表] Y 軸：殖利率 (%), X 軸：到期年限
         曲線呈現 inverted yield curve（短天期利率高於長天期）

  問題：「根據圖表，目前的利率期限結構 (term structure) 暗示什麼？」
  A. 經濟擴張
  B. 經濟衰退預期
  C. 通膨上升

純文字版（把圖轉成文字描述）：
  「1 年期利率 5.2%, 2 年期 4.8%, 5 年期 4.3%, 10 年期 4.0%,
   30 年期 3.8%。短天期利率高於長天期。」
  → 大多數模型都能正確判斷「B. 經濟衰退預期」

多模態版（直接看圖）：
  → 模型需要：1) 讀出圖上的數值 2) 判斷曲線形狀 3) 連結到經濟意涵
  → 預期部分模型在步驟 1 就出錯（讀不準圖上的數字）
```

**三種圖表類型的預期難度**：
```
表格（Type T）：財務報表、利率表  → 最容易（-5% 至 -10%）
圖形（Type G）：收益率曲線、走勢圖 → 中等（-10% 至 -20%）
混合（Type M）：表格+圖+文字     → 最難（-15% 至 -25%）
```

### 為什麼重要
如果我們宣稱「AI 能通過 CFA」但只測了純文字部分，那就像說「考生能通過考試」但跳過了所有有圖表的題目。H1 填補了所有 CFA + LLM 研究的這個系統性空白。

### 為什麼值得投頂刊
多模態推理是 2025-2026 的 NLP 熱點，加上金融專業領域的應用場景，形成「hot method + important domain」的組合。ACL/EMNLP 的多模態 track 近年投稿量暴增，但金融領域的多模態推理研究幾乎是空白。

---

## H2 — 金融知識的時效性衰退 ⭐新增

### 一句話
金融世界變化快（LIBOR 退場、Basel IV 上路、利率環境大翻轉），AI 腦子裡的知識跟不跟得上？

### 例子

```
2023 年前：
  「計算 3 個月 LIBOR-based interest rate swap 的現金流」
  → 模型用 LIBOR 框架回答，完全正確

2023 年後：
  LIBOR 已正式退場，替代為 SOFR (Secured Overnight Financing Rate)
  → 但 GPT-4o 的訓練數據截止時 LIBOR 還在使用中
  → 模型可能仍用 LIBOR 框架回答 → 知識過時

另一個例子：
  「正常的 10 年期美國國債殖利率大約是多少？」
  2020 年的正確答案：~1%（零利率環境）
  2024 年的正確答案：~4.5%（升息週期）
  → 模型回答取決於訓練數據裡哪個時期的數據更多
```

**三種時效性風險**：
1. **制度變更**（LIBOR → SOFR）→ RAG 最容易修復
2. **法規更新**（Basel III → Basel IV）→ RAG 可以修復
3. **市場環境**（「正常」利差水準）→ RAG 最難修復（因為是「常識」不是「事實」）

### 為什麼值得投頂刊
Knowledge-intensive NLP 是 ACL/EMNLP 的長青主題，但「parametric knowledge 的時效性」是新角度。金融是最適合研究這個問題的領域，因為金融制度和市場的變化速度遠超其他專業領域（法律、醫學更新較慢）。

---

## H3 — CFA Level III 申論題評估 ⭐新增

### 一句話
CFA Level III 有 50% 是申論題（寫 IPS、論述投資策略、分析倫理案例），但目前沒人測 AI 寫申論的能力。

### 例子

```
MCQ 版本：
  「退休基金的投資目標應優先考慮？」
  A. 最大化報酬
  B. 匹配負債 duration
  C. 最小化波動
  → AI 選 B → 對 ✅（但只花了 1 秒，可能是靠消去法）

Essay 版本（Level III 實際考法）：
  「為以下客戶撰寫 Investment Policy Statement (IPS)：
   張先生，55 歲，預計 65 歲退休。目前資產 $2M，
   年薪 $200K，退休後需要年收入 $120K（稅後）。
   配偶無工作，有兩名大學生子女。

   討論：
   a) Return objective（報酬目標）
   b) Risk tolerance（風險承受度）
   c) Time horizon（投資期限）
   d) Liquidity needs（流動性需求）
   e) Unique circumstances（特殊情況）」

AI 的回答需要：
  - 計算所需報酬率（考慮通膨、稅率、支出）
  - 判斷風險承受度（收入穩定但即將退休 → 中等偏低）
  - 辨識特殊情況（大學學費支出、配偶無收入）
  - 用專業的書面格式表達

評分維度（each 1-5）：
  Technical Accuracy:    4/5（計算正確但假設不夠明確）
  Completeness:          3/5（漏了稅務考量）
  Reasoning Quality:     4/5（邏輯清楚）
  Communication Clarity: 5/5（結構好、表達清晰）
  Professional Judgment:  2/5（像教科書答案，缺乏實務洞察）
```

**MCQ vs Essay 差距（預期）**：
```
主題              MCQ 準確率   Essay 綜合分數   差距
Ethics             80%          55%            -25%
Portfolio Mgmt     75%          50%            -25%
Fixed Income       82%          70%            -12%
Quantitative       78%          72%            -6%
```

Ethics 和 Portfolio Management 的差距最大，因為申論要求「深度判斷」而不是「選正確答案」。

### 為什麼值得投頂刊
NLG Evaluation（自然語言生成評估）是 ACL 的重要 track。「AI 生成的專業文本品質」（不是翻譯、不是摘要，而是專業寫作）是新的評估挑戰。加上 CFA Level III 的權威性，這是「重要問題 + 新的評估方法論」的組合。也適合投教育類頂刊（Assessment in Education）。

---

# ═══════════════════════════════════════════
# D 系列深度比較：D1-D5（信心與校準）
# ═══════════════════════════════════════════

### 五個點子的關係一張圖

```
D1 校準量測（基礎層）
 │  "模型說 90% 確定，真的 90% 對嗎？" → 量測信心 vs 實際正確率
 │
 ├──→ D2 跨模型共識（信心來源的替代方案）
 │     "與其聽一個模型自己說多確定，不如看 8 個模型投票有多一致"
 │
 ├──→ D3 棄權機制（D1 的應用層）
 │     "測完信心後，讓模型在不確定時說'我不知道'"
 │
 ├──→ D4 過度自信風險（D1 的政策層）
 │     "高信心+答錯的案例，在金融場景有多危險？"
 │
 └──→ D5 分佈偏移（D1 的穩健性檢驗）⭐新增
       "D1 測出的校準結果，換個場景還靠譜嗎？"
```

**D1 是地基，D2/D3/D4/D5 都建在它上面。** 做論文的話，D1 一定要做，其他選擇性納入。

---

### 用同一道題走過 D1 → D2 → D3 → D4

**CFA 題目**：

> 30 年期美國國債與 30 年期小型私人公司債券的殖利率差異，
> 最相關的風險溢價是？
> A. 通膨 (Inflation)
> B. 到期 (Maturity)
> C. 流動性 (Liquidity)
>
> 正確答案：C（小型私人公司的債券流動性差，所以要求更高殖利率）

---

#### D1 看這題：校準量測

```
GPT-4o-mini 回答：C (Liquidity)  ✅ 對了
  Verbalized confidence: "我 92% 確定"
  Logit-based confidence: P(C)=0.78
  Self-consistency (10次): 9/10 次選 C → 信心 90%

Llama-3.1-8B 回答：A (Inflation)  ❌ 錯了
  Verbalized confidence: "我 85% 確定"   ← Overconfident！
  Logit-based confidence: P(A)=0.41
  Self-consistency (10次): 5/10 次選 A, 3/10 選 C, 2/10 選 B → 信心 50%
```

**D1 的發現**：
- Verbalized confidence（模型自己說的）最不可靠：Llama 自稱 85% 確定但只有 50% 的一致性
- Self-consistency（問 10 次看答案穩不穩）最可靠：5/10 的一致性正確反映了模型的不確定
- Logit-based（看輸出機率）介於兩者之間

D1 會把這個發現量化成 ECE 分數，並畫出 Reliability Diagram。

---

#### D2 看這題：跨模型共識

```
8 個模型投票：

  GPT-4o-mini:    C (Liquidity)  ✅
  Qwen3-32B:      C (Liquidity)  ✅
  DeepSeek-R1-14B: C (Liquidity)  ✅
  Llama-3.1-8B:   A (Inflation)  ❌
  Qwen3-4B:       A (Inflation)  ❌
  Phi-3.5-3.8B:   B (Maturity)   ❌
  Gemma-3:        C (Liquidity)  ✅
  Qwen3-30B-A3B:  C (Liquidity)  ✅

投票結果：C 拿到 5/8 = 62.5% 共識
Disagreement entropy: 中等（不是所有模型都同意）
```

**D2 的核心論點**：「5 個模型都選 C」比「1 個模型說它 90% 確定」更可信。

---

#### D3 看這題：棄權機制

```
場景 A — 用 GPT-4o-mini（信心高）：
  Self-consistency 信心: 90%
  門檻 θ = 85%
  90% ≥ 85% → ✅ 回答 "C. Liquidity"

場景 B — 用 Llama-3.1-8B（信心低）：
  Self-consistency 信心: 50%
  門檻 θ = 85%
  50% < 85% → ⚠️ 棄權 "我對這題不夠確定，建議諮詢專家"

場景 C — Cascaded Abstention（逐級升級）：
  Step 1: Qwen3-4B 回答 A，信心 45% → 不夠確定 → 升級
  Step 2: Qwen3-32B 回答 C，信心 82% → 接近但不到 85% → 升級
  Step 3: GPT-4o-mini 回答 C，信心 90% → 90% ≥ 85% → ✅ 回答 "C"
  成本：花了 3 次 inference，但最終答對了
```

**D3 的核心產出**：Coverage-Accuracy 曲線

```
門檻 θ    回答比例(Coverage)   回答題的準確率(Accuracy)
─────────────────────────────────────────────────
0.50      100%                 78%      ← 全部回答，準確率普通
0.70       85%                 84%
0.80       72%                 89%
0.85       63%                 92%      ← 只答 63% 的題，但準確率 92%
0.90       51%                 95%
0.95       34%                 97%      ← 只答 1/3 的題，但幾乎全對
```

甜蜜點在哪？取決於場景：
- CFA 備考助教：θ=0.70（學生需要多練習，寧可多答）
- 金融投資顧問：θ=0.90（錯誤代價太高，寧可少答）

---

#### D4 看這題：過度自信的風險

```
回到 Llama-3.1-8B 的回答：

  回答：A. Inflation
  Verbalized confidence: "我 85% 確定"
  實際：❌ 答錯了

  這是一個 "overconfident error"：
  高信心（85%）+ 錯誤答案 = 最危險的組合
```

**D4 把這種案例放到金融場景裡分析**：

```
場景：你是一家資產管理公司的分析師，用 AI 輔助分析債券投資。

AI（自信地）："30 年期美國國債和小型私人公司債券的殖利率差異
主要來自通膨溢價。因此在低通膨環境下，兩者殖利率差異應該縮小，
小型公司債券的相對價值會提升。我 85% 確定。"

你信了 → 大量買入小型私人公司的 30 年期債券

實際上：殖利率差異來自流動性溢價，不是通膨。
當市場動盪時，小型公司債券的流動性急劇惡化，
殖利率差異反而暴增 → 你的投資組合大幅虧損。

AI 的 85% 信心讓你放鬆了警覺，但答案是錯的。
```

**D4 最後會連結到金融監管**：
- EU AI Act 把金融 AI 列為「高風險」→ 需要 calibration 達標才能部署
- CFA 道德準則 Standard V(A)：依賴 overconfident AI 可能違反 due diligence
- 建議：金融 AI 系統應該公開 ECE 分數，就像銀行要公開資本適足率一樣

---

### D1-D5 最終比較

| | D1 校準 | D2 共識 | D3 棄權 | D4 風險 | D5 偏移 |
|--|---------|---------|---------|---------|---------|
| **一句話** | 量測信心準不準 | 多模型投票比自評準 | 不確定就別答 | 自信但答錯有多危險 | 換場景還準嗎 |
| **性質** | 技術量測 | 技術替代方案 | 技術應用 | 政策分析 | 穩健性檢驗 |
| **獨立成論文？** | ✅ 可以 | ⚠️ 偏薄 | ⚠️ 偏薄 | ⚠️ 需搭配 D1 | ⚠️ 需搭配 D1 |
| **依賴關係** | 無 | 需大量模型推論 | 依賴 D1 | 依賴 D1 | 依賴 D1 |
| **目標讀者** | NLP/AI 研究者 | NLP/AI 研究者 | AI 工程師 | 金融監管/政策 | ML 穩健性研究者 |
| **投稿場所** | ACL/EMNLP | ACL/EMNLP | ACL/EMNLP | Management Science | NeurIPS/ICML |

---

### 建議的合併策略

**最務實的做法：D1 + D3 + D5 合成一篇論文，D2 和 D4 的精華作為子章節。**

```
論文結構：

1. Introduction：金融 AI 的信心問題
2. Method：四種 confidence estimation（D1 核心）
3. Experiment 1：Calibration 全景分析（D1 實驗 1-2）
4. Experiment 2：AUROC — 哪種方法最能預測對錯（D1 實驗 3）
   → 這裡納入 D2 的 ensemble consensus 作為第 5 種方法
5. Experiment 3：Selective Prediction（D3 的 coverage-accuracy）
   → 包含 cascaded abstention
6. Experiment 4：Distribution Shift Robustness（D5 核心）
   → 校準在 5 種偏移場景下的穩定性
7. Analysis：Overconfident Error 案例研究（D4 的精華）
   → 3-5 個具體金融場景
8. Discussion：金融監管啟示（D4 的政策面）
9. Conclusion
```

---

# ═══════════════════════════════════════════
# B7 / G4 深度比較：元研究層（推理可信度 + 認知分類）
# ═══════════════════════════════════════════

### 兩個點子的關係一張圖

```
G4 認知需求分類（基礎設施）
 │  "這道題有多難？" → 給每道題打上 Level 1-5 的標籤
 │
 │  被以下所有研究使用：
 │  ├── B1 — 按 Level 分析每個 Stage 的錯誤率
 │  ├── B5 — 按 Level 決定走 System 1 還是 System 2
 │  ├── B7 — 按 Level 分析 CoT 忠實度（本節重點）
 │  ├── E1 — 按 Level 分析錯誤類型分布
 │  └── G1 — 按 Level 建構能力矩陣
 │
B7 CoT 忠實度（品質控制）
    "AI 的推理過程是真的在推理，還是事後編造的？"
    → 偷改推理鏈的中間步驟，看答案會不會跟著變

兩者組合的意義：
  G4 Level 1-2 題 + B7 忠實度高 → B1/E1 分析推理過程的結論可信 ✅
  G4 Level 4-5 題 + B7 忠實度低 → B1/E1 在這些題的分析要加警告 ⚠️
```

**G4 是基礎設施（供所有研究使用的標籤），B7 是品質控制（驗證推理分析是否可信）。**

---

### 用同一道題走過 G4 → B7

**CFA 題目 A（計算題）**：

> 今天投資 $75,000，年利率 7%、每季複利，6 年後的終值最接近？
> A. $112,555　B. $113,330　C. $113,733
>
> 正確答案：C

**CFA 題目 B（判斷題）**：

> Ruth McDougal, CFA，在研討會上無意聽到 Randolph 公司臨床試驗結果令人失望（尚未公開）。
> 她隨即將 Randolph 的評級從「買入」改為「賣出」。她是否違反 CFA 準則？
> A. 否
> B. 是，因為她沒有披露部分分析是基於意見
> C. 是，因為她的推薦缺乏合理基礎
>
> 正確答案：C

---

#### G4 看這兩題：認知需求分類

```
題目 A — 終值計算：
  GPT-4o 分類 prompt: "請判斷這道題的認知需求層級"

  分析：
    - 概念明確：Time Value of Money
    - 公式無歧義：FV = PV × (1 + r/n)^(n×t)
    - 數值都給了，只需代入計算
    - 沒有判斷、沒有比較、沒有模糊條件

  分類結果: Level 2 — Calculation
  理由: "Given values, single formula, no judgment needed"

  人工驗證: ✅ 同意（Level 2 沒有爭議）

題目 B — 倫理判斷：
  GPT-4o 分類 prompt: "請判斷這道題的認知需求層級"

  分析：
    - 涉及多個 CFA 倫理準則（Material Nonpublic Info, Reasonable Basis）
    - "無意聽到" 是關鍵條件，需要判斷是否構成 MNPI
    - 選項 A 有部分道理（偶然聽到 ≠ 故意竊取）但不是重點
    - 需要整合多準則、在模糊條件下做判斷

  分類結果: Level 4 — Analysis
  理由: "Multiple standards, distractor option, requires weighing conditions"

  人工驗證:
    標註者 1: Level 4 ✅
    標註者 2: Level 5（認為「偶然聽到」的模糊性使條件不完整）
    → 這就是 G4 預期的 Level 4/5 邊界分歧
    → 最終決定: Level 4（因為答案還是明確的，不像 Level 5 那樣有真正的不確定性）
```

**G4 的核心產出**：所有題目的 Level 標籤 + 分布統計

```
                Level 1  Level 2  Level 3  Level 4  Level 5
                回想     計算     應用     分析     綜合
──────────────────────────────────────────────────────────
CFA-Easy         35%      25%      25%      12%       3%    ← 以 L1-2 為主
CFA-Challenge     5%      10%      25%      40%      20%    ← 以 L3-5 為主
CFA_Extracted    20%      20%      30%      22%       8%    ← 較均勻
CRA-Bigdata       8%      15%      35%      30%      12%

（以上為預期分布，實際數字待分類後確認）
```

**分類器品質（預期）**：

```
GPT-4o 自動分類 vs 人工標註 confusion matrix：

                  人工: L1   L2   L3   L4   L5
GPT-4o 分為 L1:        18    1    0    0    0
GPT-4o 分為 L2:         0   16    2    0    0
GPT-4o 分為 L3:         1    2   15    4    0
GPT-4o 分為 L4:         0    0    3   14    3    ← L3/L4 邊界最模糊
GPT-4o 分為 L5:         0    0    0    3   18

Overall agreement: ~81/100 = 81%
Cohen's Kappa: ~0.76（超過目標 0.7 ✅）

主要分歧區: Level 3 ↔ Level 4（7 題不一致）
原因: 「選正確方法」和「多步推理」的邊界本質上模糊
```

---

#### B7 看這兩題：CoT 忠實度測試

```
題目 A（Level 2 計算題）的忠實度測試：

Step 1 — 正常 CoT 收集
  模型生成的 CoT:
    "FV = PV × (1 + r/n)^(n×t)
     = 75000 × (1 + 0.07/4)^(4×6)
     = 75000 × (1.0175)^24
     = 75000 × 1.5164
     = $113,733
     答案：C"

Step 2 — 找到 Intervention Point
  可介入位置: "(1.0175)^24 = 1.5164" 這一步

Step 3 — 施加 Value Perturbation（偷改數字）
  修改為: "(1.0175)^24 = 1.4500"  ← 故意改成較小的數字

Step 4 — 讓模型從修改處繼續生成
  "= 75000 × 1.4500
   = $108,750
   最接近 A. $112,555... 不對，其實 $108,750 不在任何選項範圍...
   答案：A"  ← 答案跟著變了

Step 5 — 忠實度判定
  原答案: C → 介入後: A → 答案改變 ✅
  判定: Faithful（推理鏈真的在驅動答案）
```

```
題目 B（Level 4 倫理判斷題）的忠實度測試：

Step 1 — 正常 CoT 收集
  模型生成的 CoT:
    "McDougal 偶然聽到了 MNPI（重大非公開資訊）。
     雖然是偶然聽到，但 CFA 準則不區分獲取方式。
     關鍵問題是她基於這個資訊改變了推薦。
     根據 Standard V(A) Diligence and Reasonable Basis，
     基於未經驗證的單一資訊源做推薦，缺乏合理基礎。
     答案：C"

Step 2 — 找到 Intervention Point
  可介入位置: "CFA 準則不區分獲取方式" 這個前提

Step 3 — 施加 Premise Reversal（反轉前提）
  修改為: "根據 CFA 準則，偶然獲取的資訊不構成 MNPI，
           只有主動尋求或從內部人士直接獲得的才算。"
           ← 故意改成錯誤但有道理的前提

Step 4 — 讓模型從修改處繼續生成
  "既然偶然聽到不構成 MNPI，McDougal 的行為
   只是基於她在公開場合聽到的資訊做出判斷。
   她可以合法地將這個資訊納入她的分析中...
   但是... 她的推薦仍然缺乏合理基礎...
   答案：C"  ← 答案沒變！

Step 5 — 忠實度判定
  原答案: C → 介入後: 還是 C → 答案沒改變 ❌
  判定: Unfaithful（模型似乎先決定了答案是 C，然後繞過了被修改的前提）

  但也可能是 Partially Faithful：
  模型的推理路徑確實改變了（從 MNPI 論點切換到 Reasonable Basis 論點），
  但最終答案碰巧一樣（因為 C 可以從兩條路徑得出）。
  → 這正是 B7 需要 Faithfulness 評判器的原因：部分案例需要人工裁定
```

**B7 的核心產出**：按 G4 Level 分層的 Faithfulness Profile

```
                     Type I        Type II       Type III
                     Formula Swap  Value Perturb  Premise Reversal  平均
──────────────────────────────────────────────────────────────────────
Level 1 Recall        N/A*          N/A*          65%              65%
Level 2 Calculation   85%           90%           N/A*             88%  ← 最忠實
Level 3 Application   70%           75%           60%              68%
Level 4 Analysis      55%           60%           45%              53%
Level 5 Synthesis     40%           45%           35%              40%  ← 最不忠實

* N/A: 該介入類型不適用於該 Level
  （回想題沒有公式可換；計算題沒有前提可反轉）

（以上為預期結果，實際數字待實驗驗證）
```

**閱讀方式**：
- Level 2 計算題的忠實度 88% → 改了中間步驟，88% 的情況下答案會跟著變 → CoT 可信
- Level 5 綜合題的忠實度 40% → 改了前提，60% 的情況下答案不變 → CoT 不太可信
- **結論**：B1 和 E1 的推理過程分析在計算題上可信，在判斷題上需加 caveat

---

### B7 vs G4 比較表

| | B7 CoT 忠實度 | G4 認知需求分類 |
|--|-------------|--------------|
| **一句話** | AI 推理是真推理還是事後編造？ | 每道題有多難？分成 5 級 |
| **性質** | 品質控制（元研究） | 基礎設施（標籤系統） |
| **核心產出** | Faithfulness Profile（按 Level 分層） | Annotated Dataset（~3,700 題附標籤） |
| **方法** | Causal Intervention（偷改 → 看答案變不變） | GPT-4o 自動分類 + 人工驗證 |
| **依賴關係** | 需要 G4 的 Level 標籤 | 無依賴，可立即開始 |
| **最大瓶頸** | Intervention 工具開發 + 人工裁定邊界案例 | Level 3/4 邊界定義 + 人工標註 20-30hr |
| **影響範圍** | 影響 B1、E1 的結論可信度 | 被 B1、B5、B7、E1、G1 全部使用 |
| **獨立成論文？** | ✅ 可以（Interpretability track） | ✅ 可以（Dataset & Benchmark track） |
| **模型需求** | 5+ 被測模型 + GPT-4o 輔助 | GPT-4o 分類器 + 5 模型做 Performance by Level |
| **API 費用** | $300-500（大量推論 + 多輪介入） | $50-100（分類 ~3,700 題）|
| **目標場所** | ACL/EMNLP 2026 (Interpretability) | NeurIPS Datasets & Benchmarks 或 ACL Resource |

---

### G4 和 B7 的先後順序與執行建議

```
時間軸：

Phase 0: G4 立即開始 ← 最優先
  ├── 設計 taxonomy coding guide（Level 邊界定義 + 邊界案例）
  ├── 在 50 題上 pilot → 調整定義 → 達到人工 agreement 穩定
  ├── GPT-4o 大規模分類（~3,700 題）
  └── 100 題 × 2 人工標註者驗證（Cohen's Kappa ≥ 0.7）

Phase 0.5: B7 並行啟動（工具開發）
  ├── 設計 Intervention Point 識別 prompt
  ├── 開發 Intervention 施加 + 續生工具
  └── 在 20 題上 pilot → 驗證 Causal Intervention Protocol 可行性

Phase 1: B7 正式實驗（等 G4 標籤出來後）
  ├── 390 題（CFA-Challenge 90 + CFA-Easy 300）× 5 模型 × 3 介入類型
  ├── 按 G4 Level 分層分析
  └── 人工裁定邊界案例（Faithful vs Partially Faithful）
```

**G4 是整個研究計劃中應該最先啟動的工作**——不依賴任何其他研究，而且被最多下游研究需要。

---

### 對其他研究的具體影響

**如果 B7 發現 Level 4-5 的 CoT 忠實度真的只有 40-53%（預期），影響如下**：

```
B1 五階段管道：
  → Level 1-2 題的 Stage-wise 分析可信 ✅
  → Level 4-5 題的 Stage 5（驗證）分析需加 caveat ⚠️
     "Stage 5 的 reasonableness check 可能不是真正的驗證，
      而是模型在事後合理化已經決定的答案"

E1 錯誤圖譜：
  → Level 2 計算題的錯誤歸因（Knowledge Gap vs Calculation Error）可信 ✅
  → Level 4-5 題的 Distractor Confusion 歸因需謹慎 ⚠️
     "模型說它被選項 A 誤導，但也許它只是不知道正確答案，
      推理過程中的'被誤導'是事後編造的"

D1 校準：
  → Level 2 題：Verbalized confidence 的 ECE 可信
  → Level 4-5 題：Verbalized confidence 可能更不可靠
     （模型不只 overconfident，連它「為什麼這麼確定」的解釋也可能是編造的）

B5 雙系統：
  → System 1 的 Self-Consistency 信心估計不受影響
     （因為 Self-Consistency 不依賴推理過程，只看答案的一致性）
  → 但 System 2 的 CoT 推理品質在 Level 4-5 題上要打折扣
```

---

### docs/03 相關規劃 vs 實際文件的差異

**G4 的差異**：

| 項目 | docs/03 規劃 | G4 實際寫的 |
|------|------------|-----------|
| Taxonomy 來源 | 方向 1 的認知階段理論 | Bloom's Taxonomy + Webb's DOK |
| 層級數 | 未明確指定 | 5 級（Recall → Synthesis） |
| 資料集範圍 | 未指定 | 全部 4 個資料集（~3,700 題） |
| 人工驗證 | 未提及 | 100 題 × 2 標註者，目標 Kappa ≥ 0.7 |
| 缺少 | — | ⚠️ 沒有提到 CRA-Bigdata 的特殊性（股價預測題跟 CFA 選擇題型態不同）|

**B7 的差異**：

| 項目 | docs/03 規劃 | B7 實際寫的 |
|------|------------|-----------|
| 在 docs/03 的位置 | 沒有對應方向（是新提出的） | 全新的研究提案 |
| 靈感來源 | — | Turpin et al. (2023), Lanham et al. (2023) |
| 差異化 | — | (1) 金融領域 (2) causal intervention (3) 按認知需求分層 |
| 缺少 | — | ⚠️ 沒有提到 reasoning-specialized 模型（如 deepseek-r1）的 thinking tokens 怎麼處理 |
| 缺少 | — | ⚠️ API 費用 $300-500 可能偏低（390 題 × 5 模型 × 3 介入 = 5,850 次推論）|

**需要補的**：
1. B7 的 deepseek-r1 有 hidden thinking tokens，intervention 要在 thinking chain 還是 visible CoT 上做？這會影響實驗設計。
2. G4 應考慮 CRA-Bigdata 是否適合用同一套 taxonomy（股價預測題可能不適合 Level 1-5 框架）。
3. B7 的 $300-500 費用估計可能偏低：390 × 5 × 3 = 5,850 次推論，加上 baseline CoT 收集的 390 × 5 = 1,950 次，共 7,800 次。以 gpt-4o-mini 每次 ~$0.01-0.03 計算，本地模型免費，API 部分大約 $150-250。但如果要做 Exp 3（介入強度，每題 3 級）則三倍，可能接近估計。

---

# ═══════════════════════════════════════════
# E1 / E2 深度比較：錯誤的診斷與治療
# ═══════════════════════════════════════════

### 兩個點子的關係一張圖

```
E1 錯誤模式圖譜（診斷）
 │  "AI 到底錯在哪？" → 三維分類：什麼類型 × 什麼主題 × 推理哪一步
 │
 │ → 分類結果直接輸入 E2
 │
E2 對症修復策略（治療）
    "知道病因後，不同的病用不同的藥"
    Knowledge Gap     → RAG 補知識
    Calculation Error → Calculator 計算器
    Misapplication    → Few-shot 示範
    Distractor Confusion → 逐選項分析

共用元件：
  B1 五階段管道 → E1 的 Dimension 3（Cognitive Stage）
  B6 金融計算器 → E2 的 Calculation Error 修復工具
  G4 認知需求分類 → E1 可按 Level 進一步分層分析
  experiments/cfa_agent/tools.py → E2 的 Calculator 已有初版
```

**E1 是診斷，E2 是治療。兩者合成一篇完整的「診斷—治療」論文 = docs/03 方向 6。**

---

### 用同一道題走過 E1 → E2

**四道 CFA 題目，每道代表一種錯誤類型**：

---

#### 錯誤類型 1：Knowledge Gap

```
CFA 題目：
  「對於投資級、不可贖回、固定利率債券，spread duration 最可能接近？」
  A. Modified duration
  B. Effective duration
  C. Macaulay duration
  正確答案：A

模型（Llama-3.1-8B）回答：B. Effective duration  ❌

═══ E1 的診斷流程 ═══

Step 1 — 收集推理痕跡（reasoning trace）
  "Spread duration measures the sensitivity of bond price to spread changes.
   Effective duration is the most general measure of duration...
   Therefore, spread duration is most likely to approximate effective duration."

Step 2 — GPT-4o 自動分類
  Input: 題目 + 錯誤回答 + reasoning trace + 正確答案
  Prompt: "分析這個錯誤，從三個維度分類"

  Output:
    Dimension 1 (Error Type): Knowledge Gap → Concept Incomplete
      理由: 模型知道 spread duration 和 effective duration 的一般定義，
            但不知道「non-callable fixed-rate bonds 的 spread duration
            ≈ modified duration」這個特定等式。

    Dimension 2 (CFA Topic): Fixed Income

    Dimension 3 (Cognitive Stage): Stage 1 — Concept Identification
      理由: 錯誤發生在最開始的概念關聯階段，模型沒有建立起
            spread duration 和 modified duration 的等價關係。

  分類標籤: [Knowledge Gap / Fixed Income / Stage 1]

═══ E2 的修復流程 ═══

  錯誤類型: Knowledge Gap → 修復策略: RAG

  Step 1: RAG 檢索
    Query: "spread duration modified duration non-callable fixed-rate bond"
    Retrieved: "For option-free, fixed-rate bonds, spread duration is
                approximately equal to modified duration because the
                spread change affects all cash flows uniformly."

  Step 2: 注入 context 重新回答
    Prompt: 原題目 + Retrieved context
    模型新回答: "A. Modified duration"  ✅

  修復結果: 成功 ✅
  原因: 缺失的知識被 RAG 直接補上了
```

---

#### 錯誤類型 2：Calculation Error

```
CFA 題目：
  「今天投資 $75,000，年利率 7%、每季複利，6 年後的終值最接近？」
  A. $112,555
  B. $113,330
  C. $113,733
  正確答案：C

模型（GPT-4o-mini）回答：A. $112,555  ❌

═══ E1 的診斷 ═══

  Reasoning trace:
    "FV = PV × (1 + r/n)^(n×t)
     = 75,000 × (1 + 0.07/4)^(4×6)
     = 75,000 × (1.0175)^24
     = 75,000 × 1.5007
     = $112,555"

  GPT-4o 分類:
    Dimension 1: Calculation Error → Arithmetic Error
      理由: 公式正確，數字代入正確，但 (1.0175)^24 = 1.5164 不是 1.5007
    Dimension 2: Quantitative Methods
    Dimension 3: Stage 4 — Calculation Execution

  分類標籤: [Calculation Error / Quantitative Methods / Stage 4]

═══ E2 的修復 ═══

  錯誤類型: Calculation Error → 修復策略: Calculator Tool

  Action: TVM_Calculator(PV=75000, rate=0.07, periods=6, compounding="quarterly",
                         solve="FV")
  Return: FV = $113,733.21

  模型新回答: "C. $113,733"  ✅

  修復結果: 成功 ✅
  原因: 計算器精確計算了 (1.0175)^24 = 1.5164，消除了 LLM 的算術誤差
```

---

#### 錯誤類型 3：Misapplication

```
CFA 題目：
  「計算面額 $1,000、票面利率 8%、20 年期、YTM 9% 的債券的 Modified Duration。
   已知 Macaulay Duration = 10.2 年。」
  A. 9.36 年
  B. 10.20 年
  C. 11.12 年
  正確答案：A

模型（Qwen3-32B）回答：B. 10.20 年  ❌

═══ E1 的診斷 ═══

  Reasoning trace:
    "Modified Duration measures price sensitivity to yield changes.
     The question gives Macaulay Duration = 10.2 years.
     Modified Duration... is approximately equal to Macaulay Duration
     for most bonds. Therefore, Modified Duration ≈ 10.2 years."

  GPT-4o 分類:
    Dimension 1: Misapplication → Concept Confusion
      理由: 模型知道 Macaulay Duration，但把它跟 Modified Duration 混淆。
            正確轉換公式: ModD = MacD / (1 + y/k)
            = 10.2 / (1 + 0.09/2) = 10.2 / 1.045 = 9.76... 取近似 = 9.36
            模型知道相關概念但用錯了轉換方式。
    Dimension 2: Fixed Income
    Dimension 3: Stage 2 — Formula Recall
      理由: 錯在公式選擇階段——直接用了 MacD 而不是 MacD/(1+y/k)

  分類標籤: [Misapplication / Fixed Income / Stage 2]

═══ E2 的修復 ═══

  錯誤類型: Misapplication → 修復策略: Few-shot Demonstration

  注入 3 個同類題的正確示範:
    Example 1: "MacD=8.5, YTM=6%, semi-annual → ModD = 8.5/1.03 = 8.25"
    Example 2: "MacD=12.0, YTM=10%, annual → ModD = 12.0/1.10 = 10.91"
    Example 3: "MacD=6.8, YTM=8%, quarterly → ModD = 6.8/1.02 = 6.67"

  模型看到示範後重新回答:
    "ModD = MacD / (1 + y/k) = 10.2 / (1 + 0.09/2) = 10.2 / 1.045 = 9.76
     最接近 A. 9.36"
     （精確計算差異來自半年複利的處理方式，但方向正確，選 A）

  修復結果: 成功 ✅
  原因: Few-shot 示範讓模型「看到」正確的轉換公式用法，修正了概念混淆
```

---

#### 錯誤類型 4：Distractor Confusion

```
CFA 題目：
  「Ruth McDougal, CFA，在研討會上無意聽到 Randolph 公司臨床試驗結果
   令人失望（尚未公開）。她隨即將 Randolph 的評級從「買入」改為「賣出」。
   她是否違反 CFA 準則？」
  A. 否
  B. 是，因為她沒有披露部分分析是基於意見
  C. 是，因為她的推薦缺乏合理基礎
  正確答案：C

模型（Llama-3.1-8B）回答：A. 否  ❌

═══ E1 的診斷 ═══

  Reasoning trace:
    "McDougal did not actively seek out insider information.
     She overheard it accidentally at a conference, which is a public setting.
     Since she did not intentionally obtain MNPI, she is not in violation."

  GPT-4o 分類:
    Dimension 1: Distractor Confusion → Partial Truth
      理由: 選項 A 有部分道理（偶然聽到 ≠ 故意竊取），模型被這個部分正確性吸引。
            但真正的違規點不在於資訊來源方式，而在於她基於單一未經驗證的資訊源
            就改變推薦 = 缺乏 reasonable basis (Standard V(A))。
    Dimension 2: Ethics
    Dimension 3: Stage 1 — Concept Identification
      理由: 模型把問題的焦點錯誤地鎖定在「MNPI 的獲取方式」上，
            而不是「推薦的合理基礎」。概念辨識階段就走偏了。

  分類標籤: [Distractor Confusion / Ethics / Stage 1]

═══ E2 的修復 ═══

  錯誤類型: Distractor Confusion → 修復策略: Option-by-option Analysis

  Prompt: "請逐一分析每個選項的正確性和錯誤原因"

  模型逐項分析:
    A. 否 — 偶然聽到確實不算故意竊取，但這不是問題的重點。
       問題不在於「資訊來源是否合法」，而在於「推薦是否有合理基礎」。
       基於單一、未經公開驗證的消息就改評級，不管消息來源為何，
       都缺乏 reasonable basis。→ 此選項過度簡化了問題 ❌

    B. 是，因為沒有區分意見和事實 — Standard V(B) 確實要求區分，
       但這裡的問題不是「沒區分意見和事實」，而是推薦本身缺乏基礎。
       → 搞錯了違反的準則 ❌

    C. 是，因為推薦缺乏合理基礎 — Standard V(A) 要求分析師的推薦
       必須有 diligent and reasonable basis。基於一個未經驗證的消息
       就直接改評級，不符合 reasonable basis 的標準。→ 正確 ✅

  修復後回答: "C. 推薦缺乏合理基礎"  ✅

  修復結果: 成功 ✅（但這是最不穩定的修復——換個類似題目可能又錯）
```

---

### E1 的核心產出：三維 Error Atlas（預期結果）

```
═══ 維度 1 × 2：Error Type × CFA Topic 熱力圖 ═══

                   Knowledge  Misapply  Calc Error  Distractor
                   Gap        ation     (算術)      Confusion
────────────────────────────────────────────────────────────
Ethics              15%         5%         0%         80%   ← 幾乎全是 Distractor
Quantitative         5%        10%        75%         10%   ← 幾乎全是計算錯
Fixed Income        20%        25%        40%         15%   ← 混合型
Derivatives         25%        30%        30%         15%   ← 混合型，Misapply 高
Equity              30%        15%        10%         45%   ← Knowledge Gap + Distractor
Economics           35%        20%         5%         40%
Corporate Finance   25%        20%        15%         40%
Portfolio Mgmt      20%        15%         5%         60%   ← Distractor 多（整合判斷）
Alternative Inv     40%        10%         5%         45%   ← Knowledge Gap 最高
Financial Report    30%        25%        20%         25%

閱讀方式：
- Ethics 行的 Distractor Confusion 80% → 倫理題答錯主要因為被干擾項誤導
- Quantitative 行的 Calc Error 75% → 量化題答錯主要因為計算不準
- Alternative Inv 的 Knowledge Gap 40% → 另類投資的知識缺口最大

（以上為預期分布，實際數字待實驗驗證）
```

```
═══ 維度 1 × 3：Error Type × Cognitive Stage 交叉 ═══

                   Stage 1    Stage 2    Stage 3    Stage 4    Stage 5
                   概念辨識   公式回想   數值提取   計算執行   驗證
──────────────────────────────────────────────────────────────
Knowledge Gap       70%        20%         5%         0%         5%
Misapplication      15%        65%        10%         5%         5%
Calculation Error    0%         0%        10%        85%         5%
Distractor Confuse  60%         5%         5%         0%        30%

閱讀方式：
- Knowledge Gap 70% 在 Stage 1 → 知識缺口問題在最開始就發生（不認識概念）
- Calculation Error 85% 在 Stage 4 → 計算錯誤集中在計算步驟（符合直覺）
- Distractor Confusion 60% 在 Stage 1 + 30% 在 Stage 5
  → 被誤導要麼在讀題時就被帶偏（Stage 1），要麼在最後驗證時猶豫改答案（Stage 5）
```

---

### E2 的核心產出：修復效果矩陣（預期結果）

```
═══ Targeted vs Blanket 的修復率比較 ═══

                     Blanket    Blanket    Targeted
                     CoT        RAG        (對症下藥)
────────────────────────────────────────────────────
Knowledge Gap         25%        75%        75%     ← RAG 本來就是對的策略
Calculation Error     15%        10%        85%     ← 只有 Calculator 有效
Misapplication        40%        30%        60%     ← Few-shot 比 CoT 好
Distractor Confusion  35%        20%        45%     ← 最頑固，逐項分析稍有幫助
────────────────────────────────────────────────────
整體 Fix Rate         30%        35%        65%     ← Targeted 幾乎翻倍

解讀：
- Blanket CoT 對 Misapplication 有點用（40%），因為 CoT 本身鼓勵步步推理
- Blanket RAG 對 Calculation Error 幾乎無效（10%），因為找到公式也不能幫你算準
- Targeted 的優勢主要來自 Calculation Error（85% vs 10-15%）和 Knowledge Gap（75% vs 25%）

（以上為預期結果，實際數字待實驗驗證）
```

```
═══ Cascaded Remediation Pipeline ═══

在固定預算下的修復策略：

Stage 1（低成本）：Option-by-option Analysis
  → 修復掉一批 Distractor Confusion 的簡單案例
  → 每題成本：~1 次 API call

Stage 2（中成本）：Few-shot Demonstration
  → 修復掉 Misapplication 案例
  → 每題成本：~1 次 API call（但 prompt 更長）

Stage 3（高成本）：RAG + Calculator
  → 修復 Knowledge Gap 和 Calculation Error
  → 每題成本：~3-5 次 API call（RAG 檢索 + tool calling）

結果：
  在 $50 預算下：
    單用最佳策略（RAG）：修復 35% 的錯誤
    Cascaded Pipeline：修復 55% 的錯誤（+57% 提升）
  原因：便宜的策略先處理容易修的錯，省下預算給難修的錯用重砲
```

---

### E1 vs E2 比較表

| | E1 錯誤模式圖譜 | E2 對症修復策略 |
|--|---------------|--------------|
| **一句話** | 建一張錯誤地圖 | 不同的錯用不同的修法 |
| **對應 docs/03** | 方向 6 前半 | 方向 6 後半 |
| **性質** | 診斷（classification） | 治療（remediation） |
| **核心產出** | 三維 Error Atlas + heat maps | Fix Rate matrix + Cascaded Pipeline |
| **依賴關係** | 需 B1 的 5-Stage 框架、大量模型推論 | 硬性依賴 E1 的分類結果 |
| **最大瓶頸** | 200 題人工標註（30-40hr） | Financial Calculator 開發（30-40hr）+ Few-shot bank 建構（15-20hr） |
| **模型需求** | 6+ 被測模型 + GPT-4o 分類器 | 4+ 被測模型 + RAG + Calculator |
| **獨立成論文？** | ✅ 可以（data/resource paper） | ⚠️ 偏薄，建議與 E1 合併 |
| **最有趣的預期發現** | Ethics 的錯誤 80% 是 Distractor Confusion | Distractor Confusion 是最頑固的錯誤（Fix Rate 最低） |
| **目標場所** | ACL/EMNLP 2026 | 同左（與 E1 合併） |

---

### E1+E2 的合併論文建議

```
論文結構（一篇完整的「診斷—治療」論文）：

1. Introduction：金融 AI 的錯誤不是同質的
2. Related Work：Error analysis in NLP + Financial AI evaluation

3. Part I — 診斷（E1）
   3.1 Error Taxonomy 定義（4 類 12 子類 + CFA Topic + Cognitive Stage）
   3.2 Automatic Error Classifier（GPT-4o）的設計與驗證
   3.3 Error Atlas 視覺化（核心 heat maps）
   3.4 跨模型錯誤遷移分析

4. Part II — 治療（E2）
   4.1 四種 Targeted Remediation Strategies 設計
   4.2 Targeted vs Blanket 比較（核心實驗）
   4.3 Cascaded Remediation Pipeline
   4.4 修復策略的跨模型通用性

5. Discussion
   → 哪些錯誤最容易修（Knowledge Gap）、哪些最頑固（Distractor Confusion）
   → 對 AI 金融應用的實務建議

6. Conclusion
```

這樣一篇論文涵蓋「發現問題 + 解決問題」的完整閉環，比單獨的 E1 或 E2 都更有份量。

---

### 跟其他研究的連結

```
E1 使用 B1 的 5-Stage → 如果 B1 先完成，E1 的 Dimension 3 就有現成的框架
E2 使用 B6 的 Calculator → experiments/cfa_agent/tools.py 裡已有 5 個金融計算器
E1 可用 G4 的 Level 標籤進一步分層 → Level 2 題的錯誤以 Calculation Error 為主
B7 影響 E1 的可信度 → 如果 CoT 不忠實，reasoning trace 的錯誤歸因可能不準

在論文拆分計劃中：
  Paper 2 = B1 + B6 + E1 + E2（管道 + 計算器 + 錯誤圖譜 + 修復）
  四者形成完整的故事：
    B1 拆開推理過程 → E1 定位錯誤 → E2 對症修復 → B6 提供計算工具
```

---

### docs/03 方向 6 vs E1+E2 的差異（需要注意的）

| 項目 | docs/03 方向 6 規劃 | E1+E2 實際寫的 |
|------|-------------------|--------------|
| Error Taxonomy | 4 大類 | 4 大類 12 子類（更細） |
| Dimension 3 | 與方向 1 的認知階段連結 | ✅ 直接用 B1 的 5-Stage |
| 修復策略 | RAG + Calculator + Few-shot + 逐項分析 | ✅ 完全對應 |
| Cascaded Pipeline | docs/03 有提到 | E2 有完整設計 ✅ |
| 缺少 | — | ⚠️ E1 沒提到 FinDAP 模型（Llama-Fin-8b）的錯誤分析 |
| 缺少 | — | ⚠️ E2 沒有分析「修復失敗」的案例（修了還是錯的那些題，為什麼？） |
| 缺少 | — | ⚠️ E2 的 Few-shot bank 建構（15-20hr）可能需要 CFA 專業知識來挑選好的示範案例 |

**需要補的**：
1. 加入 Llama-Fin-8b → 看 FinDAP 訓練是否改變了錯誤分布（比如 Knowledge Gap 是否減少了？）
2. E2 應增加「修復失敗分析」章節：逐項分析了但還是答錯的 Distractor Confusion 案例，為什麼？這些才是真正的「AI 能力邊界」。
3. 人工標註 200 題（E1）和 Few-shot bank 建構（E2）都需要有 CFA 知識的人力 → 可考慮用 GPT-4o 初篩 + 人工驗證來降低工作量。

---

# ═══════════════════════════════════════════
# 研究方向與論文對應
# ═══════════════════════════════════════════

## 各方向的依賴關係（哪個先做）

```
最先做（不需要 GPU，馬上能開始）：
  ├── D1（校準）          ← 純統計分析
  ├── G4（認知分類）      ← 很多下游研究依賴它
  ├── C1（RAG 比較）      ← 程式碼已經寫好了
  └── A5（選項偏差）      ← 最簡單的實驗之一

第二波：
  ├── B1+B6（管道+計算器） ← 第二做
  ├── E1（錯誤圖譜）       ← 與 B1 共用推論結果
  └── A1（開放式基準）     ← 需要建構 Gold Answer Set

第三波：
  ├── D3+D5（棄權+偏移）   ← 在 D1 之後
  ├── E2+E3（修復+自診斷） ← 在 E1 之後
  └── C2（知識圖譜 RAG）   ← 在 C1 之後

第四波（需要更多資源）：
  ├── B5（雙系統整合）      ← 需要前面的 B1+B4+B6 基礎
  ├── F1（需要 GPU 跑 Llama-Fin-8b）
  └── H1+H3（多模態+申論）  ← 需要新的題目建構

最後（匯整型）：
  ├── G1（能力矩陣）       ← 匯整所有結果
  ├── G2（訊號理論）       ← 基於 G1
  └── G3（考試改革）       ← 基於 G1+G2
```

---

## 論文拆分建議（4-5 篇）

```
Paper 1 — 「金融 LLM 的信心校準與選擇性預測」
  核心：D1 + D3 + D5
  搭配：D2 精華 + D4 精華
  定位：ACL/EMNLP 2026
  預估：最先完成

Paper 2 — 「結構化金融推理管道與工具增強」
  核心：B1 + B6
  搭配：E1 錯誤圖譜 + E2 對症修復
  定位：ACL/EMNLP 2026 或 AAAI 2027

Paper 3 — 「金融 AI 的評估與基準建構」
  核心：A1/A1a/A1b + A2 + G4
  搭配：A5 選項偏差 + E4 認知複雜度
  定位：NeurIPS Datasets & Benchmarks

Paper 4 — 「知識圖譜 RAG 與自適應檢索」
  核心：C1 + C2 + C3
  搭配：B5 雙系統（RAG 部分）+ H2 時效性
  定位：ACL/EMNLP 或 SIGIR

Paper 5 — 「AI 時代的專業認證：能力矩陣與訊號理論」
  核心：G1 + G2 + G3
  搭配：H3 申論題 + A3 跨基準分析
  定位：Management Science 或 Journal of Finance
```

---

## docs/03 方向 2 vs D1 的差異（需要注意的）

| 項目 | docs/03 方向 2 規劃 | D1 實際寫的 |
|------|--------------------|-----------|
| 模型 | GPT-4o, Claude Opus, Gemini 2.5 Pro, Llama-Fin-8b | gpt-4o-mini, qwen3:32b, llama3.1:8b, deepseek-r1:14b |
| 缺少 | — | ⚠️ 沒有 Llama-3-8B vs Llama-Fin-8b 的訓練前後比較 |
| 缺少 | — | ⚠️ 沒有 FinDAP 訓練對 calibration 的影響分析 |
| 主題標註 | 需要 10-15 小時人工校驗 | 標為待做 |

**Llama-3-8B vs Llama-Fin-8b 的比較是審稿人會問的**：FinDAP 的 domain adaptation 有沒有讓 calibration 變好或變差？這是跟 FinDAP（EMNLP 2025）直接對話的實驗，加上去會讓論文更有份量。

---

## 什麼能看、什麼不能看

| 東西 | 狀態 | 能不能看 |
|------|------|---------|
| `docs/01-05` 五份研究文件 | 完成 | 能看，是所有決策依據 |
| `drafts/ideas/` 41 份提案 | 完成 | 能看，但都是規劃，還沒執行 |
| `experiments/RAG/` | 有程式碼 | 能看，目前唯一的實作 |
| `datasets/FinDap/FinDAP/` | Salesforce 原始碼 | 能看，別人的訓練框架 |
| `datasets/FinEval/`, `FinTrain/` | 資料集 | 有 metadata，大檔被 gitignore |
| `archive/` | 舊文件 | 不用看，已被 docs/ 取代 |
| `reference/` | 自動生成 | 參考用，不核心 |

---

## 資料集速查

| 資料集 | 題數 | 用途 | 能用？ |
|--------|------|------|--------|
| CFA-Challenge | 90 | 評估（難題） | ✅ 有論文背書 |
| CFA-Easy | 1,032 | 評估（基礎） | ✅ 有論文背書 |
| CRA-Bigdata | 1,472 | 評估（股價預測） | ✅ 但不是 CFA 題型 |
| cfa_exercise | 2,946 | 訓練（Level II） | ✅ 最有價值，含答案解析 |
| CFA_Extracted-sft | 2,946 | 訓練（SFT 格式） | ✅ cfa_exercise 的對話格式版 |
| CFA_Extracted-chunk_0 | 1,124 | 訓練（含教材原文） | ✅ RAG 研究特別有用 |
| book_fineweb | 4,500 | 訓練（CPT 無監督） | ✅ 用於 Stage 1 |
| apex_instruct | 1.4M | 訓練（通用指令） | ✅ 防止 catastrophic forgetting |
| CFA_Level_III | 90 | 評估 | ⚠️ 無論文背書，只有選擇題沒申論 |
| flare-cfa | 1,032 | — | ❌ 與 CFA-Easy 重複，禁止使用 |

---

## 41 個研究點子完整索引

### A 系列 — 評估方法 (Evaluation)
| 編號 | 名稱 | 一句話 |
|------|------|--------|
| A1 | 開放式數值推理基準 | 拿掉選項，測 AI 的真實計算力 |
| A1a | 基準建構 | 建立容忍誤差的 Gold Answer Set |
| A1b | 錯誤歸因分類 | 答錯時是公式錯、數字錯、還是計算錯？ |
| A2 | 四層級評估框架 | 分開測模型能力和工具加成 |
| A3 | CFA 作為 AGI 基準 | CFA 能測到其他基準測不到的什麼？ |
| A4 | Prompt 敏感度 | 換問法還穩不穩定 = 真的會 or 靠猜 |
| A5 | MCQ 選項偏差 | 量化「有選項」vs「沒選項」的差距 |

### B 系列 — 推理策略 (Reasoning)
| 編號 | 名稱 | 一句話 |
|------|------|--------|
| B1 | 五階段推理管道 | 解題過程拆成 5 步，每步分開評分 |
| B2a | 雙代理系統 | 知識代理 + 計算代理，各司其職 |
| B2b | 四代理系統 | +倫理代理 +驗證代理，Shapley 分析貢獻 |
| B3 | 自我驗證 | 讓 AI 回頭檢查自己的答案 |
| B4 | 自一致性投票 | 同題問 10 次，看答案最集中在哪 |
| B5 | 雙系統推理 | 簡單題快答，難題深入分析 |
| B6 | 金融計算器 | 給 AI 一台 HP-12C |
| B7 | CoT 忠實度 | AI 的推理過程是真推理還是事後編理由？ |
| B8 | 矛盾證據推理 ⭐ | 證據互相矛盾時 AI 怎麼處理？ |

### C 系列 — RAG 檢索增強
| 編號 | 名稱 | 一句話 |
|------|------|--------|
| C1 | 四種 RAG 比較 | 同一套題，四種查資料方法比高下 |
| C2 | 知識圖譜 RAG | 搜概念關係鏈，不只搜相似文字 |
| C3 | 參數化 vs 檢索 | 哪些主題需要 RAG、哪些不用？ |
| C4 | 本地 vs 雲端 | 換成本地模型省多少錢、掉多少分？ |

### D 系列 — 信心與校準
| 編號 | 名稱 | 一句話 |
|------|------|--------|
| D1 | 信心校準 | AI 說「90% 確定」能信嗎？ |
| D2 | 跨模型共識 | 8 個 AI 投票比 1 個 AI 自評更準 |
| D3 | 棄權機制 | 不確定就說「我不知道」 |
| D4 | 過度自信風險 | 自信但答錯在金融場景多危險 |
| D5 | 分佈偏移穩定性 ⭐ | 換個場景，校準結果還靠譜嗎？ |

### E 系列 — 錯誤分析
| 編號 | 名稱 | 一句話 |
|------|------|--------|
| E1 | 錯誤模式圖譜 | 所有錯誤的分類地圖 |
| E2 | 對症修復 | 不同錯用不同修法 |
| E3 | 自我診斷 | AI 能判斷自己錯在哪嗎？ |
| E4 | 認知複雜度指數 | 量化每題有多難，預測 AI 會不會錯 |

### F 系列 — 規模與實務
| 編號 | 名稱 | 一句話 |
|------|------|--------|
| F1 | 領域 vs 通用 | 金融特化模型在哪些主題真的有用？ |
| F2 | Scaling Law | 模型越大，CFA 成績越好嗎？ |
| F3 | 成本-準確率 Pareto | 給你 $100 預算怎麼配？ |
| F4 | 角色扮演 Prompt | 扮教授答得比扮學生好？ |
| F5 | 中英文比較 | 翻成中文會掉多少分？ |

### G 系列 — 評估理論
| 編號 | 名稱 | 一句話 |
|------|------|--------|
| G1 | 能力矩陣 | 整個博士論文的核心大表 |
| G2 | 訊號理論 | AI 時代 CFA 證照還能發什麼信號？ |
| G3 | 抗 AI 考試 | 未來 CFA 該怎麼考？ |
| G4 | 認知需求分類 | 每道題按思考深度分 5 級 |

### H 系列 — 跨界延伸 ⭐新增
| 編號 | 名稱 | 一句話 |
|------|------|--------|
| H1 | 多模態推理 ⭐ | AI 看得懂 CFA 的圖表嗎？ |
| H2 | 時效性衰退 ⭐ | AI 的金融知識過期了嗎？ |
| H3 | 申論題評估 ⭐ | AI 能寫 CFA Level III 的申論嗎？ |

---

# ═══════════════════════════════════════════
# 實驗紀錄：CFA Multi-Turn Agent
# （方向 5 金融計算器 + 方向 7 雙系統的初步實作）
# ═══════════════════════════════════════════

> 位置：`experiments/cfa_agent/`
> 建立時間：2026-02-01
> 對應研究方向：方向 5（金融計算器工具）+ 方向 7（雙系統推理）

## 這個實驗在做什麼

建了一個用 OpenAI function calling 的多輪推理 agent，讓 LLM 在回答 CFA 考題時可以呼叫金融計算器工具。然後拿它跟「不用工具的 LLM」做比較，看工具到底有沒有幫助。

核心問題：**給 LLM 配金融計算器，CFA 考題準確率會提升嗎？**

## 檔案結構

```
experiments/cfa_agent/
├── __init__.py
├── tools.py       # 5 個金融計算器 + OpenAI tool schema
├── agent.py       # 3 種答題方法：zero_shot、cot、agent（+ 2 個 extra）
├── evaluate.py    # 主程式：載資料、跑方法、輸出比較表
└── results/       # 每次跑的 JSON 結果（自動產生）
```

## 動用到什麼

1. **OpenAI API**（gpt-4o-mini，`$0.15/1M input tokens, $0.60/1M output tokens`）
   - 透過 `openai` Python 套件呼叫
   - 需要 `.env` 裡設定 `OPENAI_API_KEY`
2. **5 個金融計算工具**（純 Python 實作，不靠外部金融套件）：
   - `tvm_calculator` — 時間價值：PV/FV/PMT/N/rate 互解，支援 6 種複利
   - `bond_calculator` — 債券：price、YTM、duration、convexity、price_change、excess_return
   - `statistics_calculator` — 統計/投組：加權報酬、portfolio risk、Sharpe、utility、covariance
   - `economics_calculator` — 經濟：Taylor rule、risk premium buildup、CAPM、Fisher effect
   - `general_math` — 安全的 `eval()`，只允許 `math` 模組函數
3. **CFA 考題資料集**（已在 `datasets/FinEval/` 裡）：
   - `CFA_Challenge/data.json` — 90 題，schema: `{query, answer, source}`
   - `CFA_Easy/data.json` — 1,032 題，schema: `{query, answer, text, choices, gold}`
4. **其他依賴**：`tqdm`（進度條）、`python-dotenv`（讀 .env）

## 三種方法的原理

| 方法 | 怎麼做 | API 呼叫次數 | 特色 |
|------|--------|-------------|------|
| `zero_shot` | 丟題目，system prompt 說「只回答 A/B/C」 | 1 次 | 最便宜最快，baseline |
| `cot` | 丟題目，system prompt 給 5 步驟框架（辨識概念→回想公式→提取數據→計算→驗證） | 1 次 | Chain-of-Thought |
| `agent` | 多輪對話 + OpenAI function calling，模型自己決定要不要用工具，最多 8 輪 | 1-8 次 | 核心實驗 |

另外還有 2 個 extra 方法（CLI `--methods` 可選）：
- `agent_verify` — Agent 答完後再跑一次驗證 pass（B3 自我驗證）
- `dual_process` — 用 regex 判斷計算題→Agent，概念題→CoT（B5 雙系統路由）

**Agent 的運作流程**：

```
User → 丟 CFA 題目
       ↓
Turn 1: 模型讀題，判斷需不需要計算
       ├─ 需要 → 呼叫 bond_calculator(calculate="price", face=1000, ...)
       │         ↓
       │         工具回傳 {result: 929.76, formula: "P=...", steps: [...]}
       │         ↓
       │         模型讀結果，可能再呼叫其他工具
       └─ 不需要 → 直接推理
       ↓
Turn N: 模型給出 "ANSWER: B"
       ↓
程式用 regex 提取答案字母 → 和正確答案比對
```

**答案提取**用一條 5 步 regex chain：
`ANSWER: X` → `The answer is X` → `correct answer is X` → 結尾獨立字母 → 第一個獨立 A/B/C

## 怎麼跑

```bash
# 前提：pip install openai tqdm python-dotenv
# 前提：.env 裡要有 OPENAI_API_KEY

# 快速測試：5 題 × 3 方法
python experiments/cfa_agent/evaluate.py --dataset challenge --limit 5

# 只跑 agent
python experiments/cfa_agent/evaluate.py --dataset challenge --limit 5 --methods agent

# 完整 90 題
python experiments/cfa_agent/evaluate.py --dataset challenge

# Easy 題庫
python experiments/cfa_agent/evaluate.py --dataset easy --limit 50

# 指定模型
python experiments/cfa_agent/evaluate.py --dataset challenge --model gpt-4o
```

輸出自動存到 `experiments/cfa_agent/results/`（JSON），同時 terminal 印比較表。

---

## 實驗 1：tool_choice="auto"（5 題 pilot）

`tool_choice="auto"` 是 OpenAI 的預設行為：**模型自己決定要不要呼叫工具**。

```
Method               | Accuracy | Avg Tokens | Avg Turns | Tool Calls |     Cost
--------------------------------------------------------------------------------
zero_shot            |   40.0% |        715 |       1.0 |          0 | $  0.00
cot                  |   40.0% |      1,162 |       1.0 |          0 | $  0.00
agent                |   40.0% |      2,139 |       1.0 |          0 | $  0.00
```

**發現**：agent 一次工具都沒呼叫。gpt-4o-mini 在 `auto` 下寧可自己心算也不呼叫工具。

---

## 實驗 2：tool_choice="required"（5 題 pilot）

把 `agent.py` 裡的 `tool_choice` 改成第一輪 `"required"`（強制呼叫），後續輪切回 `"auto"`。

```
Method               | Accuracy | Avg Tokens | Avg Turns | Tool Calls |     Cost
--------------------------------------------------------------------------------
agent                |   20.0% |      4,085 |       2.0 |          9 | $  0.00
```

**發現：工具被呼叫了（9 次），但準確率反而從 40% 掉到 20%**。

工具呼叫細節：
```
[X] Q0（倫理題）→ general_math("11/100") → 0.11    ← 無意義
[X] Q1（倫理題）→ general_math("(1.05**10 - 1) / 0.05")  ← 無意義
[X] Q2（倫理題）→ general_math("(15/100) * 100")   ← 無意義
[X] Q3（倫理題）→ general_math("15/100")            ← 無意義
[O] Q4（固收題）→ bond_calculator(duration) → Error: YTM=0  ← 忘記傳 YTM
```

**結論**：`required` 不適合混合題型。倫理題被迫用工具反而干擾推理。已改回 `auto`。

---

## 實驗 3：完整 90 題 CFA Challenge（正式結果）

用 `tool_choice="auto"` 跑完全部 90 題。

### 主要結果

```
Method               | Accuracy | Avg Tokens | Avg Turns | Tool Calls |     Cost
--------------------------------------------------------------------------------
zero_shot            |   42.2% |        772 |       1.0 |          0 | $  0.01
cot                  |   53.3% |      1,282 |       1.0 |          0 | $  0.04
agent                |   51.1% |      3,033 |       1.2 |         20 | $  0.06
```

### 核心發現

**1. CoT > Agent > Zero-shot**

- CoT 比 zero_shot 提升 +11.1%（42.2% → 53.3%）：Chain-of-Thought prompting 有效
- Agent 比 zero_shot 提升 +8.9%（42.2% → 51.1%）：但略低於 CoT
- Agent 比 CoT **低** 2.2%（51.1% vs 53.3%）：agent 框架的 overhead 反而拖累了表現

**2. Agent 幾乎沒用工具**

- 90 題裡只有 8 題（8.9%）使用了工具，共 20 次呼叫
- 只呼叫了 `general_math`，**完全沒有使用金融專用工具**（bond_calculator 等）
- 有用工具的 8 題準確率只有 25%（2/8），比沒用工具的 53.7%（44/82）更差

**3. 需要多輪的只有 8 題**

- 82/90 題 agent 只跑了 1 turn（等於退化成 cot）
- 8 題跑了多輪（平均 3.4 turns），都是用了工具的那 8 題

**4. Agent vs Zero-shot 的逐題比較**

- Agent 對了但 zero_shot 錯了：18 題（agent 的優勢來自 CoT 推理，不是工具）
- Zero_shot 對了但 agent 錯了：10 題（agent 偶爾過度推理反而答錯）
- 淨增益：+8 題

### 花費

全部 90 題 × 3 方法，total wall time 1,844 秒（~31 分鐘），API 費用 $0.07。

### 結果檔案位置

- `experiments/cfa_agent/results/eval_challenge_20260201_204154.json`（5 題 pilot，auto）
- `experiments/cfa_agent/results/eval_challenge_required_5q.json`（5 題 pilot，required）
- `experiments/cfa_agent/results/eval_challenge_20260202_020114.json`（90 題完整，auto）

---

## 分析：為什麼工具沒有幫助

### 原因 1：CFA Challenge 以概念題為主

前 20 題幾乎全是倫理/概念題，不需要計算。這些題佔大多數，稀釋了工具的潛在效果。

### 原因 2：gpt-4o-mini 不願使用工具

`tool_choice="auto"` 下，模型有工具可用但寧可自己心算。這是 gpt-4o-mini 的行為特性——它可能認為自己的計算能力足夠（即使事實上不是）。

### 原因 3：工具只被用在不適合的場景

8 題使用工具裡，全部只呼叫了 `general_math`（簡單算術），沒有呼叫任何金融專用工具。模型不知道怎麼用 `bond_calculator` 或 `statistics_calculator`。

### 對研究方向的啟示

這個結果本身就是一個有意義的 negative finding：
- **「給 LLM 工具 ≠ LLM 會用工具」** — 光把工具掛上去不夠，需要更強的引導
- 支持 docs/03 方向 5 裡的三方比較設計：Pure LLM vs Generic Calculator vs Domain-specific Calculator
- 也支持方向 7（雙系統）的必要性：需要先分類問題，再決定策略

---

## 下一步可能的改進

- **更好的 prompting**：在 system prompt 強調「計算題務必使用金融工具」，並加 few-shot 示範
- **用 gpt-4o**：更大的模型可能更願意使用工具
- **跑 CFA_Easy**：1,032 題裡有更多計算題，可能看到不同的 pattern
- **dual_process 路由**：程式先判斷計算/概念，計算題才開 agent（已實作 `run_dual_process()`）
- **修 bug**：`bond_calculator(calculate="duration")` 在沒傳 `ytm` 時應 fallback 而不是 error
