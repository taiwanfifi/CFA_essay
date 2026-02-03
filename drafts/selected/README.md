# 精選研究清單：10 篇論文的攻擊路線圖

## 核心論述

金融 LLM 的評估正處於一個尷尬的位置：所有人都在刷 benchmark 分數，但沒有人追問三個根本問題——**準確率是真的嗎**（MCQ 選項是拐杖、題目可能被背過）、**錯的時候知道自己錯嗎**（過度自信比答錯更危險）、**在真實環境下還能維持嗎**（噪音、偏誤、多模態）。

本清單的 10 篇論文構成一條完整的攻擊鏈：先拆穿現有 benchmark 的假象（A1, A5），再揭露模型不知道自己不知道的危險（D1, D4），繪製錯誤的精確地圖（E1），然後開闢多模態與制度理論的新戰場（H1, G2），最後用對抗性壓力測試做終極檢驗（I1, I2, I3）。每篇都有明確的新穎貢獻，合在一起是對「金融 AI 到底行不行」這個問題的系統性回答。

---

## 快速導覽

| 編號 | 題目 | 測什麼 | 新穎點 | 難度 | 依賴 |
|------|------|--------|--------|------|------|
| **A1** | Open-Ended Numerical Reasoning | 移除選項後的真實推理能力 | 三層判定機制 + 結構化錯誤歸因 | ★★★ | 無 |
| **A5** | MCQ Option Bias Quantification | 選項提供了多少不公平優勢 | 精確量化 option bias 的三維分解 | ★★ | 與 A1 共享基礎設施 |
| **D1** | Calibration & Selective Prediction | 模型的信心值是否可靠 | 四種 confidence 方法的金融場景比較 | ★★ | 無 |
| **D4** | Overconfident AI Risk Analysis | 高信心錯誤答案的系統性風險 | CFA Ethics 框架 + 監管啟示 | ★★ | D1 |
| **E1** | CFA Error Pattern Atlas | 錯誤的精確分類與地圖 | 三維 Error Taxonomy + 可公開釋出的圖譜 | ★★★ | 無 |
| **H1** | Multimodal Financial Reasoning | 圖表理解是否為獨立瓶頸 | 首個多模態 CFA 基準 | ★★★★ | 無 |
| **G2** | Signaling Theory under AI | AI 如何瓦解專業認證的訊號價值 | Modified Spence Model 理論推導 | ★★★★ | G1 (Ability Matrix) |
| **I1** | Counterfactual Stress Test | 背題 vs 真懂金融邏輯 | Robust Accuracy 指標 + Memorization Gap | ★★★ | 無 |
| **I2** | Behavioral Biases in LLMs | LLM 是否繼承人類非理性偏誤 | 六維偏誤框架 + Debiasing 實驗 | ★★★ | 無 |
| **I3** | Noise & Red Herrings | 模型能否過濾無關資訊 | Noise Sensitivity Index + Dose-Response 分析 | ★★ | 無 |

> 難度：★ 數量反映實驗設計與資料準備的複雜度，不代表學術價值高低。

---

## 研究詳解：五大戰線

### 戰線一：拆穿 Benchmark 的假象 (A1, A5)

**Story**：選項是拐杖 → 移除選項後真相大白。

現有 CFA benchmark 清一色是 MCQ。但選項本身洩漏了答案的量級方向（order of magnitude）、符號正負（全正或有負）、以及排除不合理答案的線索。這不是理論推測——GSM8K 領域已經證明去選項後準確率暴跌。

- **A1** 是基礎工程：建構 open-ended 版 CFA 基準，設計三層判定機制（Exact → Directional → Incorrect），並用結構化錯誤歸因系統分析每一個錯誤的根源。這不只是「去掉選項」，而是重新定義「什麼算對」——金融領域的 compounding 假設、day count convention、rounding policy 都讓正確答案不唯一。
- **A5** 是精確量化：同一題、同一模型、有選項 vs 無選項，option bias = accuracy_with - accuracy_without。在模型規模、CFA 主題、題目類型三個維度上分解 bias 的來源。特別關注「有選項才答對」的題目——這些最能揭示 crutch effect 的機制。

**合作邏輯**：A1 建設基準設施，A5 產出精確數字。A5 的數據是 A1 實驗的天然副產品。

### 戰線二：揭露過度自信的危險 (D1, D4)

**Story**：不只要對，還要知道自己不知道什麼。

金融場景中，答錯不是最危險的——**高度自信地答錯**才是。一個說「我 95% 確定這支債券的 duration 是 4.2 年」但實際上算錯的 AI，比坦承不確定的 AI 危險一百倍。

- **D1** 是技術測量：四種 confidence estimation 方法（Verbalized / Self-Consistency / Ensemble / Logit-based）的系統比較。核心指標是 Expected Calibration Error (ECE) 和 coverage-accuracy tradeoff——模型在何種信心閾值下能達到 CFA 及格水準的準確度？這是所有研究中計算資源需求最低的，純統計分析。
- **D4** 是風險應用：從 D1 數據中篩選「confidence ≥ 80% 但答案錯誤」的案例，進行系統性風險分析。獨特貢獻在於連結 CFA Ethics Standards——AI 高信心錯誤答案是否構成 misrepresentation？依賴 overconfident AI 是否違反 due diligence？構建 AI Risk Severity Matrix（likelihood × impact）。

**合作邏輯**：D1 提供數據，D4 提供敘事與政策價值。D4 是 D1 的跨領域衍生，可投 AI policy 或金融科技期刊。

### 戰線三：繪製錯誤地圖 (E1)

**Story**：不同錯誤需要不同藥方。

「這個模型 CFA 準確率 70%」是無用的資訊——30% 的錯誤裡，多少是知識缺口、多少是公式誤用、多少是計算失誤、多少是被 distractor 迷惑？每種錯誤的修復策略完全不同：知識缺口需要更多訓練數據、公式誤用需要 structured reasoning、計算失誤需要 tool-use、distractor confusion 需要注意力機制改進。

- **E1** 建構三維 Error Taxonomy：Error Type（4 大類 12 子類）× CFA Topic（10 類）× Cognitive Stage（5 階段）。用 GPT-4o 作為自動分類器，在 200 題人工標註上驗證 Cohen's Kappa。產出一個可公開釋出的 CFA Error Pattern Atlas——圖譜本身即為核心學術貢獻（data/resource paper）。

**獨立價值**：E1 的 error taxonomy 是後續所有改進研究的起點。I1 的微擾後新增錯誤、I3 的雜訊誘發錯誤，都可以用 E1 的框架分類。

### 戰線四：開闢新戰場 (H1, G2)

**Story**：從純文字走向多模態 + 從技術走向制度。

前三條戰線都在現有的文字 CFA 題目框架內作戰。第四戰線跳出框架。

- **H1** 開闢多模態維度：CFA 考試大量使用 exhibit（財報表格、收益率曲線、散佈圖），但所有現有研究都只處理純文字。H1 建構首個多模態 CFA 基準，系統量化 multimodal gap（圖片版 vs 文字描述版的準確率差距），並分解圖表理解為三個子階段（數據讀取 → 趨勢辨識 → 整合推理）。
- **G2** 轉換分析單位：從模型到制度。用 Modified Spence Signaling Model 形式化推導：當 AI 複製認知能力的成本趨近零時，CFA 認證作為 labor market signal 的價值如何選擇性退化。這是一篇理論 + 實證論文，對話對象是 Spence (1973)、Becker (1964)、Autor (2003)。

**差異化定位**：H1 面向 ACL/EMNLP 的多模態 track，G2 面向 Management Science 或 QJE 等經濟學期刊。與前三條戰線的技術論文形成互補。

### 戰線五：對抗性壓力測試 (I1, I2, I3) ⭐ Stress Testing

**Story**：背題 vs 真懂？理性 vs 偏誤？乾淨 vs 雜訊？

這是整個研究計畫的壓軸戰線。前四條戰線建立了測量基礎設施，第五戰線用三種對抗性方法進行終極檢驗。

- **I1 反事實壓力測試**：改數字、改條件、改情境——如果模型是真懂金融邏輯，微擾後應該同樣答對；如果只是背考古題，Memorization Gap 會很大。提出 Robust Accuracy 作為比傳統 accuracy 更可靠的能力指標。靈感來自 Apple 的 GSM-Symbolic 研究。
- **I2 行為偏誤測試**：Loss Aversion、Anchoring、Herding、Recency Bias、Overconfidence、Disposition Effect——六種行為金融學經典偏誤的 LLM 版本。如果 AI 繼承了人類的非理性，Robo-Advisor 的安全性就需要重新評估。額外測試三種 debiasing 策略的效果。
- **I3 雜訊與紅鯡魚**：在乾淨題目中注入四類雜訊（無關數據、誤導陳述、格式噪音、矛盾資訊），量化 Noise Sensitivity Index。測試假說：CoT 推理模型的雜訊過濾能力優於 Direct Answer 模型。繪製 dose-response curve：雜訊要多重，模型才會崩潰？

**合作邏輯**：I1 改變 signal，I3 添加 noise——兩種互補的 stress test 維度。I2 從完全不同的角度（行為經濟學而非 NLP）檢驗 AI 的可靠性。三篇合在一起回答：金融 AI 在非理想條件下還能用嗎？

---

## 執行順序建議

```
Phase 1（快速產出）
├── D1 Calibration ← 最低計算成本，純統計分析
├── A5 MCQ Option Bias ← 實驗設計極簡，可立即開始
└── I3 Noise & Red Herrings ← Pilot study (50 題) 可快速驗證方法

Phase 2（核心建設）
├── A1 Open-Ended Benchmark ← 建設 A5 的完整版基礎設施
├── E1 Error Pattern Atlas ← 需大規模推論 + 人工標註
└── I1 Counterfactual Stress Test ← 需微擾生成 pipeline

Phase 3（高影響力）
├── D4 Overconfident AI ← 依賴 D1 數據，但政策影響力高
├── I2 Behavioral Biases ← 需設計 150 道情境題，工作量大但新穎度極高
└── H1 Multimodal ← 需圖表題建構，技術門檻高

Phase 4（理論封頂）
└── G2 Signaling Theory ← 依賴 G1 Ability Matrix，理論推導可先行
```

**依賴關係圖**：
```
D1 ──→ D4
A1 ←──→ A5（共享基礎設施，可平行）
E1 ←── I1, I3（E1 的 taxonomy 可擴展）
G1* ──→ G2（G1 不在本清單但為 G2 前置）
其餘皆獨立，可平行推進
```

---

## 投稿策略矩陣

| 論文 | 首選場所 | 備選場所 | 定位 |
|------|----------|----------|------|
| **A1** | EMNLP (Resources Track) | ACL, NeurIPS D&B | Benchmark + Resource |
| **A5** | ACL Findings | NAACL, EACL | Empirical Short Paper |
| **D1** | AAAI | IJCAI, AISTATS | Empirical + Methodology |
| **D4** | FAccT / AIES | Financial Innovation, AI & Ethics | Policy + Interdisciplinary |
| **E1** | EMNLP (Resources Track) | ACL, LREC-COLING | Data/Resource Paper |
| **H1** | ACL / EMNLP (Multimodal) | AAAI, NeurIPS | Benchmark + Empirical |
| **G2** | Management Science | QJE, Rev. Econ. Stat. | Theory + Empirical |
| **I1** | NeurIPS | ICML, EMNLP | Robustness + Methodology |
| **I2** | Nature Human Behaviour | J. Behav. Exp. Finance, AAAI | Interdisciplinary |
| **I3** | ACL / EMNLP (Robustness) | NeurIPS D&B, J. Fin. Data Sci. | Robustness + Empirical |

**跨場所策略**：
- CS/NLP 主場：A1, A5, E1, H1, I1, I3（技術導向）
- AI Safety/Policy：D4, I2（跨領域影響力）
- 經濟學/金融學：G2（理論導向）
- 全方位：D1（方法通用性強，多場所適用）

---

## 檔案索引

| 檔案 | 來源 | 說明 |
|------|------|------|
| `A1-open-ended-numerical.md` | ideas/ 複製 | 開放式數值推理基準 |
| `A5-mcq-option-bias.md` | ideas/ 複製 | 選項偏差量化 |
| `D1-calibration-selective-prediction.md` | ideas/ 複製 | 信心校準與選擇性預測 |
| `D4-overconfident-ai-regulation.md` | ideas/ 複製 | 過度自信 AI 風險分析 |
| `E1-error-pattern-atlas.md` | ideas/ 複製 | 錯誤圖譜 |
| `G2-signaling-theory.md` | ideas/ 複製 | 訊號理論 |
| `H1-multimodal-financial-reasoning.md` | ideas/ 複製 | 多模態金融推理 |
| `I1-counterfactual-stress-test.md` | 新建 | 反事實壓力測試 |
| `I2-behavioral-biases-llm.md` | 新建 | 行為金融學偏誤 |
| `I3-noise-red-herrings.md` | 新建 | 雜訊與紅鯡魚 |
