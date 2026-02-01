# G2 AI 衝擊下的專業認證訊號理論
# Professional Certification Signaling Under AI Disruption: A Theoretical and Empirical Analysis

## 研究問題

When the cost of replicating certified cognitive skills approaches zero, the signaling value of standardized professional certification deteriorates. 具體而言：CFA 認證長期作為金融業 labor market 的 screening device，其有效性建立在「通過認證者具備稀缺認知能力」的前提上。當 AI 能以近乎零邊際成本複製其中部分認知能力時，這些能力的稀缺性消失，證照作為 signal 的價值隨之下降。本研究不是一篇測量論文——不測量 AI 多強——而是一篇理論 + 實證論文：建構 AI disruption 下專業認證 signaling 退化的理論模型，並以 G1 Ability Matrix 作為實證證據。研究單位（unit of analysis）是制度（institution），不是模型（model）。

## 核心方法

**理論框架：Modified Spence Signaling Model**

原始 Spence (1973) 模型中：
- Signal（訊號）= 教育投資 / 專業認證
- Signal value = f(cost of acquisition, ability correlation)
- 均衡條件：高能力者取得 signal 的成本低於低能力者，形成 separating equilibrium

本研究的修改：
- 引入 AI replication cost 參數 c_AI(s)：AI 複製能力 s 的邊際成本
- 當 c_AI(s) -> 0 時，能力 s 的稀缺性消失
- Signal value = f(scarcity of certified ability) = f(1 - AI_replicability)
- 區分 formalizable abilities（可形式化能力，c_AI -> 0）vs tacit abilities（隱性能力，c_AI 仍高）
- 推導出 partial signaling collapse：證照的訊號價值不是全面崩潰，而是在特定能力維度上選擇性退化

**與 Autor (2003) Task-based Framework 的銜接**

將 CFA 測量的認知能力映射到 Autor 的 task 分類：
- Routine Cognitive Tasks（對應 Declarative Knowledge, Algorithmic Skill）→ 最易被 AI 複製
- Non-routine Analytical Tasks（對應 Analytical Decomposition）→ 部分可被複製
- Non-routine Interactive Tasks（對應 Integrative Judgment, Stakeholder Reasoning）→ 最難被複製

**與 Becker (1964) Human Capital Theory 的對話**

AI 不是消滅 human capital，而是改變其組成結構：
- General human capital（通用知識）的市場價值因 AI 而下降
- Specific human capital（情境判斷、人際推理）的相對價值上升
- 證照制度若仍側重前者，則其作為 human capital 指標的效度（validity）下降

## 實驗設計

1. **理論模型推導**：形式化 Modified Spence Model，推導 partial signaling collapse 的均衡條件，識別 tipping point（AI replicability 達到什麼水準時 signal 開始失效）。
2. **實證驗證**：使用 G1 Ability Matrix 的數據，計算每種 Ability Type 的 Signaling Value Retention。驗證理論預測：formalizable abilities 的 signaling value 顯著低於 tacit abilities。
3. **跨認證比較（如可行）**：將分析框架擴展至其他專業認證（USMLE、Bar Exam），測試理論的通用性。
4. **制度動態分析**：基於 AI 能力的 scaling 趨勢，模擬未來 3-5 年 CFA signaling value 的退化軌跡。

## 需要的積木
- ✅ 理論文獻 — Spence (1973), Becker (1964), Autor et al. (2003) 均為經典文獻
- ✅ CFA 制度背景 — CFA Institute 公開的 curriculum framework 與 competency standards
- ❌ G1 Ability Matrix 完成版 — 需等待 G1 完成以提供實證數據
- ❌ 形式化理論模型 — 需推導 Modified Spence Model 的數學表述
- ❌ 跨認證資料 — USMLE/Bar Exam 的能力框架（用於通用性驗證，非必需）

## 預期產出
- Modified Spence Signaling Model：首個形式化 AI disruption 下專業認證訊號退化的理論模型
- Partial signaling collapse 定理：證明信號退化是選擇性的，非全面的
- Tipping point 分析：AI replicability 的臨界值
- 政策含義：對 CFA Institute 及其他專業認證機構的制度設計建議
- 為 G3（AI-Resistant Assessment Design）提供理論基礎

## 資料需求
| 資料來源 | 用途 | 狀態 |
|----------|------|------|
| G1 Ability Matrix | 實證證據（Layer 3 指標） | 需等待 G1 完成 |
| CFA Institute Curriculum | 能力框架背景 | 公開可取得 |
| Spence/Becker/Autor 原始論文 | 理論推導基礎 | 已取得 |
| Labor market data（可選） | 驗證 CFA 持證者薪資溢價變化 | 需另行收集 |

## 模型需求
- 本研究不需要 LLM 推論——所有 AI performance 數據來自 G1 矩陣
- 若進行 tipping point 模擬，需基本的數值模擬環境（Python/R 即可）

## 狀態
理論框架可先行推導，但實證驗證需等待 G1 Ability Matrix。建議在其他實驗論文進行期間，同步推進理論模型的數學表述。

## 可合併的點子
- **G1 (Ability Matrix)** — G2 的實證基礎完全依賴 G1
- **G3 (AI-Resistant Assessment)** — G2 的理論模型直接導出 G3 的政策建議
- G2 + G3 可合併為一篇長論文（理論 + 政策），但分開發表可投不同領域期刊

## 來源筆記
- drafts/archive/old-1-signaling-framework.md — D-type 論文的完整推導過程，包含「研究單位是制度不是模型」的關鍵洞察
- Spence, M. (1973). Job market signaling. Quarterly Journal of Economics.
- Becker, G. S. (1964). Human Capital. University of Chicago Press.
- Autor, D. H., Levy, F., & Murnane, R. J. (2003). The skill content of recent technological change. Quarterly Journal of Economics.
- 目標發表場所：Management Science (Technology Track)、Journal of Finance (education/policy)、Review of Economics and Statistics
