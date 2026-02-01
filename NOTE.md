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

## 研究方向 1：五階段推理管道

### 這在解決什麼

現在的做法只知道「模型答錯了」，但不知道錯在哪一步。

### 真實題目範例

**CFA 題目**：

> 三年期、4% 年付息、面額 $1,000 的債券，即期利率為 S₁=5%, S₂=6%, S₃=7%。
> 計算債券價格與到期收益率 (YTM)。
> A. $912.41, 6.82%
> B. $922.64, 6.94%
> C. $931.05, 7.12%

**BEFORE — 現在的 LLM 做法（直接回答）**：

```
Input:  上面的題目
Process: LLM 內部黑箱推理，一口氣生成答案
Output:  "答案是 C. $931.05"  ← 答錯了，但不知道為什麼
```

模型可能在某一步出錯，但我們看不見：
- 是不認識 spot rate 這個概念？
- 是忘記折現公式？
- 是從題幹提取數字搞混了？
- 是計算 40/1.06² 算錯了？
- 還是算出來了但沒驗證合理性？

**AFTER — 五階段管道**：

```
Stage 1 — 概念辨識
  Input:  題目全文
  Output: [Spot Rate, Bond Pricing, Yield to Maturity, Discount Factor]
  評估:   ✅ 正確辨識了所有概念

Stage 2 — 公式回想
  Input:  上述概念
  Output: Price = Σ CF_t / (1 + S_t)^t ; YTM 使用 trial-and-error 或數值法
  評估:   ✅ 公式正確

Stage 3 — 數字提取
  Input:  題幹文本
  Output: { coupon: 40, face: 1000, S1: 0.05, S2: 0.06, S3: 0.07, years: 3 }
  評估:   ✅ 提取正確

Stage 4 — 計算執行
  Input:  公式 + 數字
  Output: 40/1.05 + 40/1.06² + 1040/1.07³ = 38.10 + 35.60 + 849.02 = $922.72
  評估:   ⚠️ 計算有微小誤差（正確答案 $922.64），849.02 應為 848.95
          → 錯誤定位：Stage 4 的 1040/1.07³ 計算有精度問題

Stage 5 — 合理性驗證
  Input:  計算結果 + 題目背景
  Output: "YTM > coupon rate → 價格應低於面額，$922 合理"
  評估:   ✅ 驗證邏輯正確
```

**差異**：Before 只得到「錯了」。After 精確定位到「Stage 4 計算步驟出錯」，對應的修復方式就是加計算器工具（方向 5）。

---

## 研究方向 2：校準與選擇性預測

### 這在解決什麼

模型說「我 95% 確定」的時候，真的有 95% 的機率對嗎？如果不是，能不能讓它在不確定時說「我不知道」？

### 真實題目範例

**CFA 題目**：

> 名目無風險利率 (nominal risk-free rate) 最佳描述為實質無風險利率加上什麼的溢價？
> A. 到期期限 (maturity)
> B. 流動性 (liquidity)
> C. 預期通膨 (expected inflation)

（正確答案：C）

**BEFORE — 現在的做法**：

```
Input:   題目
Process: LLM 直接回答
Output:  "C. expected inflation"  ← 對了

但我們不知道模型有多確定。它可能：
- 對 C 的信心是 92%（well-calibrated）
- 對 C 的信心是 55% 但碰巧選對了（lucky guess）
- 對 A 的信心其實是 45%，差點就答錯
```

另一題：

> 30 年期美國國債與 30 年期小型私人公司債券的殖利率差異，最相關的風險溢價是？
> A. 通膨 (Inflation)
> B. 到期 (Maturity)
> C. 流動性 (Liquidity)

（正確答案：C — 小型私人公司流動性差）

```
模型回答: "A. Inflation"  ← 錯了
模型信心: "我 88% 確定"    ← Overconfident！高信心但答錯
```

**AFTER — 校準分析 + 選擇性預測**：

```
Step 1: 收集模型對每道題的信心分數

  方法 A — Logit-based（看模型的 softmax 輸出機率）
    題目 1: P(A)=0.03, P(B)=0.05, P(C)=0.92 → 信心 92%
    題目 2: P(A)=0.41, P(B)=0.22, P(C)=0.37 → 信心 41%

  方法 B — Self-Consistency（同一題問 10 次，看答案一致性）
    題目 1: 10 次都答 C → 信心 100%
    題目 2: 4 次答 A、3 次答 C、3 次答 B → 信心 40%

  方法 C — Verbalized（直接問模型"你多確定？"）
    題目 1: "我 90% 確定" → 信心 90%
    題目 2: "我 88% 確定" → 信心 88% ← 注意：模型自稱很確定但其實在亂猜

Step 2: 繪製 Calibration 曲線

  理想情況：信心 90% 的題，正確率應該也是 90%
  實際情況（預期發現）：
    信心 90% → 實際正確率只有 72%  ← Overconfident
    信心 70% → 實際正確率 65%      ← 略微 overconfident
    信心 50% → 實際正確率 48%      ← 接近校準

  → ECE (Expected Calibration Error) = 0.12（越接近 0 越好）

Step 3: 選擇性預測（設定信心門檻）

  門檻 θ=0.80:
    只回答信心 ≥ 80% 的題（約 70% 的題）
    → 準確率從 78% 提升到 88%

  門檻 θ=0.90:
    只回答信心 ≥ 90% 的題（約 50% 的題）
    → 準確率提升到 93%

  → 畫出 Coverage-Accuracy 曲線，找到最佳平衡點
```

**差異**：Before 只知道準確率 78%。After 知道模型在 Derivatives 主題上最 overconfident（自稱 90% 確定但只有 60% 正確率），而且能透過「放棄回答不確定的題」把準確率拉到 90%+。

---

## 研究方向 3：知識圖譜 RAG (KG-RAG)

### 這在解決什麼

普通 RAG 靠語義相似度找文本，但金融概念之間有結構性的前後依賴關係，語義搜尋找不到。

### 真實題目範例

**CFA 題目**：

> 一位投資組合經理想要實施 immunization strategy 來匹配負債。
> 他的負債 duration 是 7.5 年。以下哪個 portfolio 最適合？
> A. Duration 7.5 年、全部為 non-callable bonds
> B. Duration 7.5 年、包含 callable 和 non-callable bonds
> C. Duration 8.0 年、全部為 non-callable bonds

（正確答案：A）

**BEFORE — 普通 RAG**：

```
Input:  "immunization strategy duration 匹配"
檢索:   語義相似度搜尋 → 找到一段描述 immunization 的文本片段
問題:   找到的片段只說「immunization 是一種策略」，沒有解釋
        為什麼 callable bonds 會破壞 immunization
        （因為 callable bonds 有 negative convexity，
         利率下降時 duration 會改變，打破匹配）
Output: "B. 包含 callable 和 non-callable"  ← 答錯
原因:   RAG 找到的文本不包含「callable bonds 影響 duration 穩定性」的知識
```

**AFTER — 知識圖譜 RAG**：

```
Step 1: 從題目辨識概念
  → [Immunization, Duration, Callable Bonds, Non-callable Bonds]

Step 2: 在知識圖譜中查找

  Immunization --requires--> Duration Matching
  Immunization --requires--> Convexity >= Liability Convexity
  Callable Bonds --has_property--> Negative Convexity
  Negative Convexity --conflicts_with--> Duration Stability
  Duration Stability --prerequisite--> Immunization

Step 3: 沿著圖譜走，得到子圖

  "Immunization 需要 duration 匹配 → duration 匹配需要 duration 穩定
   → callable bonds 有 negative convexity → negative convexity 會導致
   duration 不穩定 → 所以 callable bonds 會破壞 immunization"

Step 4: 把子圖轉成文本注入 LLM

  Context: "Immunization requires that portfolio duration matches
  liability duration AND remains stable. Callable bonds exhibit
  negative convexity, causing duration to change unpredictably
  when interest rates move. This instability can break the
  immunization match. Therefore, non-callable bonds are preferred."

Step 5: LLM 基於這個 context 回答
  Output: "A. Duration 7.5 年、全部為 non-callable bonds"  ← 正確
```

**差異**：普通 RAG 只找到「immunization 是什麼」，但漏掉了「callable bonds 為什麼不行」這個多跳推理鏈。KG-RAG 沿著圖譜找到 Callable → Negative Convexity → Duration Instability → Breaks Immunization 的完整推理路徑。

---

## 研究方向 4：偏好學習（推理品質 > 答案正確性）

### 這在解決什麼

現在的訓練只獎勵「答案對」，但不管推理過程。一個碰巧猜對但推理亂七八糟的回答，和一個推理嚴謹但最後算錯一步的回答，前者得到獎勵、後者被懲罰。這是反直覺的。

### 真實題目範例

**CFA 題目**：

> 2 年期固定對浮動 LIBOR swap rate 是 2.02%，2 年期美國國債殖利率是 1.61%。
> Swap spread 是多少？
> A. 41 bps
> B. 61 bps
> C. 163 bps

（正確答案：A. 41 bps）

**模型回答 — 版本 A（答對但推理差）**：

```
"Swap spread 是兩個利率的差。2.02 - 1.61 = 0.41%，也就是 41 bps。答案是 A。"
```

評分：答案 ✅ 對了，但推理只有一行，沒解釋什麼是 swap spread、為什麼要這樣算、結果代表什麼。

**模型回答 — 版本 B（答錯但推理好）**：

```
"Swap spread 衡量的是銀行間信用風險相對於政府公債的溢價。
計算方式：Swap spread = Swap rate - Treasury yield。

代入數字：
  Swap rate = 2.02%
  Treasury yield = 1.61%
  Swap spread = 2.02% - 1.61% = 0.41%

這相當於 41 basis points。正的 swap spread 表示銀行的信用風險
高於政府，這是正常現象。不過如果 swap spread 變成負值，
就暗示市場對政府信用有擔憂（如 2008 金融危機期間）。

答案是 B. 61 bps。"
```

評分：最後答案 ❌ 選錯了（可能是抄寫/輸出格式錯誤），但推理過程完整、概念正確、有金融 insight。

**BEFORE — FinDAP 的 RPO 訓練**：

```
偏好對：版本 A（答對）> 版本 B（答錯）
獎勵：版本 A 得到正向獎勵
結果：模型學到「快速給答案就好，不需要深入解釋」
```

**AFTER — 我們的多維度偏好學習**：

```
四維度評分：
  版本 A:
    Step Correctness:      5/5（計算正確）
    Logical Coherence:     2/5（只有一步，沒有邏輯鏈）
    Formula Appropriateness: 3/5（用了對的公式但沒解釋為什麼）
    Financial Depth:       1/5（沒有金融洞察）
    總分：11/20

  版本 B:
    Step Correctness:      4/5（計算正確但最後選項選錯）
    Logical Coherence:     5/5（完整的推理鏈）
    Formula Appropriateness: 5/5（解釋了公式的含義和適用場景）
    Financial Depth:       5/5（提到 negative swap spread 和 2008 危機）
    總分：19/20

偏好對（Type B 創新）：版本 B（推理好但答錯）> 版本 A（答對但推理差）
訓練結果：模型學到「要寫出完整的推理過程和金融洞察」
```

**差異**：Before 獎勵「碰巧對的淺回答」。After 獎勵「推理嚴謹的深回答」，即使答案有小瑕疵。長期來看，推理好的模型整體準確率也會更高，因為推理過程本身能幫助 self-correction。

---

## 研究方向 5：金融計算器工具

### 這在解決什麼

LLM 的數學計算是已知弱點，但 CFA 考試允許用計算器。給 LLM 一個計算器，就像給考生一個 HP-12C。

### 真實題目範例

**CFA 題目**：

> 年利率 4.00%（stated annual rate），若等效年化利率 (EAR) 為 4.08%，
> 則該銀行的計息方式為？
> A. 每日複利 (daily)
> B. 每季複利 (quarterly)
> C. 每半年複利 (semiannually)

（正確答案：A. 每日複利）

**BEFORE — 純 LLM 推理**：

```
Input:  題目
Process: LLM 心算

  "EAR = (1 + r/n)^n - 1
   如果 quarterly: EAR = (1 + 0.04/4)^4 - 1 = (1.01)^4 - 1
   (1.01)^4 = ... 嗯... 大約 1.0406
   EAR ≈ 4.06%，不等於 4.08%

   如果 daily: EAR = (1 + 0.04/365)^365 - 1
   這個... (1.0001096)^365 ≈ ... 我算不出來"

Output: "B. quarterly"  ← 答錯了
原因:  LLM 無法精確計算 (1.0001096)^365
```

**AFTER — LLM + 金融計算器**：

```
Input: 題目

Thought: "需要計算不同複利頻率下的 EAR，然後找到哪個等於 4.08%"

Action: EAR_Calculator(stated_rate=0.04, compounding="quarterly")
Observation: EAR = 4.0604%

Thought: "4.0604% ≠ 4.08%，不是 quarterly。試 daily。"

Action: EAR_Calculator(stated_rate=0.04, compounding="daily")
Observation: EAR = 4.0808%

Thought: "4.0808% ≈ 4.08%，匹配！驗證一下 semiannual。"

Action: EAR_Calculator(stated_rate=0.04, compounding="semiannually")
Observation: EAR = 4.0400%

Thought: "Semiannual 給出 4.04%，不匹配。Daily 最接近 4.08%。"

Output: "A. daily"  ← 正確
```

**另一個更複雜的例子**：

**CFA 題目**：

> 計算面額 $1,000、票面利率 6%、YTM 7%、10 年期、半年付息的債券價格。
> A. $901.23
> B. $929.76
> C. $945.82

```
BEFORE（LLM 心算）:
  "每半年付 $30，共 20 期，折現率每期 3.5%
   PV = 30 × [1-(1.035)^(-20)]/0.035 + 1000/(1.035)^20
   30 × ... 嗯... (1.035)^20 ≈ 2.0... 不，好像是 1.99...
   我不太確定..."
  Output: "C. $945.82"  ← 答錯

AFTER（LLM + Bond Calculator）:
  Thought: "半年付息債券，需要計算 PV"
  Action: BondPrice(face=1000, coupon_rate=0.06, ytm=0.07, years=10, freq=2)
  Observation: $929.76
  Thought: "YTM 7% > coupon 6%，所以折價發行，$929.76 < $1,000，合理。"
  Output: "B. $929.76"  ← 正確
```

**差異**：LLM 負責理解題意、選工具、傳參數、解讀結果；精確的數值計算交給計算器。就像真正的 CFA 考生用 HP-12C 一樣。

---

## 研究方向 6：錯誤模式挖掘與修復

### 這在解決什麼

不同的錯誤需要不同的修復方式。把所有錯誤都用同一種方法修是浪費。

### 真實題目範例

**範例 1 — Knowledge Gap（知識缺口）**：

> CFA 題目：
> 對於投資級、不可贖回、固定利率債券，spread duration 最可能接近？
> A. Modified duration
> B. Effective duration
> C. Macaulay duration
> （正確答案：A）

```
模型回答: "B. Effective duration"
推理過程: "Spread duration 衡量的是... 我不太確定 spread duration
          和 modified duration 的關係。Effective duration 似乎更通用..."

錯誤分類: Knowledge Gap → Concept Incomplete
          模型不知道「對非含權債券，spread duration ≈ modified duration」

修復策略: RAG → 檢索相關知識片段：
          "For option-free, fixed-rate bonds, spread duration is
           approximately equal to modified duration because the
           spread change affects all cash flows uniformly."

修復後重新回答: "A. Modified duration"  ← 修復成功
```

**範例 2 — Calculation Error（計算錯誤）**：

> CFA 題目：
> 今天投資 $75,000，年利率 7%、每季複利，6 年後的終值最接近？
> A. $112,555
> B. $113,330
> C. $113,733
> （正確答案：C）

```
模型回答: "A. $112,555"
推理過程: "FV = 75000 × (1 + 0.07/4)^(4×6)
          = 75000 × (1.0175)^24
          = 75000 × 1.5007 = $112,555"

錯誤分類: Calculation Error → Arithmetic Error
          (1.0175)^24 = 1.5164 不是 1.5007

修復策略: Calculator Tool →
          TVM_Calculator(PV=75000, rate=0.07, periods=6, freq=4, solve="FV")
          → FV = $113,733.21

修復後重新回答: "C. $113,733"  ← 修復成功
```

**範例 3 — Distractor Confusion（被干擾項誤導）**：

> CFA 題目：
> Ruth McDougal, CFA，受邀參加研討會，無意中聽到 Randolph 公司
> 的臨床試驗結果（尚未公開）令人失望。她隨即將 Randolph 的評級
> 從「買入」改為「賣出」。她是否違反 CFA 準則？
> A. 否
> B. 是，因為她沒有披露部分分析是基於意見
> C. 是，因為她的推薦缺乏合理基礎
> （正確答案：C）

```
模型回答: "A. 否"
推理過程: "她並非故意竊取內幕消息，只是偶然聽到的，
          所以不算違反 material nonpublic information 準則。"

錯誤分類: Distractor Confusion → Partial Truth
          選項 A 有部分道理（偶然聽到確實不算故意竊取），
          但問題不在於信息來源方式，而在於她基於非公開信息
          就改變推薦，缺乏 reasonable basis。

修復策略: Option Analysis → 逐項分析
          A: "偶然聽到"不是免死金牌，仍需要有合理基礎
          B: 這裡的問題不是沒有區分意見和事實
          C: ✅ 基於未經驗證的非公開信息做推薦 = 缺乏合理基礎

修復後重新回答: "C. 缺乏合理基礎"  ← 修復成功
```

**BEFORE vs AFTER 的差異**：

```
BEFORE — 所有錯誤都用同一種方法（例如全部用 RAG）：
  Knowledge Gap:       RAG → 有效 ✅
  Calculation Error:   RAG → 找到公式但還是算錯 ❌（需要計算器不是知識）
  Distractor Confusion: RAG → 找到一般描述但不針對選項分析 ❌
  修復成功率: ~35%

AFTER — 對症下藥：
  Knowledge Gap:       → RAG 補知識 ✅
  Calculation Error:   → Calculator Tool ✅
  Distractor Confusion: → Option-by-option Analysis ✅
  Misapplication:      → Few-shot 示範正確應用 ✅
  修復成功率: ~65%
```

---

## 研究方向 7：雙系統推理（System 1 / System 2）

### 這在解決什麼

簡單題用重砲打蚊子是浪費，難題用小槍打大象會失敗。需要自適應地分配計算資源。

### 真實題目範例

**簡單題**：

> 名目無風險利率最佳描述為實質無風險利率加上什麼的溢價？
> A. 到期期限   B. 流動性   C. 預期通膨
> （正確答案：C）

**困難題**：

> 三年期 4% 年付息 $1,000 債券，即期利率 S₁=5%, S₂=6%, S₃=7%。
> 計算價格與 YTM。

**BEFORE — 所有題都用同一流程**：

```
方案 A：全部 zero-shot → 簡單題對了 ✅，難題算錯 ❌
方案 B：全部完整管道（RAG + CoT + 計算器 + 驗證）
  → 簡單題對了 ✅ 但浪費 5 次 API call
  → 難題也對了 ✅ 但總成本超高

1000 題全部走完整管道 = 5000 次 API call = 很貴
```

**AFTER — 雙系統自適應**：

```
每道題先走 System 1（快速直覺）：

  簡單題：
    System 1: "C. expected inflation"
    信心分數: 0.95（Self-Consistency: 10/10 次都答 C）
    判斷: 0.95 ≥ 閾值 0.85 → ✅ 直接輸出，不需要 System 2
    成本: 1 次 API call

  困難題：
    System 1: "嗯... 我覺得是 B"
    信心分數: 0.52（Self-Consistency: 5 次 A、3 次 B、2 次 C）
    判斷: 0.52 < 閾值 0.85 → ⚠️ 觸發 System 2

    System 2:
      Step 1: KG-RAG 檢索 spot rate, bond pricing 知識
      Step 2: CoT 逐步推理
      Step 3: Calculator → BondPrice(...) = $922.64
      Step 4: 驗證 — YTM > coupon → 折價，合理
    輸出: "B. $922.64, 6.94%"  ← 正確
    成本: ~5 次 API call

結果:
  假設 1000 題中：
    600 題走 System 1（簡單題）= 600 次 API call
    400 題走 System 2（難題）= 2000 次 API call
    總計: 2600 次 API call

  vs 全部走 System 2 = 5000 次 API call

  準確率: 接近全部走 System 2（差距 < 2%）
  成本: 降低 ~48%
```

---

## 各方向的依賴關係（哪個先做）

```
Paper 1 → 方向 2（校準）     ← 最先做，不需要 GPU，2-3 月出結果
    ↓
Paper 2 → 方向 1+5（管道+計算器） ← 第二做
    ↓
Paper 3 → 方向 4（偏好學習）   ← 需要 GPU 訓練
    ↓
Paper 4 → 方向 3+6（KG-RAG+錯誤修復）
    ↓
Paper 5 → 方向 7（雙系統整合）  ← 最後做，整合所有前面的成果
```

---

## 什麼能看、什麼不能看

| 東西 | 狀態 | 能不能看 |
|------|------|---------|
| `docs/01-05` 五份研究文件 | 完成 | 能看，是所有決策依據 |
| `drafts/ideas/` 36 份提案 | 完成 | 能看，但都是規劃，還沒執行 |
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
