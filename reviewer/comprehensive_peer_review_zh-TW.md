# 綜合同儕審查報告（繁體中文版）
## 7 篇 LLM 金融推理論文（CFA 考試評估系列）

**審查日期：** 2026-02-10
**審查者：** Claude Opus 4.6（獨立審查代理人）
**方法論：** 交叉比對 46+ 篇同儕審查論文；驗證所有實驗數據與 JSON 結果檔案；審計共享程式碼庫之方法論品質。

---

# !! 重要：投稿策略分析與價值排序 !!

> **本節為審查者針對作者的戰略建議，置於審查報告之前。**

---

## 一、最高價值論文排序（0–100 分）

| 排名 | 論文 | 學術價值分 | 發表可行性分 | 綜合推薦分 | 理由 |
|------|------|-----------|-------------|-----------|------|
| **1** | **P7（信號理論）** | **92** | **85** | **88** | 唯一具備原創理論貢獻（Partial Signaling Collapse Theorem）的論文。將 Spence 信號模型正式擴展至 AI 時代，有「奠基性論文」(seminal paper) 潛力。引用價值最高。 |
| **2** | **P2（壓力測試）** | **85** | **82** | **82** | 實驗設計最強。GPT-5-mini 記憶落差 36.4pp 是震撼性發現。N=1,032 統計效力充足。GSM-Symbolic 範式的金融領域首次應用。 |
| **3** | **P1（選項偏差）** | **82** | **75** | **78** | 核心發現（模型依賴性偏差悖論）具高引用潛力，但評估方法不對稱是嚴重隱患。若能修復此缺陷，價值可升至 85+。 |
| **4** | **P5（錯誤圖譜）** | **78** | **78** | **76** | GCI 實驗真正新穎。「50.4% 在完美上下文下仍無法完全恢復」是重要診斷發現。但篇幅偏短、理論深度不足。 |
| **5** | **P6（校準分析）** | **72** | **65** | **68** | CaR 指標具創意（VaR → LLM 校準），但 N=90 樣本量不足以支撐結論。修復信心計算 bug 後可行性會提升。 |
| **6** | **P3（行為偏誤）** | **65** | **60** | **62** | 金融場景設計有價值，但與 LLM Economicus (COLM 2024) 重疊度最高。N=60、單模型、單評判者都是弱點。 |
| **7** | **P4（對抗倫理）** | **60** | **50** | **58** | 實驗概念新穎，但 N=47 是致命傷。零翻轉結果無法區分「真正的倫理穩健」還是「記憶導致的免疫」。 |

### 最值得發表的論文

**P7（信號理論）無疑是最值得發表的。** 理由：
1. **理論原創性最高**——其他 6 篇都是「已有範式的領域應用」，只有 P7 提出了全新的理論框架
2. **跨學科影響力**——同時觸及勞動經濟學、教育政策、AI 評估三個領域
3. **時機性極佳**——"Reasoning Models Ace the CFA Exams" (Patel et al., 2025) 剛證明 AI 能通過所有三級 CFA 考試，P7 的理論框架正好解釋「所以呢？這對證照制度意味著什麼？」
4. **政策影響力**——CFA Institute 正面臨考試形式改革壓力，P7 的建議具直接應用價值

**次優發表組合：P7 + P2 + P1**（形成「理論→實證→機制」的完整敘事鏈）

---

## 二、FRL 真的會接收這些論文嗎？

### FRL 近期接收的 AI/LLM 論文（實證）

| 論文標題 | 作者 | 年份 | 卷期 |
|---------|------|------|------|
| "ChatGPT for (Finance) research: The Bananarama Conjecture" | Dowling & Lucey | 2023 | Vol. 53 |
| "GPT has become financially literate" | Niszczota & Abbas | 2023 | Vol. 58 |
| "Can ChatGPT improve investment decisions?" | 多位作者 | 2024 | — |
| "Financial literacy of ChatGPT: Evidence through financial news" | Chiu et al. | 2025 | Vol. 78 |
| "AT-FinGPT: Financial risk prediction via audio-text LLM" | 多位作者 | 2025 | — |
| "Code like an economist: Analyzing LLMs' code generation in economics" | 多位作者 | 2025 | — |
| "Generative AI in finance: Replicability and methodological contingencies" | 多位作者 | 2025 | — |

**結論：FRL 確實在大量接收 AI/LLM 金融論文。** 2023–2025 年間有穩定的 ChatGPT/LLM 論文發表流。FRL 甚至在德累斯頓工業大學辦了 "AI in Corporate Finance" 的論文發展工作坊，顯示編輯對 AI 主題的強烈興趣。

### 但有一個致命問題：字數限制

**FRL 的嚴格字數限制是 2,500 字以下。**

| 論文 | 目前字數 | 超出比例 | 需裁減量 |
|------|---------|---------|---------|
| P1 | ~3,719 | +49% | 需裁減 ~1,200 字 |
| P2 | ~4,367 | +75% | 需裁減 ~1,800 字 |
| P3 | ~3,395 | +36% | 需裁減 ~900 字 |
| P4 | ~3,536 | +41% | 需裁減 ~1,000 字 |
| P5 | ~2,627 | +5% | 需裁減 ~130 字（最接近） |
| P6 | ~3,463 | +39% | 需裁減 ~960 字 |
| P7 | ~4,231 | +69% | 需裁減 ~1,700 字 |

**所有 7 篇都超字。** P5 最接近（僅超 5%），P2 和 P7 超出最多。這意味著：
- 如果堅持投 FRL，每篇都需要大幅刪減
- P7 需要砍掉近 40% 的內容，包括可能需要簡化數學推導
- P2 需要刪去大量實驗細節

### FRL 的審稿偏好

FRL 特別歡迎以下類型的論文：
1. 對已確立結論的**可重複性質疑**
2. 先前發現的**跨國適用性**檢驗
3. **挑戰現有方法論**的論文
4. 展示**方法論偶然性**（methodological contingency）的發現

**你的 P1（選項偏差）和 P2（壓力測試）最符合類型 1 和 3**——它們質疑「MCQ 分數 = 真實能力」這一被廣泛接受的假設。P7 符合類型 4——它展示 CFA 認證信號的條件性崩潰。

---

## 三、替代期刊策略分析

### 純財經 SCI/SSCI 期刊

| 期刊 | IF (2024) | 等級 | 適合論文 | 優缺點 |
|------|-----------|------|---------|--------|
| **Financial Analysts Journal (FAJ)** | ~2.5–3.0 | Q1/Q2 | **P1, P7** | **CFA Institute 自己的期刊！** 已發表 "How Much Does ChatGPT Know about Finance?" (Fairhurst & Greene, 2024)。你的論文直接評估 CFA 考試表現，這是最自然的學術歸屬。IF 較低但學術聲望高。 |
| **International Review of Financial Analysis (IRFA)** | 9.8 | Q1 | P2, P7 | 有 AI + Finance 專刊。接受較長論文。IF 極高。 |
| **Journal of Behavioral and Experimental Finance (JBEF)** | 5.76 | Q1 | **P3, P7** | 行為金融焦點完美匹配 P3。P7 的信號理論也涉及行為面向。 |
| **Financial Innovation** | ~6–8 | Q1 | P1, P5 | 開放取用；發表過 "Unleashing ChatGPT in finance research" (2025)。 |
| **Finance Research Letters (FRL)** | 6.9 | Q1 | P5（最接近字數）| 需大幅裁減字數。但品牌認知度高。 |

### 跨學科 SCI 期刊（AI + 金融）

| 期刊 | IF (2024) | 等級 | 適合論文 | 說明 |
|------|-----------|------|---------|------|
| **Expert Systems with Applications** | 7.5–10.5 | Q1 | P2, P5 | 更偏技術導向；接受系統性 AI 評估和基準測試。無字數限制問題。 |
| **Decision Support Systems** | ~7–8 | Q1 | P1, P6 | 不確定性下的決策支援系統。 |
| **Technological Forecasting and Social Change** | ~10–12 | Q1 | P7 | AI 對社會制度影響的分析。P7 的 AI 顛覆認證制度完美契合。 |

### Journal of Financial Education：不推薦

**Journal of Financial Education 沒有 SCI/SSCI 索引。** 僅在 ABDC（澳大利亞商學院院長委員會）有索引，屬非常低層級的分類系統。對大多數學術評鑑制度來說不算 SSCI 期刊。**不建議投稿。**

**事實上不存在同時聚焦「金融 + 教育」且有 SCI/SSCI 索引的期刊。** 最接近的可能是 Computers & Education（IF ~8.9），但那需要教育介入研究設計，你的論文不符合。

---

## 四、我的最終建議：最佳投稿組合

### 策略 A：全部投 FRL（高風險高回報）
- **優點：** 品牌一致性；7 篇形成系列；IF 6.9
- **缺點：** 所有論文需大幅裁減（25–75%）；P4、P3 可能被拒
- **預估接受率：** P7(70%), P2(65%), P1(55%), P5(60%), P6(40%), P3(35%), P4(25%)

### 策略 B：分散投稿（推薦）

| 論文 | 首選期刊 | 備選期刊 | 理由 |
|------|---------|---------|------|
| **P7** | **Financial Analysts Journal** | IRFA | CFA Institute 自家期刊；已有直接先例論文；學術聲望最高 |
| **P2** | **IRFA** | Expert Systems | IF 9.8；有 AI+Finance 專刊；可保留完整實驗細節 |
| **P1** | **FRL** 或 **Financial Innovation** | IRFA | FRL 如果能裁到 2,500 字；否則 Financial Innovation |
| **P5** | **FRL** | Expert Systems | 已最接近字數限制（2,627 字）；只需微調 |
| **P6** | **JBEF** 或 **Decision Support Systems** | FRL | CaR 指標的行為金融面向適合 JBEF |
| **P3** | **JBEF** | — | 行為偏誤主題完美匹配 |
| **P4** | **暫緩** 或擴充後投 Expert Systems | — | N=47 在任何定量期刊都很勉強；建議擴充合成數據後再投 |

### 策略 C：精選 3 篇投稿

如果資源有限，**只投最強的 3 篇：**
1. **P7 → Financial Analysts Journal**（理論貢獻最高）
2. **P2 → IRFA**（實證發現最強）
3. **P5 → FRL**（字數最接近、GCI 最新穎）

---

## 五、坦率評估：你的論文在頂級期刊有機會嗎？

**坦白說：**

1. **P7 有真正進入頂級金融期刊的潛力。** 它的理論框架是原創的，政策相關性強，時機完美。如果能在 Financial Analysts Journal 發表（CFA Institute 自家期刊），這將是最有影響力的成果。

2. **P2 和 P1 是紮實的實證工作**，但它們本質上是「將已有的 ML 評估範式應用到金融領域」。這在 FRL/IRFA 等 Q1 期刊完全有發表空間，但不會被視為開創性工作。

3. **P3、P4、P6 面臨樣本量和方法論挑戰。** P4 的 N=47 在任何嚴肅的定量期刊都會被質疑。P3 的 N=60 勉強及格但不理想。P6 的 N=90 加上信心計算 bug 需要修復。

4. **整體而言，7 篇中有 4–5 篇可以進入 SCI Q1 期刊（IF 5+）。** 這已經是很好的成績。關鍵是選對期刊、對準字數限制、修復已知的方法論問題。

5. **最大的競爭威脅是時間。** NYU Stern 的 CFA Level III 研究（23 個模型）和 CFA-Based Benchmark Study（1,560 題）已經在 arXiv 上了。你的差異化優勢（選項偏差、壓力測試、信號理論）是獨特的，但如果拖太久，別人可能會追上來。

---

# 以下為完整同儕審查報告（繁體中文翻譯）

---

## 目錄

1. [執行摘要](#1-執行摘要)
2. [文獻比對與新穎性評估](#2-文獻比對與新穎性評估)
3. [數據完整性審計](#3-數據完整性審計)
4. [方法論批評](#4-方法論批評)
5. [逐篇審查（P1–P7）](#5-逐篇審查)
6. [跨論文結構性問題](#6-跨論文結構性問題)
7. [評分摘要](#7-評分摘要)
8. [新研究方向](#8-新研究方向)

---

## 1. 執行摘要

本系列 7 篇論文代表了一項系統性的 LLM 金融推理評估，使用源自 SchweserNotes 的 CFA 考試題目（透過 FinDAP，EMNLP 2025 Oral）。涵蓋選項偏差測量、穩健性壓力測試、行為偏誤檢測、對抗式倫理、錯誤分類、信心校準及信號理論分析。

### 整體評估

**優勢：**
- **真正的新穎性**——將已建立的 ML 評估範式（擾動穩健性、校準、格式比較）應用於專業金融認證——此前無人做過如此全面的研究
- **連貫的研究計畫**——7 篇論文形成相互扣合的系列，發現之間有意義地交叉引用
- **核心實驗的方法論嚴謹性**（McNemar 檢定含 Yates 校正、配對設計、全樣本覆蓋）
- **修正完整性**——空白回應偏差被識別並修正，而非隱藏（A5、I2）

**弱點：**
- **不對稱的評估方法論**——A5 實驗的旗艦實驗（字母匹配 vs. 混合數值+評判者評分）威脅核心「選項偏差」的主張
- **小樣本量**——P4 (N=47) 和 P6 (N=90) 限制了可推廣性
- **單模型為主的結果**——大多數論文以 GPT-4o-mini 為主模型、GPT-5-mini 為交叉驗證；若有 3 個以上模型會更有說服力
- **LLM-as-judge 可靠性**——空白回應約 55% 被評為正確的問題已被捕獲，但根本性的評判者可靠性問題（調查文獻顯示專家領域一致性僅 60–68%）仍未解決
- **JSON 與論文數據不一致**——A5 GPT-5-mini（檔案中 86.3% vs. 論文中 83.2%）——修正是合理的但 JSON 檔案從未更新，造成可審計性疑慮

### 結論
7 篇中有 5 篇適合在 Finance Research Letters 修改後發表。P7（信號理論）是最強的貢獻。P4（對抗倫理）和 P3（行為偏誤）面臨最大挑戰。

---

## 2. 文獻比對與新穎性評估

### 調查論文數：46+ 篇，涵蓋 6 個類別

| 類別 | 審查論文數 | 主要來源 |
|------|-----------|---------|
| MCQ 格式偏差 | 4 | Zheng et al. (ICLR 2024 Spotlight), Balepur et al. (ACL 2025), Myrzakhan et al. (Open-LLM-Leaderboard 2024), Sanchez Salido et al. (2025) |
| CFA/金融考試評估 | 6 | Callanan et al. (FinNLP/IJCAI 2024), Mahfouz et al. (EMNLP 2024 Industry), Patel et al. (arXiv 2025), Jagabathula et al. (NYU/arXiv 2025), CFA-Based Benchmark (arXiv 2509.04468), FinDAP (EMNLP 2025 Oral) |
| 記憶/穩健性 | 8 | GSM-Symbolic (ICLR 2025), GSM-Plus (ACL 2024), GSM-DC (EMNLP 2025), MATH-Perturb (ICML 2025), Lopez-Lira 記憶問題 (2025), RECALL (ACL 2024), Mosaic Memory (Nature Comms 2026), Generalization vs. Memorization (ICLR 2025) |
| LLM 行為偏誤 | 4 | LLM Economicus (COLM 2024), Suri et al. (J. Exp. Psych. 2024), Malberg et al. (NLP4DH 2025), Capraro et al. (PNAS 2025) |
| 校準/信心 | 5 | Xiong et al. (ICLR 2024), QA-Calibration (ICLR 2025), Mind the Confidence Gap (TMLR 2025), KalshiBench (2025), UQ Survey (KDD 2025) |
| 對抗安全/倫理 | 6 | FITD (EMNLP 2025), HarmBench (ICML 2024), JailbreakBench (NeurIPS 2024), TRIDENT (2025), LLM Ethics Benchmark (Sci. Reports 2025), Andriushchenko et al. (ICLR 2025) |
| 信號理論/AI 影響 | 4 | Galdin & Silbert (Princeton 2025), AI & Higher Ed Signaling (MDPI 2024), "Can AI Distort Human Capital?" (2024), "Reasoning Models Ace CFA" (arXiv 2025) |
| LLM-as-judge 可靠性 | 4 | CALM (NeurIPS 2024), Chen et al. (EMNLP 2024), Survey on LLM-as-Judge (2024), Noisy Rationales (NeurIPS 2024) |
| 金融 LLM 基準 | 5 | FinEval (2023), FinanceBench (2023), FinBen (NeurIPS 2024), BloombergGPT (2023), FinGPT (2023) |

### 各論文新穎性裁定

| 論文 | 最接近的先行研究 | 是否新穎？ | 新穎度評級 |
|------|----------------|----------|----------|
| **P1**（選項偏差）| Open-LLM-Leaderboard (Myrzakhan 2024)——在 MMLU 上做 MCQ→開放式轉換 | **是。** 首次在金融領域問題上做 MCQ vs. 開放式比較。首次展示模型依賴性的選項偏差（p=0.251→p<0.001）。三級評估（A/B/C）是新穎的評分方案。 | ★★★★☆ |
| **P2**（壓力測試）| GSM-Symbolic (ICLR 2025)——對數學的噪音/擾動 | **是。** 首次在 CFA 問題上做反事實擾動 + 噪音注入。領域特定的噪音分類（N1–N4）是新穎的。「記憶落差」指標應用於專業知識是新的。 | ★★★★☆ |
| **P3**（行為偏誤）| LLM Economicus (COLM 2024)——透過效用理論測試行為偏誤 | **部分。** 損失趨避、錨定、框架效應與 Ross et al. 重疊。P3 的新穎性在於金融特定的配對情境（CFA 層級的投資決策場景）以及未被他人測試的偏誤類型（從眾、沉沒成本）。 | ★★★☆☆ |
| **P4**（對抗倫理）| TRIDENT (2025)——金融安全基準, FITD (EMNLP 2025)——多輪越獄 | **是。** 無先行研究測試專業倫理判斷的對抗式翻轉（相對於安全拒絕）。CFA 特定的壓力分類和 ERS 指標是新穎的。GPT-5-mini 免疫性發現引人注目。 | ★★★☆☆ |
| **P5**（錯誤圖譜）| CFA-Based Benchmark (2509.04468)——CFA 錯誤分類; FLARE (ACL 2025)——錯誤分類 | **是。** 黃金上下文注入（GCI）作為診斷性預言實驗無先例。發現即使在完美上下文下僅 50.4% 的錯誤可完全恢復，是新穎且實用的重要發現。 | ★★★★☆ |
| **P6**（校準）| Xiong et al. (ICLR 2024)——LLM 信心校準 | **部分。** 在 CFA 問題上的校準是新的領域應用。CaR（信心風險值）橋接 VaR 與 LLM 校準是真正新穎的。但 N=90 限制影響力。 | ★★★☆☆ |
| **P7**（信號理論）| Galdin & Silbert (Princeton 2025)——自由市場中 AI + Spence 信號 | **是。** 首次將 Spence 信號模型正式應用於專業 CFA 認證的 AI 顛覆。部分信號崩潰定理是原創理論貢獻。透過 A5 數據的實證基礎整合良好。 | ★★★★★ |

### 關鍵發現：無實質相同的先行研究

**在調查的 46+ 篇論文中，沒有任何一篇執行過與 7 篇論文中任何一篇實質相同的實驗。** 最接近的重疊有：
1. P3 vs. LLM Economicus——兩者都測試行為偏誤但在不同領域用不同方法
2. P2 的 I3 vs. GSM-Symbolic——相同擾動範式應用於不同領域
3. P6 vs. Xiong et al.——相同校準方法應用於不同領域

關鍵差異化因素是**系統性地應用於專業金融知識（CFA 考試問題）**與**領域特定的實驗設計**，這對 Finance Research Letters 而言是適當的定位。

---

## 3. 數據完整性審計

### 方法論
所有實驗結果 JSON 檔案均以程式方式讀取，並與 7 篇論文 LaTeX 檔案和 MEMORY.md 文件中的聲明進行交叉比對。

### 驗證結果

| 實驗 | JSON 數值 | 論文聲明 | 是否一致？ |
|------|----------|---------|----------|
| A5 GPT-4o-mini 含選項 | 82.6% | 82.6% | ✅ |
| A5 GPT-4o-mini 無選項 | 80.6% | 80.6% | ✅ |
| A5 GPT-4o-mini 偏差 | +1.9pp | +1.9pp | ✅ |
| A5 GPT-4o-mini McNemar p | 0.251 | n.s. | ✅ |
| **A5 GPT-5-mini 無選項** | **86.3%** | **83.2%** | **⚠️ 不一致** |
| **A5 GPT-5-mini 偏差** | **+6.5pp** | **+9.6pp** | **⚠️ 不一致** |
| A5 GPT-5-mini 含選項 | 92.8% | 92.8% | ✅ |
| A1 GPT-4o-mini Level A/B/C | 253/222/557 | 253/222/557 | ✅ |
| I1 GPT-4o-mini 落差 | 18.6pp | 18.6pp | ✅ |
| I1 GPT-5-mini 落差 | 36.4pp | 36.4pp | ✅ |
| I3 所有 NSI 值（兩模型） | 全部一致 | 全部一致 | ✅ |
| I2 GPT-4o-mini 平均偏誤 | 0.500 | 0.500 | ✅ |
| D6 GPT-4o-mini 翻轉數 | 14 | 14 | ✅ |
| D6 GPT-5-mini 翻轉數 | 0 | 0 | ✅ |
| E1 GPT-4o-mini 恢復率 | 82.4% | 82.4% | ✅ |
| E1 GPT-5-mini 恢復率 | 88.3% | 88.3% | ✅ |
| E1 GPT-5-mini 完全恢復 | 50.4% | 50.4% | ✅ |
| D1 總觀測數 | 257 | 257 | ✅ |

### 關鍵不一致：A5 GPT-5-mini

**問題：** JSON 檔案（`run_20260207_174114/results.json`）顯示 `accuracy_without_options = 0.8634`（86.3%），對應 +6.5pp 選項偏差。P1 和 P7 均報告無選項準確率 83.2%、偏差 +9.6pp。

**解釋：** 此不一致記錄於 MEMORY.md，源自空白回應的**事後修正**：
- 1,032 個「無選項」回應中有 58 個為空白（模型未返回內容）
- LLM-as-judge 將其中 32 個空白回應評為「正確」（55% 的比率）
- 作者保守地將所有 58 個空白回應視為不正確
- 修正後：891 - 32 = 859 正確 → 859/1032 = 83.2%

**評估：** 修正在方法論上是**可辯護的**——將空白回應評為正確顯然是評判者限制的偽影。然而：
1. **JSON 檔案從未更新**以反映修正，造成可審計性缺口
2. **不存在修正腳本**——修正是手動應用到 LaTeX 的
3. 有權限存取 JSON 的審稿人會發現數字不匹配
4. **建議：** 創建文件化的後處理腳本

### GPT-5-mini I2 數據：正確移除

I2 行為偏誤實驗的 GPT-5-mini 產生 80% 空白回應，導致偽影平均偏誤分數 0.892。**從 P3 移除此數據的決定是正確且值得稱讚的。**

### E1 GCI GPT-5-mini：已驗證

完整運行（`golden_context_gpt-5-mini_20260207_220440.json`）N=557 錯誤已驗證。儘管有 51 個空白回應（9.2%），整體結果與論文完全一致。

---

## 4. 方法論批評

### 4.1 關鍵問題（必須解決）

**問題 1：A5 選項偏差的不對稱評估（影響 P1、P7）**

核心「選項偏差」的測量比較了：
- **含選項：** 標準 MCQ 字母提取（`extract_answer()`）→ 精確字元匹配
- **無選項：** 混合評估——先嘗試數值容差（±2%），再 LLM-as-judge 回退

這**不是受控比較。**「無選項」條件使用根本不同的（且在數值問題上可能更寬鬆、在文字問題上更不穩定的）評估方法。因此測量到的「選項偏差」混淆了：
1. 真正的格式依賴性表現差異
2. 評估方法論差異

**嚴重程度：高。** 這是所有 7 篇論文中最重要的方法論問題。核心發現（選項偏差存在且模型依賴）可能在方向上仍然正確，但幅度（+1.9pp、+9.6pp）可能受評估不對稱性干擾。

**緩解因素：** GPT-4o-mini 顯示不顯著的 +1.9pp 偏差（p=0.251），而 GPT-5-mini 顯示 +9.6pp（p<0.001），兩者使用**相同的評估管線**，表明模型依賴性發現即使在絕對幅度不精確的情況下也是穩健的。

**問題 2：LLM-as-Judge 空白回應偏差（影響使用評判者的所有論文）**

`semantic_match_judge()` 函數沒有驗證學生答案是否為空。空白或近乎空白的回應約 55% 被評為「正確」，系統性地向上偏移結果。

**已解決：** A5 修正（83.2%）和 I2 移除已處理已知實例。

**問題 3：validate_perturbation() 在 I1 中從未被調用（影響 P2）**

程式庫定義了綜合的 `validate_perturbation()` 函數，但在 `run_experiment.py` 中**從未被調用**。估計 10–20% 的擾動可能無效，這主要使記憶落差測量向上偏移。

### 4.2 中度問題（應該解決）

**問題 4：D1 的信心計算 Bug（影響 P6）**

自我一致性信心除以總數 `k` 而非 `len(valid)`。如果 10 個回應中有 3 個提取失敗，信心計算為 majority/10 而非 majority/7，人為壓低信心估計約 30%。直接影響 ECE 和 CaR 計算。

**問題 5：答案提取的靜默失敗（影響所有論文）**

`extract_answer()` 在所有 5 層正則表達式都失敗時靜默返回 `None`。調用者將 None 視為錯誤而不記錄。

**問題 6：數值提取取最後一個數字（影響 P1 A1）**

`extract_numerical_answer()` 的回退取回應文字中的**最後一個數字**，可能是中間計算而非最終答案。

### 4.3 輕微問題（可選）

- `tolerance_match()` 對 gold=0 允許 [-0.02, 0.02] 區間——技術上過於寬鬆
- 評判者 JSON 回退使用關鍵字匹配——可能產生假陽性
- I3 噪音注入未驗證注入的噪音是否真的改變了查詢
- E1 黃金上下文評判者解析使用非穩健的正則表達式

---

## 5. 逐篇審查

---

### 論文 1（P1）：Beyond Multiple Choice——選項偏差 + 三級評估
**實驗：** A1_open_ended + A5_option_bias | **N=1,032** | **字數：~3,719**

#### 分數：78/100

#### 決定：接受但需重大修改

#### 優勢
1. **新穎的實驗設計：** 首次在專業金融問題上進行系統性 MCQ vs. 開放式比較（N=1,032）。金融領域無先行研究。
2. **引人注目的發現：**「選項偏差悖論」——GPT-5-mini 顯示 +9.6pp 偏差（p<0.001），而 GPT-4o-mini 僅 +1.9pp（p=0.251, n.s.）——真正令人意外，具高引用潛力。
3. **三級評估（A/B/C）：** 超越二元評分的細緻分級。
4. **全樣本設計：** 使用全部 1,032 題 CFA-Easy 問題，統計效力強。

#### 弱點
1. **關鍵——評估不對稱（§4.1）：** 含選項用字母匹配，無選項用混合數值容差+LLM 評判。不是比較同類事物。
2. **A5 GPT-5-mini 數據修正：** 83.2% 的數字需要在論文中透明記錄。
3. **機制解釋薄弱：**「收斂錨定」假說合理但屬推測。
4. **僅測試 2 個模型：** 格式偏差研究的慣例是 5 個以上模型。

#### 缺失文獻
- Open-LLM-Leaderboard (Myrzakhan et al., 2024)——**必須引用**
- "None of the Others" (Sanchez Salido et al., 2025)
- Zheng et al. (ICLR 2024 Spotlight)——MCQ 選擇偏差

#### 需要的具體修改
1. 在方法論中明確承認評估不對稱
2. 添加數據修正的註腳或「數據處理」小節
3. 引用並區分 Open-LLM-Leaderboard
4. 考慮敏感性分析：如果兩種條件都只用評判者評分，選項偏差是多少？

---

### 論文 2（P2）：壓力測試——反事實擾動 + 噪音注入
**實驗：** I1_counterfactual + I3_noise_red_herrings | **N=1,032** | **字數：~4,367**

#### 分數：82/100

#### 決定：接受但需小修

#### 優勢
1. **強實驗設計：** 反事實擾動（I1）+ 噪音注入（I3）提供互補的穩健性測試。配對設計實現乾淨的比較。
2. **引人注目的跨模型發現：** GPT-5-mini 的記憶落差幾乎是 GPT-4o-mini 的兩倍（36.4pp vs. 18.6pp），儘管基線準確率更高。此「擴展悖論」具高引用性。
3. **領域特定噪音分類（N1–N4）** 是真正的貢獻。
4. **噪音敏感度指標（NSI）** 提供跨噪音類型的標準化比較。

#### 弱點
1. **validate_perturbation() 未使用（§4.1 問題 3）：** 未知比例的擾動可能無效。
2. **必須突出引用 GSM-Symbolic：** 擾動注入範式由 GSM-Symbolic (ICLR 2025) 和 GSM-Plus (ACL 2024) 建立。
3. **N4 顯示負 NSI：** 過量細節反而改善表現——需更多討論。
4. **擾動答案格式不一致**

#### 缺失文獻
- GSM-Symbolic (ICLR 2025)——**必須引用為主要方法論先例**
- GSM-Plus (ACL 2024), GSM-DC (EMNLP 2025), MATH-Perturb (ICML 2025)
- Lopez-Lira et al. (2025)——金融 LLM 的記憶問題
- Mosaic Memory (Nature Comms 2026)

---

### 論文 3（P3）：繼承的非理性——LLM 中的行為偏誤
**實驗：** I2_behavioral_biases | **N=60 個情境** | **字數：~3,395**

#### 分數：62/100

#### 決定：修改後重審

#### 優勢
1. **創意場景設計：** 60 個目的建構的配對情境，涵蓋 6 種偏誤類型。
2. **平均偏誤分數 0.500** 是引人注目的發現。
3. **去偏誤層級**（結構化 > 指導性 > 情境性）具實用貢獻。

#### 弱點
1. **N=60 偏小。** 每種偏誤類型僅 10 個情境，缺乏統計效力。
2. **與現有文獻有實質重疊：** LLM Economicus (COLM 2024)、Suri et al. (J. Exp. Psych. 2024) 和 Malberg et al. (NLP4DH 2025) 都測試過錨定、框架和損失趨避。
3. **單一主模型 (GPT-4o-mini)。**
4. **LLM-as-judge 自我評判問題。**
5. **「繼承」框架缺乏支持：** 標題暗示偏誤從訓練數據傳遞到模型行為，但未提供訓練數據分析。

#### 缺失文獻
- LLM Economicus (COLM 2024)——**必須引用並廣泛區分**
- Suri et al. (J. Exp. Psych. 2024), Malberg et al. (NLP4DH 2025), Capraro et al. (PNAS 2025)

---

### 論文 4（P4）：承壓——對抗式倫理
**實驗：** D6_adversarial_ethics | **N=47** | **字數：~3,536**

#### 分數：58/100

#### 決定：拒絕（鼓勵修改後重投）

#### 優勢
1. **新穎實驗：** 無先行研究測試對抗式提示能否翻轉專業倫理判斷。
2. **引人注目的跨模型發現：** GPT-4o-mini 14 次翻轉 vs. GPT-5-mini 0 次——完全免疫。
3. **倫理穩健性分數（ERS）** 與 CFA 標準的映射。

#### 弱點
1. **致命——N=47。** 47 個觀測不足以支撐定量結論。每種壓力類型分析（47 ÷ 5 ≈ 9.4）基本上沒有統計效力。
2. **零翻轉仍然可疑。** 無法區分：
   - 真正的倫理穩健性（模型推理並拒絕壓力）
   - 記憶導致的免疫（模型忽略壓力因為匹配了記憶模式）
   這在 P2 發現 GPT-5-mini 有 36.4pp 記憶落差的背景下尤其令人擔憂。
3. **單次提示設計：** FITD (EMNLP 2025) 表明多輪升級更有效。
4. **無人類基線。**

#### 缺失文獻
- FITD (EMNLP 2025), TRIDENT (2025), HarmBench (ICML 2024), JailbreakBench (NeurIPS 2024)

---

### 論文 5（P5）：CFA 錯誤圖譜——錯誤分類 + 黃金上下文注入
**實驗：** E1_error_analysis | **N=557 個錯誤** | **字數：~2,627**

#### 分數：76/100

#### 決定：接受但需小修

#### 優勢
1. **GCI 真正新穎。** 提供完美上下文並測量恢復——無先例。僅 25.5% (GPT-4o-mini) / 50.4% (GPT-5-mini) 實現完全恢復是重要的診斷發現。
2. **錯誤分類是領域特定的。** 68.8% 概念錯誤的發現具實用意義。
3. **清晰的解釋：** 知識缺口（可通過上下文恢復）vs. 推理缺口（不可恢復）。
4. **GPT-5-mini 交叉驗證**已驗證正確。

#### 弱點
1. **字數偏低（2,627）。** 需要更多討論。
2. **GCI 混淆知識缺口與注意力效果。**
3. **錯誤類別手動指定，未報告評分者間信度。**
4. **GPT-5-mini 有 51 個空白回應（9.2%）**應在論文中提及。

#### 缺失文獻
- CFA-Based Benchmark (arXiv 2509.04468), FLARE (ACL 2025), Self-RAG (ICLR 2024 Oral)

---

### 論文 6（P6）：自信地犯錯——校準 + 過度自信風險
**實驗：** D1_confidence_calibration + D4_overconfident_risk | **N=90 題, 257 觀測** | **字數：~3,463**

#### 分數：68/100

#### 決定：修改後重審

#### 優勢
1. **CaR（信心風險值）** 是真正有創意的指標，橋接金融風險管理（VaR）和 LLM 校準。
2. **實用相關性：** 過度自信的 AI 金融顧問構成真正的監管風險。
3. **多種校準方法**（口頭信心、自我一致性、logprobs）。

#### 弱點
1. **N=90（257 觀測）對校準研究而言偏小。**
2. **信心計算 Bug（§4.2 問題 4）：** 必須調查並修復。
3. **解析失敗時回退到 0.5 信心**向校準分析注入噪音。
4. **CFA-Challenge 的正當性合理但有限制。**

#### 缺失文獻
- Xiong et al. (ICLR 2024)——**必須引用為主要方法論先驅**
- QA-Calibration (ICLR 2025), Mind the Confidence Gap (TMLR 2025), KalshiBench (2025)

---

### 論文 7（P7）：當機器通過考試——信號理論
**實驗：** 理論性；引用 A5 數據 | **N=1,032（透過 A5）** | **字數：~4,231**

#### 分數：88/100

#### 決定：接受但需小修

#### 優勢
1. **傑出的理論貢獻。** 將 Spence (1973) 信號模型正式擴展，引入 AI 作為降低信號成本的第三參與者，是整個系列中最原創的貢獻。「部分信號崩潰定理」是真正的新穎結果。
2. **信號保留率（28.8%）** 是理論模型使用 A5 數據的優雅實證應用。
3. **政策相關性：** 對 CFA Institute 的建議（格式重設計、AI 抵抗性評估）具可操作性且及時。
4. **有同期實證支持：**「Reasoning Models Ace the CFA Exams」(Patel et al., 2025) 直接支持 P7 的理論論點。
5. **跨學科強度：** 成功橋接勞動經濟學、教育理論和 AI 評估。

#### 弱點
1. **實證基礎完全依賴 P1 的 A5 數據。** 如果 A5 評估被質疑，P7 的經驗校準會弱化。
2. **定理假設二元的可形式化/隱性技能分割。** 實際上技能分布是連續的。
3. **無信號價值侵蝕的直接證據。** 無雇主行為數據。
4. **A5 數據修正（83.2%, +9.6pp）實際上強化了論點**——但這種不對稱依賴應透明化。

#### 缺失文獻
- Galdin & Silbert (Princeton 2025)——**必須引用**
- "Reasoning Models Ace the CFA Exams" (Patel et al., 2025)
- AI & Higher Ed Signaling (MDPI 2024)

---

## 6. 跨論文結構性問題

### 6.1 數據重用與獨立性
P1 和 P7 共用 A5 選項偏差數據。P5 使用 A1 的錯誤集（557 個 Level C 回應）。P2 使用相同的 1,032 題。這在基礎數據（CFA-Easy N=1,032）中創建了依賴鏈。**對作為系列提交的研究計畫而言這是可接受的**，但每篇論文應自成一體。

### 6.2 GPT-5-mini 空白回應問題
GPT-5-mini 在三個實驗中產生空白回應：
- A5：58/1,032 (5.6%)——已修正
- I2：48/60 (80%)——數據已移除
- E1：51/557 (9.2%)——整體結果仍有效

**建議：** 在每篇跨模型論文中添加「GPT-5-mini 回應品質」說明。

### 6.3 LLM-as-Judge 一致性
所有實驗使用 `gpt-4o-mini` 作為評判模型。一致性好但未經人類專家判斷驗證。調查文獻顯示僅 60–68% 的領域專家一致性。

### 6.4 數據集來源
所有論文使用透過 FinDAP 衍生的 SchweserNotes 問題。部分 CFA 問題可能與模型訓練數據重疊（基準汙染）。P2 的反事實實驗部分解決了此問題。

---

## 7. 評分摘要

| 論文 | 分數 | 決定 | 關鍵優勢 | 關鍵弱點 |
|------|------|------|---------|---------|
| **P7**（信號） | **88** | 接受/小修 | 原創理論貢獻；部分信號崩潰定理 | 完全依賴 P1 的 A5 數據 |
| **P2**（壓力測試） | **82** | 接受/小修 | 震撼性記憶落差發現（36.4pp）；領域特定噪音分類 | 需定位於 GSM-Symbolic 範式；驗證函數未使用 |
| **P1**（選項偏差） | **78** | 接受/大修 | 新穎的 MCQ vs. 開放式比較；模型依賴性偏差悖論 | 評估方法不對稱是關鍵問題 |
| **P5**（錯誤圖譜） | **76** | 接受/小修 | GCI 真正新穎；AI 顧問的實用意義 | 篇幅短；混淆知識缺口與注意力效果 |
| **P6**（校準） | **68** | 修改重審 | CaR 指標有創意；監管風險框架適當 | N=90 不足；信心計算 bug |
| **P3**（行為偏誤） | **62** | 修改重審 | 金融特定配對情境；去偏誤層級 | N=60 小；與現有文獻重疊大；單模型 |
| **P4**（對抗倫理） | **58** | 拒絕（鼓勵重投） | 新穎實驗；GPT-5-mini 完全免疫引人注目 | N=47 致命；無法區分穩健性 vs 記憶 |

---

## 8. 新研究方向

### 方向 1：多模型格式偏差全景
擴展至 10+ 模型（含 Claude、Gemini、Llama、DeepSeek）在相同 CFA-Easy 問題上映射「格式偏差全景」。

### 方向 2：動態/程序化 CFA 題目生成
從金融第一原理動態生成 CFA 風格問題，完全消除汙染疑慮。

### 方向 3：多輪對抗倫理升級
遵循 FITD (EMNLP 2025)，設計多輪升級實驗（如客戶逐步向 AI 金融顧問施壓）。

### 方向 4：校準加權諮詢系統
將 P6 的 CaR 指標操作化為實際諮詢系統中的信心加權推薦機制。

### 方向 5：人類專家基線比較
比較 LLM 表現與人類 CFA 考生/持證人在選項偏差、記憶落差、行為偏誤上的差異。

### 方向 6：縱向信號價值追蹤
追蹤 CFA 持證人薪資溢價、雇主調查、考試報名趨勢隨 AI 能力提升的變化。

### 方向 7：受控無關上下文的 GCI
注入**無關**黃金上下文作為控制條件，區分真正的知識恢復與注意力增強效果。

### 方向 8：推理軌跡分析
使用開源推理模型（如 DeepSeek-R1）分析內部推理軌跡中記憶模式和推理脫軌的位置。

---

## 附錄：文獻引用

### MCQ 格式偏差
1. Zheng et al. "Large Language Models Are Not Robust Multiple Choice Selectors." ICLR 2024 Spotlight.
2. Pezeshkpour & Hruschka. "Large Language Models Sensitivity to The Order of Options." NAACL 2024.
3. Balepur, Rudinger, Boyd-Graber. "Which of These Best Describes Multiple Choice Evaluation with LLMs?" ACL 2025.
4. Sanchez Salido et al. "None of the Others." 2025.
5. Myrzakhan et al. "Open-LLM-Leaderboard: From Multi-choice to Open-style Questions." 2024.

### CFA/金融考試評估
6. Callanan et al. "Can GPT Models Be Financial Analysts?" FinNLP/IJCAI 2024.
7. Mahfouz et al. "The State of the Art of LLMs on CFA Exams." EMNLP 2024 Industry.
8. Patel et al. "Reasoning Models Ace the CFA Exams." arXiv 2025.
9. Jagabathula et al. "Advanced Financial Reasoning at Scale: CFA Level III." arXiv 2025.
10. "Evaluating LLMs for Financial Reasoning: A CFA-Based Benchmark Study." arXiv 2509.04468, 2025.
11. Ke et al. "FinDAP." EMNLP 2025 Oral.

### 記憶/穩健性
12. Mirzadeh et al. "GSM-Symbolic." ICLR 2025.
13. Li et al. "GSM-Plus." ACL 2024.
14. Yang et al. "GSM-DC." EMNLP 2025.
15. "MATH-Perturb." ICML 2025.
16. Lopez-Lira, Tang, Zhu. "The Memorization Problem." 2025.
17. Liu et al. "RECALL." ACL 2024.
18. "The Mosaic Memory of Large Language Models." Nature Communications, 2026.
19. Dong et al. "Generalization or Memorization." ACL 2024.
20. "Generalization v.s. Memorization." ICLR 2025.

### LLM 行為偏誤
21. Ross, Kim, Lo. "LLM Economicus?" COLM 2024.
22. Suri et al. "Do LLMs Show Decision Heuristics Similar to Humans?" J. Exp. Psych.: General, 2024.
23. Malberg et al. "A Comprehensive Evaluation of Cognitive Biases in LLMs." NLP4DH 2025.
24. Capraro et al. "Amplified Cognitive Biases in Moral Decision-Making." PNAS 2025.

### 校準/信心
25. Xiong et al. "Can LLMs Express Their Uncertainty?" ICLR 2024.
26. "QA-Calibration." ICLR 2025.
27. Chhikara. "Mind the Confidence Gap." TMLR 2025.
28. "KalshiBench." 2025.
29. "UQ & Calibration Survey." KDD 2025.

### 對抗安全/倫理
30. "Foot-In-The-Door (FITD)." EMNLP 2025.
31. Mazeika et al. "HarmBench." ICML 2024.
32. Chao et al. "JailbreakBench." NeurIPS 2024.
33. Hui et al. "TRIDENT." 2025.
34. "LLM Ethics Benchmark." Scientific Reports, 2025.
35. Andriushchenko et al. "Jailbreaking Leading Safety-Aligned LLMs." ICLR 2025.

### 信號理論 / AI 影響
36. Galdin & Silbert. "Making Talk Cheap." Princeton Economics, 2025.
37. "AI and the Sustainability of Signaling and Human Capital Roles of Higher Education." MDPI Sustainability, 2024.
38. Li & Zhou. "Can AI Distort Human Capital?" Working Paper, 2024.

### LLM-as-Judge
39. "Justice or Prejudice? (CALM)." NeurIPS 2024.
40. Chen et al. "Humans or LLMs as the Judge?" EMNLP 2024.
41. "A Survey on LLM-as-a-Judge." arXiv 2024.

### 金融 LLM 基準
42. Zhang et al. "FinEval." 2023.
43. Islam et al. "FinanceBench." 2023.
44. Xie et al. "FinBen." NeurIPS 2024.
45. Wu et al. "BloombergGPT." 2023.
46. Yang et al. "FinGPT." 2023.

### 其他
47. Liang et al. "Noisy Rationales." NeurIPS 2024.
48. "Profit Mirage / FactFin." 2025.
49. ESMA. "Leveraging Large Language Models in Finance." 2025.

---

*本審查以程式化方式進行，完整存取所有實驗程式碼、結果檔案和論文手稿。所有數據交叉引用均已針對儲存庫中的實際 JSON 結果檔案進行驗證。*
