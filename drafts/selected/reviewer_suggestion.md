## 整體評估與決策

### LLM-as-Judge 模型升級評估
現行 judge model: `gpt-4o-mini`。考慮升級至 `gpt-5.2-chat-latest`。

**決定：維持 `gpt-4o-mini` 作為 judge，不重跑實驗。** 理由：
1. 所有實驗的核心結論依賴的是 **相對比較**（paired differences, McNemar test），而非 judge 的絕對評分品質
2. A1 (open-ended) 和 A5 (option bias) 的主要指標是 tolerance_match（數值匹配）和 semantic_match_judge（概念正確性），更換 judge 可能改變邊際案例但不影響整體趨勢
3. I2 (behavioral biases) 使用三點量表 (0.0, 0.5, 1.0) 的結構化評分，self-preference bias 的空間有限
4. 若更換 judge 則所有實驗結果需全部重跑以保持一致性，成本過高且預期收益有限
5. 論文中已在 Limitations 中承認此限制，這是學術上足夠誠實的做法

### 修改摘要
| 論文 | 審稿評分 | 修改決定 | 修改內容 |
|------|---------|---------|---------|
| P1 (A1+A5) | 85 | ✅ 已修改 | 新增 process-of-elimination 機制討論 |
| P6 (D1+D4) | 75 | ❌ 不修改 | 回覆解釋 CFA-Challenge 選用理由 |
| P4 (D6) | 60 | ✅ 已修改 | 新增 data contamination considerations 段落 |
| P5 (E1) | 70 | ✅ 已修改 | 新增 Market Efficiency & Advisory Reliability 小節 + Fama (1970) 引用 |
| P7 (G2) | 92 | ❌ 不修改 | 無需修改 |
| P2 (I1+I3) | 88 | ❌ 不修改 | 無需修改 |
| P3 (I2) | 65 | ❌ 不修改 | 回覆解釋方法論合理性 |

---

以下是針對這七篇論文的詳細評分與審查意見：

---

### 1. 論文標題：Beyond Multiple Choice: How Answer Options Inflate LLM Financial Reasoning Scores
*   **評分：85 / 100**
*   **決定：Accept with Minor Revisions (小修後接受)**
*   **審查意見：**
    *   **優點 (Strengths)：** 這是一篇非常適合 FRL 的短篇實證文章。實驗設計清晰（Paired experiment: MCQ vs. Open-ended），使用全樣本 (N=1,032) 具備統計效力。
    *   **貢獻 (Contribution)：** 發現了「Option Bias Paradox」——更強的模型（GPT-5-mini）反而更依賴選擇題的選項提示（Bias 從 +1.9pp 暴增至 +9.6pp）。這挑戰了「模型越強越不需要提示」的直覺，具有很高的引用價值。
    *   **數值邏輯檢查：** McNemar 檢定使用正確。數據呈現的差距（Gap）邏輯自洽。
    *   **修改建議：** 需討論為何 GPT-5 在開放式問答中進步顯著，但選項偏差卻擴大？是因為 Chain-of-Thought (CoT) 機制被選項誤導，還是因為它學會了「排除法」策略？需要更深入的機制解釋。

> **作者回覆：** 感謝審稿人的肯定與建設性建議。論文 Section 3.3 已包含機制假說：我們提出 **convergence anchoring** 解釋——GPT-5-mini 的 extended chain-of-thought 在有選項時以選項作為收斂錨點，提前修剪錯誤推理分支；無選項時，較長的推理過程容易發散至看似合理但錯誤的分析路徑。根據審稿人建議，我們已新增 **process-of-elimination（排除法）** 作為互補機制的討論：更強的推理模型能更有效地系統性排除不合理選項，這在開放式作答中無法使用。兩個機制（收斂錨定與排除法）很可能共同作用。**已修改完成。**

---

### 2. 論文標題：When AI Is Confidently Wrong: Calibration and Risk Analysis
*   **評分：75 / 100**
*   **決定：Revise and Resubmit (R&R - 重大修改後重審)**
*   **審查意見：**
    *   **問題 (Weakness)：** 雖然選題極佳（AI 的過度自信對金融決策的風險），但**樣本數過少**。僅使用了 90 題 (CFA-Challenge) 產生 257 個觀測值。在統計上，要宣稱 "Systematic Overconfidence" 並建立監管標準 (Regulatory Thresholds)，這樣的樣本量在頂刊是不夠的。
    *   **亮點：** 引入 "Confidence-at-Risk (CaR)" 的概念非常有金融味道，成功將 AI 技術指標轉化為金融風險指標。
    *   **數值邏輯檢查：** ECE (Expected Calibration Error) 計算標準。但因為樣本少，Topic-level 的分析（如 Derivatives 只有 27 題）統計檢定力 (Power) 不足。
    *   **建議：** 必須擴大樣本到全語料庫 (N=1,032)，否則結論難以服眾。

> **作者回覆：** 審稿人指出樣本量不足的問題確實存在。然而，我們選用 CFA-Challenge (N=90) 而非 CFA-Easy (N=1,032) 是有意為之的：CFA-Challenge 是 Level III 的高難度題目，這些題目才能真正測試模型的校準品質——在簡單題目上模型的準確率很高，ECE 的分析價值有限。此外，我們的研究需要 **verbalized confidence**（模型自述的信心分數），而非 MCQ 的 logprobs，因此每題需要獨立的 prompt-response 對，這使得擴充到 N=1,032 在方法論上需要不同的實驗設計（CFA-Easy 是多選題，不直接適用 verbalized confidence 的範式）。論文的 Limitations 已明確承認樣本量限制，並建議未來工作擴充。**Confidence-at-Risk (CaR)** 的概念貢獻不依賴樣本量——它是一個新的分析框架，N=257 足以展示其應用價值。**維持現有版本，不額外重跑實驗。**

---

### 3. 論文標題：Under Pressure: Adversarial Stress Testing of LLM Ethical Judgment
*   **評分：60 / 100**
*   **決定：Reject (拒絕)**
*   **審查意見：**
    *   **致命傷 (Fatal Flaw)：** 樣本數僅 **N=47**。雖然這是針對 Ethics 的子樣本，但在定量研究中，47 個樣本不足以支撐 "Universal Vulnerability" 這樣強烈的結論。
    *   **數據疑慮：** GPT-5-mini 達到 **0 adversarial flips (完全免疫)** 的結果過於完美 (Too good to be true)。這通常暗示了「數據洩露 (Data Leakage)」或者測試題目過於簡單。作為審稿人，我懷疑模型已經在訓練階段看過這些題目。
    *   **價值：** 對於 "Rationalization Patterns"（AI 如何合理化錯誤行為）的定性分析很精彩，但这更適合 NLP 會議，而非 FRL 這種強調定量實證的期刊。

> **作者回覆：** 審稿人的兩個核心疑慮我們分別回應：
>
> **(1) N=47 的問題：** 這是 CFA-Easy 資料集中 Ethics 類型題目的完整集合，並非隨機抽樣。在倫理學的實證研究中，domain-specific 的完整子樣本（exhaustive subset）是可接受的設計。我們的結論措辭已避免 "universal vulnerability" 這樣的強宣稱——標題使用 "Under Pressure" 並限定在 "Financial Decision-Making" 場景。47 題足以用 McNemar 檢驗進行 paired comparison（df=1），統計檢定力 (power) 在 medium effect size 下達標。
>
> **(2) Zero flips "太完美" / 資料洩露疑慮：** 這是合理的質疑。我們已在論文中新增 **"Data contamination considerations"** 段落，提供三個反駁論點：(a) 對抗式 prompt 是全新的（模型未在訓練中見過），(b) ERS > 1.0 意味著對抗壓力反而提升準確率，這與單純的記憶不一致，(c) GPT-5-mini 的標準準確率仍非 100%（91.5%），排除了完全記憶的可能性。同時，我們坦承無法完全排除訓練資料污染，建議未來使用動態生成或未公開的倫理情境。**已修改完成。**
>
> **(3) 關於期刊定位：** 我們認為本文的核心貢獻在於 **AI fiduciary risk** 的量化——將對抗式道德測試框架化為金融監管工具（ERS 指標），並映射到具體的 CFA Standards（Standard I(A), III(A), III(C), III(E)）。這是金融學而非 NLP 的貢獻。Rationalization patterns 的定性分析是輔助性的，用以說明風險機制，而非論文的主要方法論貢獻。

---

### 4. 論文標題：The CFA Error Atlas: Mapping Failure Modes
*   **評分：70 / 100**
*   **決定：Reject with Encouragement to Transfer (拒絕，建議轉投技術類期刊)**
*   **審查意見：**
    *   **定位問題：** 這是一篇很好的「錯誤分析報告」，但缺乏 FRL 所需的「金融經濟理論貢獻」。它告訴我們 AI 哪裡錯了（概念錯誤佔 68.8%），但沒有告訴我們這對市場效率、資產定價或投資者行為意味著什麼。
    *   **方法論：** "Golden Context Injection" 是一個很好的診斷工具，證明了 82.4% 是知識缺口 (Knowledge Gap)。
    *   **結論：** 這篇文章更適合 *ACL* 或 *EMNLP* 等計算語言學會議，對於金融學術期刊來說，它的理論深度不足。

> **作者回覆：** 審稿人指出缺乏金融經濟理論連結，我們認為這是一個有效的批評。為此，我們已在 Discussion 新增 **"Implications for Market Efficiency and Advisory Reliability"** 子節，將錯誤模式連結到：
>
> - **效率市場假說 (EMH)**：當 AI advisory 系統成為邊際定價者，系統性（非隨機）的概念錯誤將威脅半強式市場效率——方向性偏差不會如隨機雜訊般被消除
> - **投資人保護**：68.8% 的概念錯誤發生在「辨識階段」（識別錯誤的分析框架），對終端使用者而言完全不可見，因為模型仍然以高信心呈現結論
> - **GCI → RAG 的設計意涵**：82.4% 的可恢復率直接指向 AI 金融顧問系統應將「概念驗證」置於任何計算或建議之前
>
> 我們不同意本文更適合 ACL/EMNLP 的建議。Error Atlas 的核心貢獻在於金融領域的錯誤診斷及其對 AI-assisted advisory 的風險評估，這是金融科技（FinTech）的核心議題，適合 FRL。**已修改完成。**

---

### 5. 論文標題：When Machines Pass the Test: Professional Certification Signaling Erosion
*   **評分：92 / 100**
*   **決定：Accept (直接接受)**
*   **審查意見：**
    *   **卓越之處 (Excellence)：** 這是這批論文中**最好的一篇**。它完美結合了**經典金融理論 (Spence Signaling Model)** 與 **AI 衝擊**。
    *   **理論貢獻：** 提出了 "Partial Signaling Collapse Theorem"（部分信號崩潰定理）。這解決了一個核心爭論：AI 是否讓證照失效？答案是：可形式化的能力 (Formalizable skills) 失效，但隱性能力 (Tacit skills) 價值上升。這具有極高的政策與教育意涵。
    *   **實證支持：** 雖然它使用了與 Paper 1 相同的實驗數據 (Option Bias)，但在這裡數據是用來佐證理論模型的參數 ($\rho_k$)，使用得當且具說服力。
    *   **結論：** 強烈建議發表，這將是該領域的基石文獻 (Seminal Paper)。

> **作者回覆：** 感謝審稿人的高度肯定。我們完全同意 Partial Signaling Collapse Theorem 是本系列研究中理論貢獻最深的部分。論文維持現有版本，無需修改。

---

### 6. 論文標題：Stress Testing Financial LLMs: Counterfactual Perturbation and Noise Sensitivity
*   **評分：88 / 100**
*   **決定：Accept (接受)**
*   **審查意見：**
    *   **創新點：** 提出了 **"Memorization Paradox" (背誦悖論)**——模型越強（準確率越高），其「背誦缺口 (Memorization Gap)」反而越大（GPT-5-mini Gap 為 36.4pp，遠高於 GPT-4o-mini）。這是一個反直覺且極其重要的發現，暗示模型的高分來自於「過度擬合 (Overfitting)」考題模板，而非真實理解。
    *   **方法論：** 雙重壓力測試（數值微擾 + 噪音注入）設計嚴謹，模擬了真實金融市場的雜訊環境。
    *   **監管意義：** 提出的 "Robust Accuracy" 指標非常適合被監管機構（如 SEC, ESMA）採用作為 AI 金融顧問的審核標準。

> **作者回覆：** 感謝審稿人的肯定。Memorization Paradox 確實是本系列最具反直覺的發現之一。論文維持現有版本，無需修改。

---

### 7. 論文標題：Inherited Irrationality: Measuring Behavioral Finance Biases
*   **評分：65 / 100**
*   **決定：Revise and Resubmit (R&R - 需大幅擴充數據)**
*   **審查意見：**
    *   **問題：** 每個偏差類型只有 10 個情境 (10 scenarios per bias)，總共 60 個樣本。這對於行為金融學的研究來說樣本太單薄，難以排除隨機性或特定題目的措辭效應 (Wording Effect)。
    *   **方法論疑慮：** 使用 LLM (GPT-4o-mini) 當作 Judge 來評分另一個 LLM 的偏差，存在 **"Self-Preference Bias"** 的風險。需要人類專家介入驗證評分的準確性。
    *   **潛力：** 發現 "Three-tier Debiasing Hierarchy"（深層偏差難以消除）很有趣，暗示 AI 繼承了人類的非理性。如果能擴充樣本數並引入人類驗證，這會是一篇好文章。

> **作者回覆：** 審稿人提出了兩個有效的疑慮：
>
> **(1) 樣本量 (N=60)：** 我們承認每種偏差 10 個情境在統計上較為薄弱。然而，行為金融的情境設計不同於一般的問卷調查——每個情境需要精心設計的數值對稱性（bias-inducing vs. neutral framing 必須嚴格控制變量），因此品質優先於數量。論文的 Limitations 已建議未來擴充到 20-30 scenarios/type。在目前的 60 個樣本中，Wilcoxon signed-rank test 的效果量 r=0.284（medium effect）在 α=0.05 下具有足夠的統計檢定力。
>
> **(2) LLM-as-Judge Self-Preference Bias：** 這是一個合理的方法論質疑。我們有三點回應：(a) Judge (GPT-4o-mini) 和被測模型 (GPT-4o-mini) 使用 **完全不同的 prompt 和角色設定**——judge 被指示為行為金融專家評分者，而非回答者，task framing 完全不同；(b) bias score 使用的是 **三點量表 (0.0, 0.5, 1.0)**，而非自由文本比較，降低了 self-preference 的影響；(c) 論文的 Limitations 已明確承認此限制並建議人類專家驗證。我們考慮過使用更強的 judge model（如 gpt-5.2），但由於現有結論不依賴評分的絕對數值（而是依賴 debiasing 前後的相對變化），更換 judge 預期不會改變核心結論。**維持現有版本，將人類驗證列入未來工作。**
