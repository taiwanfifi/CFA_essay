# I2 LLM 中的行為金融學偏誤
# Behavioral Finance Biases in Large Language Models: Do AIs Inherit Human Irrationality?

## 研究問題

行為金融學最核心的發現是：人類並非理性經濟人（homo economicus），而是系統性地受到認知偏誤影響。LLM 的訓練語料來自人類文本，因此可能繼承了這些非理性偏誤。這在金融場景中尤其危險：如果一個 Robo-Advisor 內建了 loss aversion（損失趨避）、anchoring（錨定效應）、herding（從眾效應）等偏誤，其投資建議將系統性地偏離最優決策。

本研究設計一組基於 Prospect Theory 和行為經濟學經典實驗的金融情境測試，量化 LLM 是否表現出已知的人類認知偏誤，並分析不同模型、不同 prompting 策略下偏誤程度的差異。

## 核心方法

### 測試的六種偏誤

**1. Loss Aversion（損失趨避）**
- 經典實驗：Kahneman & Tversky (1979) Prospect Theory
- 金融情境：等價的投資收益 vs 損失框架（framing effect），例如「某投資有 80% 機率獲利 $100」vs「某投資有 20% 機率損失 $400」（期望值相同）
- 測量：模型是否系統性偏好避免損失的選項？

**2. Anchoring Bias（錨定效應）**
- 金融情境：在估值題目前植入不同的數值錨點
- 例如：「某分析師估計股價為 $150」→ 模型估值偏向 $150 附近 vs 無錨點時的估值
- 測量：Anchor Distance = |有錨估值 - 無錨估值|

**3. Herding Effect（從眾效應）**
- 金融情境：注入「大多數分析師認為...」或「市場共識是...」
- 測量：社會證據（social proof）對模型判斷的影響程度
- 對照：正確答案與「共識」不一致時，模型是否跟隨共識而非獨立推理？

**4. Recency Bias（近因偏誤）**
- 金融情境：提供時間序列數據，測試模型是否過度加權近期數據
- 例如：近三個月下跌但長期趨勢上升的股票，模型的投資建議為何？
- 測量：模型回答中引用近期 vs 遠期數據的比例

**5. Overconfidence Bias（過度自信偏誤）**
- 與 D1/D4 互補：不只看 calibration，而是測試模型是否系統性地高估自己的預測精度
- 金融情境：要求模型給出 90% confidence interval，測量實際覆蓋率
- 測量：Calibration Error specifically on prediction intervals

**6. Disposition Effect（處置效應）**
- 金融情境：模擬持有盈利和虧損股票的投資組合，詢問賣出建議
- 經典預測：人類傾向過早賣出盈利股、過晚賣出虧損股
- 測量：模型是否展現相同的不對稱賣出傾向？

### 實驗框架

每種偏誤設計 20-30 道情境題，每道題製作：
- **Bias-inducing version**：包含偏誤誘導元素的版本
- **Neutral version**：移除偏誤誘導元素的對照版本
- **Rational baseline**：根據經濟學理論（Expected Utility Theory）的理性答案

核心指標：
- **Bias Score** = |模型回答 - 理性基線| / |偏誤誘導方向 - 理性基線|
  - 0 = 完全理性，1 = 完全受偏誤驅動
- **Bias Susceptibility Index** = 平均 Bias Score across all bias types
- **Debiasing Effectiveness** = (baseline Bias Score - post-intervention Bias Score) / baseline Bias Score

## 實驗設計

**實驗 1：基線偏誤測量**
- 6 種偏誤 × 25 道情境題 = 150 道題
- 8+ 模型分別測試 bias-inducing 和 neutral 版本
- 計算 per-model、per-bias-type 的 Bias Score

**實驗 2：Debiasing Interventions**
三種 prompt-level 干預策略的效果比較：
- **Strategy A — 明確提醒**：在 prompt 中加入「注意避免 [specific bias]」
- **Strategy B — 反向思考**：要求模型列出「支持相反結論的理由」後再回答
- **Strategy C — 角色扮演**：要求模型扮演「嚴格遵循 Expected Utility Theory 的理性投資人」
- 測量：哪種策略最能降低 Bias Score？

**實驗 3：與人類數據的對比**
- 收集行為金融學文獻中已知的人類偏誤基線數據
- 比較：LLM 的偏誤方向與人類一致嗎？程度更強還是更弱？
- 特別關注：是否存在「AI 獨有的偏誤」——人類不表現但 LLM 表現的非理性模式

**實驗 4：CoT 推理對偏誤的影響**
- 假說：Chain-of-Thought 推理可能 amplify 偏誤（模型在推理過程中 rationalize 偏誤決策）
- 對比：Direct answer vs CoT 在各偏誤上的 Bias Score
- 分析 CoT 推理文本中的偏誤 rationalization 模式

## 需要的積木
- ✅ OpenAI API + Ollama local models — 被測模型
- ✅ 行為經濟學文獻 — Kahneman & Tversky (1979), Thaler (1985), Shiller (2000)
- ❌ 150 道行為偏誤金融情境題 — 需設計與驗證（主要工作量）
- ❌ 理性基線計算 — 每道題需基於 Expected Utility Theory 推導理性答案
- ❌ 人類偏誤基線數據收集 — 需從行為金融學文獻中提取可比較的數據
- ❌ Debiasing prompt 模板 — 需設計三種干預策略的 prompt

## 預期產出
- `results/I2_bias_scores.json` — 每個模型 × 每種偏誤的 Bias Score
- `results/I2_debiasing_effectiveness.csv` — 三種干預策略的效果比較
- `results/I2_human_vs_llm_bias.csv` — 人類 vs LLM 偏誤程度對比
- `figures/I2_bias_radar_chart.png` — 每個模型的六維偏誤雷達圖
- `figures/I2_debiasing_comparison.png` — 干預前後 Bias Score 變化
- `figures/I2_cot_amplification.png` — CoT 對偏誤的放大/抑制效果
- Table: Most susceptible bias types ranked by average Bias Score across models

## 資料需求
- 自建 150 道行為偏誤金融情境題集（本研究的核心 resource contribution）
- 行為金融學文獻中的人類實驗數據（作為 benchmark）
- 不使用現有 CFA dataset——需專門設計以觸發特定偏誤的題目

## 模型需求
- OpenAI API: gpt-4o, gpt-4o-mini
- Ollama large: qwen3:32b, deepseek-r1:14b
- Ollama medium: llama3.1:8b
- Ollama small: qwen3:4b, phi3.5:3.8b
- 需覆蓋不同規模以測試偏誤是否隨模型變大而減少

## 狀態
Conceptual — 核心瓶頸是 150 道偏誤情境題的設計與理性基線的推導。建議先從 Loss Aversion 和 Anchoring 兩種最經典偏誤開始，各設計 10 道題進行 pilot study。

## 可合併的點子
- **D1** (Calibration)：Overconfidence Bias 的測量可直接使用 D1 的校準方法論
- **D4** (Overconfident AI)：I2 的 overconfidence 實驗提供 D4 的另一個切入角度
- **I1** (Counterfactual)：可測試微擾後模型的偏誤是否改變
- **G2** (Signaling Theory)：LLM 偏誤的發現為 G2 的「AI 不等於理性代理人」提供實證

## 來源筆記
- Kahneman, D. & Tversky, A. (1979). "Prospect Theory: An Analysis of Decision under Risk." Econometrica.
- Thaler, R. (1985). "Mental Accounting and Consumer Choice." Marketing Science.
- Shiller, R. (2000). "Irrational Exuberance." Princeton University Press.
- Hagendorff et al. (2023). "Human-like intuitive behavior and reasoning biases emerged in large language models but disappeared in ChatGPT." Nature Computational Science.
- 目標投稿場所：Nature Human Behaviour, Journal of Behavioral and Experimental Finance, AAAI (AI Safety track)
