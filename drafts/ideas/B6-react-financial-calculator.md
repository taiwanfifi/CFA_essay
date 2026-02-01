# B6 ReAct 金融計算器代理
# ReAct Agent with Domain-Specific Financial Calculator Tools

## 研究問題

CFA 考試允許且鼓勵考生使用 HP-12C 或 BA II Plus 金融計算器，考題的設計預設了精確計算能力。然而 LLM 的數學計算是公認弱點：FinanceMath 基準測試中 GPT-4o+CoT 僅達 60.9%，與人類專家 92% 之間有 31% 的差距。本研究探討：為 LLM 配備領域特定金融計算器工具（非通用 Python interpreter），能否在計算題上縮小甚至消除這個差距？相比通用 code interpreter，domain-specific calculator 的優勢在哪裡？

## 核心方法

**五類金融計算器工具**

1. **TVM Calculator (Time Value of Money)**
   - PV, FV, PMT, N, I/Y 的互算
   - 支援 ordinary annuity / annuity due / perpetuity
   - 模擬 BA II Plus 的 TVM 功能

2. **Bond Calculator**
   - Bond price, YTM, current yield
   - Macaulay duration, modified duration, effective duration
   - Convexity 計算
   - 支援 semi-annual / annual coupon

3. **Statistics Calculator**
   - Portfolio return & risk (均值-方差框架)
   - Sharpe ratio, Treynor ratio, Jensen's alpha, Information ratio
   - Covariance, correlation matrix 計算

4. **Derivatives Calculator**
   - Black-Scholes option pricing (call & put)
   - Put-call parity 驗證與求解
   - Binomial option pricing (1-period, 2-period)

5. **Financial Ratio Calculator**
   - DuPont decomposition (3-factor & 5-factor)
   - Liquidity ratios (current, quick, cash)
   - EV/EBITDA, P/E, P/B, Dividend Yield

**ReAct Loop 設計**

```
Thought: [LLM 分析題意，決定需要哪個計算器]
Action: [選擇工具 + 提取參數]
  → BondPrice(face=1000, coupon=0.06, ytm=0.07, years=10, freq=2)
Observation: [計算器回傳結果] → 929.76
Thought: [LLM 解讀結果，判斷是否合理]
  → 債券價格 < 面值，因為 YTM > coupon rate，合理
Answer: [選擇最終答案] → C. $929.76
```

LLM 負責：理解題意、選擇工具、提取參數、解讀結果。Calculator 負責：精確數值計算。

## 實驗設計

- **Exp 1: 三方比較（核心實驗）**
  - Condition A: Pure LLM（無工具）
  - Condition B: LLM + Generic Python（LLM 自行撰寫 Python 計算代碼）
  - Condition C: LLM + Domain-Specific Calculator（本研究的金融計算器）
  - 按題目類型分析：概念題 / 計算題 / 分析題

- **Exp 2: Tool Selection & Parameter Extraction 評估**
  - Tool Selection Accuracy: LLM 是否選對了工具
  - Parameter Extraction Accuracy: LLM 是否正確提取並傳入參數
  - 錯誤分解：wrong tool / wrong parameter / unnecessary tool call / missed tool call

- **Exp 3: 計算器覆蓋率分析**
  - 分析五類計算器能覆蓋多少比例的 CFA 計算題
  - 識別未被覆蓋的計算類型，評估是否需要擴展工具集

- **Exp 4: 跨模型泛化性**
  - 測試不同 LLM（llama3.1:8b, qwen3:32b, gpt-4o）使用同一套計算器工具的效果
  - 分析：Tool Selection Accuracy 是否隨模型能力提升而提高

## 需要的積木

- ✅ CFA 測試資料集 — FinEval-CFA-Challenge (90), CFA-Easy (1,032)
- ✅ LLM 推論環境 — Ollama local + OpenAI API
- ✅ ReAct 框架基礎 — LangChain / LangGraph 支援 ReAct agent pattern
- ❌ TVM Calculator — Python 實作（~8hr）
- ❌ Bond Calculator — Python 實作（~10hr）
- ❌ Statistics Calculator — Python 實作（~8hr）
- ❌ Derivatives Calculator — Python 實作（~10hr）
- ❌ Financial Ratio Calculator — Python 實作（~6hr）
- ❌ Tool description prompts — 每個工具的 function schema + 使用範例
- ❌ 計算題標註 — 標記哪些題目需要數值計算（~10hr）

## 預期產出

- LLM + Financial Calculator 在計算題上準確率顯著提升（預期 +15-25%）
- LLM + Financial Calculator 略優於 LLM + Generic Python（預期 +3-8%），因為減少了 LLM 撰寫計算代碼的錯誤
- Tool Selection Accuracy 約 85-90%，Parameter Extraction 為主要錯誤來源
- 在概念題上三個 Condition 表現相近（工具不影響概念理解能力）
- 五類計算器預期覆蓋 70-80% 的 CFA 計算題

## 資料需求

| 資料集 | 用途 | 狀態 |
|--------|------|------|
| FinEval-CFA-Challenge (90) | 困難題測試 | 已就緒 |
| FinEval-CFA-Easy (1,032) | 主測試集 | 已就緒 |
| CFA_Extracted (1,124) | 輔助工具選擇分析 | 已就緒 |

## 模型需求

- **ReAct Agent LLM**: gpt-4o, qwen3:32b（需要較強的 tool-use 能力）
- **對比測試**: llama3.1:8b, deepseek-r1:14b（中等規模模型的 tool-use 能力）
- **注意**: 部分小模型可能不善於 function calling，這本身也是有價值的發現

## 狀態

🔲 尚未開始 — 金融計算器工具開發是主要工作量（~42hr），但技術風險低

## 可合併的點子

- **B1 (5-Stage Pipeline)** — Financial Calculator 直接插入 Stage 4 (Calculation Execution)
- **B2a/B2b (Multi-Agent)** — Calculator Agent 可直接復用本研究的工具集
- **B5 (Dual-Process)** — Calculator tools 作為 System 2 的計算組件
- CFA 考試的真實條件模擬：考生使用 HP-12C/BA II Plus，LLM 使用 domain-specific calculator

## 來源筆記

- docs/03-研究方向深度設計.md 方向 5：Financial Reasoning with Calculator Tool Augmentation
- ReAct (Yao et al., 2023) — Reasoning + Acting 框架
- FinanceMath 基準測試中 LLM 與人類 31% 的計算差距
- CFA Institute 允許的計算器：HP-12C, BA II Plus, BA II Plus Professional
