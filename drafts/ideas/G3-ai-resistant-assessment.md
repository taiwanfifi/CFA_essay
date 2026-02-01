# G3 未來 CFA 該考什麼？AI-Resistant Assessment Design
# AI-Resistant Assessment Design: Rethinking Professional Certification in the Age of Language Models

## 研究問題

如果 AI 能穩定地通過 CFA 考試中測量「可形式化能力」的題目，那麼未來的 CFA 考試應該測量什麼？怎麼測？本研究不是簡單地建議「考溝通力」——而是基於 G1 Ability Matrix 的實證數據，系統性地識別哪些能力維度在 AI 時代仍具有 signaling value，並提出具體的 assessment design 替代方案。核心論證：有效的 AI-resistant assessment 必須測量 AI 表現不穩定、prompt-sensitive、且跨模型不一致的能力——因為這些特性表明該能力尚未被 AI 商品化。

## 核心方法

**Phase 1: 從 G1 矩陣識別 AI-Resistant Abilities**

基於 G1 Ability Matrix 的 Layer 3 指標，建立三級分類：
- AI-Replaceable：AI Performance 高 + Stability 高 + Sensitivity 低 → Declarative Knowledge, Algorithmic Skill → 不再值得考
- AI-Assisted：Performance 中 + Stability 中 + Sensitivity 中 → Analytical Decomposition → 應在允許 AI 工具的條件下測量
- AI-Resistant：Performance 低 + Stability 低 + Sensitivity 高 → Integrative Judgment, Normative Reasoning, Stakeholder Reasoning → 未來認證核心

**Phase 2: 三種替代評量形式**

方案 A — Scenario-Based Interactive Assessment：動態情境互動，決策後情境演變。測量 Integrative Judgment。範例：客戶投資組合在市場衝擊後的即時重新配置。

方案 B — Responsibility-Bearing Decision Making：考生必須附上 accountability statement，不是「正確答案」而是「為什麼願意對建議負責」。測量 Normative Reasoning + Fiduciary Judgment。

方案 C — Stakeholder Interaction Evaluation：模擬多方利害關係人互動，同時平衡客戶需求、法規限制、公司利益。測量 Interpersonal Reasoning。

**Phase 3: 可行性分析** — 評估 scalability（CFA 全球 30 萬考生）、grading consistency、AI gaming risk。

## 實驗設計

1. **Expert Survey / Delphi Method**：邀請 CFA charterholders 與 assessment design 專家（5-10 人），對三方案進行多輪評估（validity, feasibility, fairness）。
2. **Prototype 開發**：每種方案開發 10 道 prototype 題目，小規模 pilot 測試。
3. **AI Resistance 驗證**：對 prototype 題目測試多個 LLM，確認新形式比傳統 MCQ 更 AI-resistant。
4. **現行 CFA 比較**：分析 CFA Level 3 essay/constructed response 題目在多大程度上已接近 AI-resistant。

## 需要的積木
- ✅ G1 Ability Matrix — AI-Replaceable / AI-Assisted / AI-Resistant 分類基礎
- ✅ G2 Signaling Theory — 理論論證
- ✅ CFA Institute 公開考試藍圖 — 現行評量架構
- ❌ Expert panel — 需招募 5-10 人
- ❌ Prototype 題目 — 需設計三種新形式的範例題目
- ❌ Pilot study 環境 — 小規模測試基礎設施

## 預期產出
- AI-Resistant Assessment Framework：系統性的評量設計指南
- 三種替代方案的 prototype 與 pilot 結果
- 從 G1 矩陣到政策建議的完整推導鏈
- 對 CFA Institute 及其他專業認證機構的能力權重重分配建議

## 資料需求
| 資料來源 | 用途 | 狀態 |
|----------|------|------|
| G1 Ability Matrix（完成版） | AI-Resistant 能力識別 | 需等待 G1 |
| G2 理論模型 | 政策建議的理論依據 | 需等待 G2 |
| CFA Institute Curriculum | 現行評量架構 | 公開可取得 |
| Expert survey 回覆 | Delphi Method 數據 | 需收集 |

## 模型需求
- 多個 LLM（GPT-4o, Claude, Ollama local models）：驗證 prototype 的 AI resistance
- 不需要 fine-tuning，純 inference

## 狀態
依賴 G1 與 G2 完成。等待期間可先收集 CFA Level 3 essay 範例並設計 prototype 初稿。

## 可合併的點子
- **G2 (Signaling Theory)** — G2 的理論直接導出 G3 的政策建議；可合併為 theory + policy 長論文
- **G4 (Cognitive Demand Taxonomy)** — 協助識別現行題目中已接近 AI-resistant 的部分
- **B7 (CoT Faithfulness)** — 若 CoT 在 judgment 題上不忠實，強化「MCQ 無法測量真正判斷力」論點

## 來源筆記
- drafts/archive/old-1-signaling-framework.md — Step 6：「未來 CFA 該考什麼」的實證推導
- G2 的 partial signaling collapse → 直接指向 assessment redesign 需求
- 定位為 educational policy paper，目標：Assessment in Education、Studies in Higher Education、Educational Researcher
