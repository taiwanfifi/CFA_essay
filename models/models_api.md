# MedEval-X 模型清單

> API keys 存放在 `medeval/.env`（已加入 .gitignore，不會上傳）

---

## Cloud Models（三家不同訓練資料 → 交叉驗證核心）

不同家族的模型用不同的訓練語料，等於「擁有不同知識背景的專家」。
三家同時判斷一道題，共識 ≥ 2/3 才通過，分歧大的才請醫師校正。

### OpenAI

| 模型 | Model ID | 角色 | 成本 | 備註 |
|------|----------|------|------|------|
| GPT-4o | `gpt-4o` | 出題 + 審題 | $2.5/$10 per MTok | 主力生成模型 |
| GPT-4o mini | `gpt-4o-mini` | 審題 | $0.15/$0.6 per MTok | 便宜的批量驗證 |

```python
from medeval.generation.models import OpenAIModel
model = OpenAIModel("gpt-4o")
```

### Anthropic (Claude)

| 模型 | Model ID | 角色 | 成本 | 備註 |
|------|----------|------|------|------|
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | 出題 + 審題 | $3/$15 per MTok | 主力驗證模型 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 審題 | 低 | 快速篩選 |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | 出題（困難題） | $5/$25 per MTok | 最強但最貴 |

```python
from medeval.generation.models import AnthropicModel
model = AnthropicModel("claude-sonnet-4-5-20250929")
```

### Google Gemini

| 模型 | Model ID | 角色 | 成本 | 備註 |
|------|----------|------|------|------|
| Gemini 2.5 Pro | `gemini-2.5-pro` | 出題 + 審題 | 付費 | Google 搜尋資料訓練，知識面獨特 |
| Gemini 2.5 Flash | `gemini-2.5-flash` | 審題 | 較低 | 快速驗證 |
| Gemini 3 Pro Preview | `gemini-3-pro-preview` | 出題 | 付費 | 最新版（preview） |

```python
from medeval.generation.models import GeminiModel
model = GeminiModel("gemini-2.5-pro")
```

---

## Local Models（Ollama — 額外知識來源）

本機已安裝的模型。各自的訓練資料也不同（DeepSeek 用中國語料、Qwen 用阿里巴巴語料、Llama 用 Meta 語料），進一步增加多樣性。

| 模型 | Ollama ID | 大小 | 強項 | 角色 |
|------|-----------|------|------|------|
| **DeepSeek-R1 14B** | `deepseek-r1:14b` | 9 GB | 推理能力強，CoT | 出題 + 審題 |
| **Qwen3 32B** | `qwen3:32b` | 20 GB | 多語言，中文強 | 出題 + 審題 |
| **Qwen3 4B** | `qwen3:4b` | 2.5 GB | 快速 | 快速審題 |
| **Llama 3.1 8B** | `llama3.1:8b` | 4.7 GB | 通用基線 | 出題 + 審題 |
| **Phi 3.5 3.8B** | `phi3.5:3.8b-mini-instruct-q4_K_M` | 2.4 GB | 小型但聰明 | 審題 |
| **Gemma 3** | `gemma3:latest` | 3.3 GB | Google 開源版 | 審題 |

```python
from medeval.generation.models import OllamaModel
model = OllamaModel("deepseek-r1:14b")
```

---

## 預設交叉驗證組合

### 組合 A：異家族 Cloud（預設，最可靠）

```
GPT-4o (OpenAI) + Claude Sonnet (Anthropic) + Gemini 2.5 Pro (Google)
```
- 三家訓練資料完全不同
- 共識 ≥ 2/3 → 自動通過
- 三家都不同意 → 標記「需人工審核」

### 組合 B：Cloud + Local 混合

```
GPT-4o + Claude Sonnet + DeepSeek-R1 14B
```
- 省 Gemini API 費用
- DeepSeek 推理能力強，且訓練語料又不同

### 組合 C：全 Local（零成本）

```
DeepSeek-R1 14B + Qwen3 32B + Llama 3.1 8B
```
- 不花 API 費用
- 品質可能不如 Cloud，但可做初步篩選
- 只有分歧項再送 Cloud 驗證 → 省錢

### 組合 D：速度優先

```
GPT-4o-mini + Claude Haiku + Gemini 2.5 Flash
```
- 全用便宜模型
- 適合 pilot test 或初步篩選

---

## 使用範例

### 一鍵啟動三模型交叉驗證

```python
from medeval.generation.models import OpenAIModel, AnthropicModel, GeminiModel
from medeval.generation.validator import MultiModelValidator

validator = MultiModelValidator([
    OpenAIModel("gpt-4o"),
    AnthropicModel("claude-sonnet-4-5-20250929"),
    GeminiModel("gemini-2.5-pro"),
])

# 驗證一批生成的題目
results = validator.validate_batch(items, orig_questions, orig_answers)
```

### 用 CLI 指定模型

```bash
# 用 GPT-4o 生成，三家 Cloud 驗證
python -m medeval.scripts.generate_benchmark \
    --module m4 --count 10 --pilot \
    --generator gpt-4o \
    --validators "claude-sonnet-4-5-20250929,gemini-2.5-pro,gpt-4o-mini" \
    --validate

# 用 DeepSeek 生成（免費），Cloud 驗證
python -m medeval.scripts.generate_benchmark \
    --module m4 --count 10 \
    --generator deepseek-r1:14b \
    --validators "gpt-4o,claude-sonnet-4-5-20250929,gemini-2.5-pro" \
    --validate
```

---

## 安裝依賴

```bash
pip install openai anthropic google-genai requests python-dotenv
```

## 為什麼多家模型交叉很重要？

```
OpenAI  → 訓練於 CommonCrawl + 書籍 + 程式碼
Anthropic → Constitutional AI + 不同的 RLHF 資料
Google  → Google 搜尋索引 + 學術文獻
DeepSeek → 中國語料 + 數學/推理強化
Qwen    → 阿里巴巴語料 + 多語言
Llama   → Meta 的開放語料

每家「讀的書不同」→ 知道的東西不同 → 互相檢查更可靠
```
