# FinDAP 框架解析

本文件為 FinDAP 論文與框架的技術解析，聚焦於架構設計、程式碼實作與研究局限。
資料集的詳細描述請參閱 `01` 號文件，本文不再重複。

---

## 一、論文基本資訊

| 項目 | 內容 |
|------|------|
| 標題 | Demystifying Domain-adaptive Post-training for Financial LLMs |
| 會議 | EMNLP 2025 (Oral Presentation) |
| 作者 | Zixuan Ke, Yifei Ming, Xuan-Phi Nguyen, Caiming Xiong, Shafiq Joty |
| 機構 | Salesforce AI Research |
| arXiv | 2501.04961 |
| ACL Anthology | https://aclanthology.org/2025.emnlp-main.1579/ |
| GitHub | https://github.com/SalesforceAIResearch/FinDap |
| 產出模型 | Llama-Fin-8b (基於 Meta-Llama-3-8B-Instruct，8B 參數) |

---

## 二、框架總覽：四大元件

FinDAP 的核心貢獻在於提出一套系統性的 domain-adaptive post-training 方法論，
由四個相互依存的元件組成：

```
FinDAP Framework
+-- FinCap  (能力定義)     --> 定義金融 LLM 需要什麼能力
+-- FinRec  (訓練方案)     --> 怎麼訓練才能獲得這些能力
+-- FinTrain (訓練資料)    --> 用什麼資料來訓練
+-- FinEval  (評估體系)    --> 怎麼衡量訓練效果
```

以下逐一解析。

---

### 2.1 FinCap: Financial Capabilities

FinCap 定義了金融 LLM 的四個核心能力維度：

| 維度 | 英文名稱 | 含義 |
|------|----------|------|
| 金融概念 | Financial Concepts | 理解金融術語、定義、原理 |
| 金融任務 | Financial Tasks | 執行 NER、情感分析、分類等具體任務 |
| 金融推理 | Financial Reasoning | 多步驟數值計算、邏輯推導 |
| 指令遵循 | Instruction Following | 按照指令格式正確回應 |

這個能力分層架構的意義在於：它為後續的訓練方案設計提供了明確的目標，
也為評估體系提供了多維度的量測框架。論文的一個重要發現是，
不同訓練階段對不同能力維度的貢獻並不相同（詳見第五節）。

---

### 2.2 FinRec: Financial Recipes (三階段訓練方案)

這是 FinDAP 最核心的技術貢獻。訓練分為三個階段：

#### Stage 1: Joint CPT + SFT (從基礎模型開始)

- **CPT (Continued Pre-training)**: 非監督式的金融文本續訓
- **SFT (Supervised Fine-tuning)**: 監督式的指令微調
- **關鍵設計**: CPT 與 SFT 聯合訓練，而非先 CPT 再 SFT

聯合訓練的技術理由：傳統的先 CPT 再 SFT 流程會導致 catastrophic forgetting。
當模型經過大量非監督文本的 CPT 後，其指令遵循能力會顯著退化。
FinDAP 透過將 CPT 與 SFT 的資料混合在同一訓練過程中，
讓模型在吸收領域知識的同時維持指令遵循能力。

在實作上，使用 downsampling 將 CPT 資料量縮減至與 SFT 資料量一致，
然後 shuffle 混合進行訓練。

#### Stage 2: Curriculum Learning (從 Stage 1 checkpoint 繼續)

- 以 Stage 1 的輸出模型為基礎，進行更進階的課程學習
- 使用更高的 warmup ratio (0.5 vs 預設 0.1)
- 繼續 joint CPT + SFT 但使用更難的資料分布
- 從已有的 checkpoint 繼續訓練 (resume_from_checkpoint)

#### Stage 3: Preference Alignment with RPO

- **RPO (Robust Policy Optimization)**: 結合 DPO 與 SFT loss 的偏好對齊方法
- **Dual-signal preference**: 同時使用 outcome signal 和 process signal
- **Stepwise corrective preference**: 逐步修正的偏好資料構建
- **Generative reward model**: 使用生成式獎勵模型評估回應品質

RPO 的核心公式是在 DPO loss 基礎上加入 SFT loss 項，由 `rpo_alpha` 控制權重。
在程式碼中，`DPOConfig(rpo_alpha=1)` 即啟用 RPO，將 SFT loss 以等權重加入。

---

### 2.3 FinTrain: 訓練資料集

| 資料集 | 樣本數 | 類型 | 用途 |
|--------|--------|------|------|
| apex_instruct | 1.47M | 通用指令 | SFT (指令遵循) |
| book_fineweb | 4,500 | 非監督金融文本 | CPT (領域知識) |
| cfa_exercise | 2,946 | CFA Level II 練習題 | SFT (金融推理) |

資料來源為 SchweserNotes 2020 等教材，非官方 CFA Institute 考題。
詳細資料集描述請參閱 `01` 號文件。

---

### 2.4 FinEval: 評估體系

FinEval 的設計特點是多維度評估：

| 維度 | 分類 | 說明 |
|------|------|------|
| 任務相似度 | Similar / Novel | 評估資料是否與訓練資料分布相似 |
| 領域類型 | General / Domain-Specific / Reasoning | 通用能力、領域知識、推理能力 |
| 回答方式 | Direct Answer / Chain-of-Thought | 直接作答 vs 推理鏈 |

評估基準：

| 基準 | 樣本數 | 難度 | 說明 |
|------|--------|------|------|
| CFA-Challenge | 90 | 高 | 具有挑戰性的 CFA 題目 |
| CFA-Easy | 1,032 | 中 | 較容易的 CFA 題目 |
| CRA-Bigdata | 1,472 | 中 | 金融推理任務 |

---

## 三、程式碼架構解析

### 3.1 目錄結構

本地倉庫位於 `datasets/FinDap/FinDAP/`，其核心結構如下：

```
datasets/FinDap/FinDAP/
+-- posttrain.py                  # 主程式入口
+-- config.py                     # 參數定義
+-- approaches/
|   +-- posttrain.py              # SFT / DPO-RPO trainer 實作
+-- utils/
|   +-- prepare.py                # PosttrainPreparer: 資料載入、模型初始化
|   +-- model.py                  # 模型工具、checkpoint 轉換
|   +-- common.py                 # 共用工具
|   +-- packing/
|       +-- packed_dataset.py     # 序列打包 Dataset 實作
|       +-- monkey_patch_packing.py  # Flash Attention monkey-patch
+-- dataloader/
|   +-- data.py                   # 資料集載入 (從 HuggingFace Hub)
+-- yaml/
|   +-- fsdp_config_{2,4,8,16}.yaml  # FSDP 分散式訓練設定
+-- scripts/
|   +-- cpt_sft/                  # Stage 1 & 2 訓練腳本
|   +-- offline_rl/               # Stage 3 訓練腳本
+-- fineval.py                    # 評估框架
```

### 3.2 主程式入口: posttrain.py

`posttrain.py` 的 `main()` 函數根據參數選擇三條程式路徑：

```
args = parsing_posttrain()
prepare_approach = PosttrainPreparer(args)

if args.convert_checkpoint_to_ckpt:
    --> checkpoint 格式轉換 (不進行訓練)

elif args.use_trainer:
    if 'dpo' in args.idrandom:
        --> DPO/RPO trainer (Stage 3)
    else:
        --> SFT trainer (Stage 1 & 2)
```

`idrandom` 參數是訓練模式的核心控制變數，它同時決定：
1. 使用哪條訓練路徑 (SFT vs DPO)
2. 載入哪些資料集
3. 資料集的組合方式

### 3.3 資料載入機制: dataloader/data.py

所有訓練資料都預先 tokenize 後上傳至 HuggingFace Hub，
在 `ZixuanKe/` namespace 下。載入時直接使用 `load_dataset()` 從 Hub 拉取。

程式碼中定義了兩個 mapping：
- `tokenized_trainer_map`: CPT/SFT 資料集名稱到 Hub 路徑的映射
- `dpo_trainer_map`: DPO/RPO 偏好資料集名稱到 Hub 路徑的映射

這表示所有資料前處理（tokenization、格式轉換）都已在離線完成，
訓練時不需要任何本地資料處理。

### 3.4 PosttrainPreparer: 訓練準備器

`PosttrainPreparer` (位於 `utils/prepare.py`) 是整個訓練流程的中樞，
負責以下工作：

1. **序列解析** (`prepare_sequence`): 從 `sequences` 文件讀取資料集序列，
   根據 `idrandom` 參數查找對應的序列索引

2. **模型載入** (`load_model_tok`): 載入預訓練模型與 tokenizer，
   啟用 Flash Attention 2，對於 DPO 任務同時載入 reference model

3. **訓練配置**: 根據訓練模式建立 `SFTConfig` 或 `DPOConfig`

4. **資料準備** (`prepare_posttrain`): 根據 `idrandom` 分支處理：
   - 若包含 `'sft'` 和 `'dapt'`: 混合 CPT+SFT 資料，
     使用 downsampling/upsampling 平衡資料量
   - 若僅包含 `'sft'`: 純 SFT 訓練
   - 若包含 `'dpo'`: 載入偏好資料 (chosen/rejected pairs)

### 3.5 序列打包: Packing 機制

FinDAP 使用序列打包 (sequence packing) 來提高訓練效率。
此機制包含兩個關鍵技術：

#### PackedDataset

`packed_dataset.py` 中的 `PackedDataset` 類別將多個短序列打包進單一 `max_seq_length` 的序列中：

- `pack_data_points_by_length()`: 基於貪心策略，將連續的短序列合併，
  直到總長度接近 `max_seq_length`
- `pack_data_points_FA()`: 將合併後的序列轉為 Flash Attention 可用的格式，
  使用遞增整數的 `attention_mask`（1, 2, 3...）來區分不同原始序列

#### Monkey-patch Flash Attention

`monkey_patch_packing.py` 透過替換 transformers 內部的 `_get_unpad_data` 函數，
讓 Flash Attention 能正確處理打包序列中的注意力隔離。

原始的 `_get_unpad_data` 假設 attention_mask 為 0/1 二值，
修改後的版本能處理多值 attention_mask（每個打包序列用不同的正整數標記），
從而在一個 batch 內同時處理多個互不干擾的序列。

支援的模型架構：Llama, Mistral, Mixtral, Qwen2, Phi3。

### 3.6 關鍵訓練參數

從 `config.py` 與訓練腳本中提取的重要參數：

| 參數 | 類型 | 說明 |
|------|------|------|
| `--use_trainer` | flag | 必要參數，啟用 HuggingFace Trainer |
| `--idrandom` | str | 訓練模式與資料集選擇的核心控制變數 |
| `--instruction_mask` | flag | 對指令部分的 token 進行 loss masking |
| `--isolate_attention` | flag | 打包序列間的注意力隔離 |
| `--use_flash_attention_2` | flag | 啟用 Flash Attention 2 |
| `--use_rpo` | flag | 啟用 Robust Policy Optimization |
| `--downsample` | flag | CPT 資料 downsample 至 SFT 資料量 |
| `--max_seq_length` | int | 最大序列長度 (Stage 1-2: 8000, Stage 3: 2048) |
| `--learning_rate` | float | 學習率 (Stage 1-2: 5e-6, Stage 3: 5e-7) |
| `--checkpointing_steps` | int | checkpoint 儲存間隔 |
| `--warmup_proportion` | float | warmup 比例 (Stage 2 使用 0.5) |

### 3.7 三階段訓練腳本對比

| 項目 | Stage 1 | Stage 2 | Stage 3 |
|------|---------|---------|---------|
| 腳本 | `mix_cpt_mix_sft_..._from_base.sh` | `mix_cpt_mix_sft_..._from_v1.sh` | `rpo_cfa_stepwise.sh` |
| 基礎模型 | `Meta-Llama-3-8B-Instruct` | Stage 1 checkpoint | Stage 2 checkpoint |
| idrandom | `dapt_mix_sft_mix_full_extend_exercise_book` | 同 Stage 1 | `dpo_cfa_sample_from_policy_stepwise` |
| Learning Rate | 5e-6 | 5e-6 | 5e-7 |
| Max Seq Length | 8000 | 8000 | 2048 |
| Warmup | 0.1 (預設) | 0.5 | 0.1 (預設) |
| Checkpoint Steps | 1000 | 500 | 250 |
| 特殊設定 | `--downsample` | `--resume_from_checkpoint` | `--use_rpo` |
| FSDP 配置 | 16 GPUs | 16 GPUs | 16 GPUs |

---

## 四、RPO 偏好對齊的技術細節

### 4.1 RPO vs DPO

DPO (Direct Preference Optimization) 的標準做法是最小化偏好對之間的 loss：

```
L_DPO = -log(sigma(beta * (log(pi/pi_ref)(chosen) - log(pi/pi_ref)(rejected))))
```

RPO 在此基礎上增加一個 SFT loss 項：

```
L_RPO = L_DPO + rpo_alpha * L_SFT(chosen)
```

其中 `rpo_alpha` 控制 SFT loss 的權重。在 FinDAP 的實作中 `rpo_alpha=1`，
即 DPO loss 與 SFT loss 等權重。
這確保模型在學習偏好的同時不會偏離 chosen response 的分布太遠。

### 4.2 Dual-signal Preference

FinDAP 的偏好資料構建使用雙重信號：

1. **Outcome signal**: 最終答案的正確性 (binary: correct/incorrect)
2. **Process signal**: 推理過程的品質 (stepwise evaluation)

具體而言，`stepwise` 後綴的資料集表示使用了 process signal：
- `cfa_extracted_exercise_sup_sample_from_policy_v1.1_dpo` -- 僅 outcome signal
- `cfa_extracted_exercise_sup_sample_from_policy_v1.1_stepwise_dpo` -- 加入 process signal

### 4.3 Generative Reward Model

從 `data.py` 的資料集名稱可以看到使用了 generative reward model：
`cfa_extracted_exercise_sup_sample_from_policy_v1.1_genrm_qwen3-32b_dpo`

這表示使用 Qwen3-32B 作為 generative reward model 來評估偏好對的品質，
而非傳統的 discriminative reward model。

---

## 五、關鍵研究發現

### 5.1 Joint CPT+SFT 防止 Catastrophic Forgetting

這是 FinDAP 最重要的實驗發現之一。
傳統的 sequential pipeline (先 CPT 再 SFT) 會導致模型在 CPT 階段
忘記 pre-training 時學到的指令遵循能力。
Joint training 透過交錯訓練兩種資料，有效緩解此問題。

在程式碼中，這體現為 `prepare_posttrain()` 中的邏輯：
當 `idrandom` 同時包含 `'sft'` 和 `'dapt'` 時，
會使用 `concatenate_datasets` 將 SFT 與 CPT 資料合併，
再以 `shuffle(seed=42)` 打亂順序。

### 5.2 不同階段貢獻不同能力

| 訓練階段 | 主要貢獻的能力維度 |
|----------|-------------------|
| CPT | Financial Concepts (金融概念理解) |
| SFT | Financial Tasks (金融任務執行) |
| RL (RPO) | Financial Reasoning (推理品質) |

### 5.3 Curriculum Learning 穩定訓練

Stage 2 使用更高的 warmup ratio (0.5 vs 0.1)，
從 Stage 1 的 checkpoint 繼續訓練，形成從簡單到複雜的課程學習。
較高的 warmup 防止在新資料分布上突然的梯度跳變。

### 5.4 Dual-signal 顯著提升推理

同時使用 outcome signal 與 process signal 的偏好學習，
相較於僅使用 outcome signal，在推理品質上有顯著提升。
這意味著不僅關注「答案對不對」，還關注「推理過程好不好」。

---

## 六、FinDAP 的局限與我們的改進空間

這一節分析 FinDAP 框架在哪些方面存在研究空白，
以及我們可以如何在這些方向上進行拓展與改進。
這是本文件最重要的部分，因為它直接對應到可以發表的研究貢獻。

### 6.1 缺乏問題解決策略 -- 可引入推理框架

**FinDAP 的局限:**
FinDAP 聚焦於 domain adaptation methodology（如何讓通用模型適應金融領域），
但並未探討 problem-solving strategies（模型應如何解決金融問題）。
模型收到題目後直接生成答案，沒有結構化的推理流程。

**我們可以做的:**

1. **Chain-of-Thought (CoT) 策略設計**: 針對 CFA 考試的不同題型
   （概念辨析、數值計算、情境判斷）設計專用的 CoT prompting 模板。
   例如，數值計算題可以要求模型先列出公式、代入數值、逐步計算。

2. **ReAct (Reasoning + Acting)**: 讓模型交替進行推理和動作，
   例如在解題過程中判斷是否需要查閱特定公式或表格。

3. **Multi-Agent 系統**: 設計多個專業化的 agent（概念解釋 agent、
   計算 agent、驗證 agent），讓它們協作解決複雜的金融問題。
   這對 CFA Level II 的 vignette-based 題目尤其有價值，
   因為這類題目需要同時處理文本理解、數據提取和計算推理。

4. **Self-consistency**: 讓模型生成多條推理路徑，取多數投票的答案，
   這在數值計算題上可能顯著提升準確率。

### 6.2 無錯誤分析與可解釋性 -- 可建立錯誤分類體系

**FinDAP 的局限:**
論文僅報告 accuracy 數字，沒有分析模型在什麼類型的題目上犯錯，
也沒有提供模型決策的可解釋性分析。

**我們可以做的:**

1. **建立金融 LLM 錯誤分類體系 (Error Taxonomy)**:
   - 概念錯誤 (Conceptual Error): 對金融術語或原理的理解有誤
   - 計算錯誤 (Computational Error): 公式正確但數值計算有誤
   - 推理錯誤 (Reasoning Error): 推理鏈中某個步驟的邏輯跳躍不合理
   - 資訊遺漏 (Information Omission): 未能從題幹中提取關鍵資訊
   - 格式錯誤 (Format Error): 推理正確但輸出格式不符要求

2. **逐題分析**: 針對 CFA-Challenge 的 90 道題進行逐題錯誤歸因，
   這在論文中具有很高的研究價值。

3. **Attention 分析**: 分析模型在解題時的注意力分布，
   了解模型是否關注了正確的資訊。

### 6.3 無校準研究 -- 可量測信心與準確度的關係

**FinDAP 的局限:**
論文完全沒有討論 calibration。模型可能以高信心給出錯誤答案，
或以低信心給出正確答案，但我們無從得知。

**我們可以做的:**

1. **Confidence Calibration 分析**: 量測模型對每個答案的信心程度
   （例如透過 token probability），然後繪製 calibration curve，
   分析信心與準確度的對應關係。

2. **Expected Calibration Error (ECE)**: 計算 ECE 指標，
   量化模型的校準程度。

3. **選擇性預測 (Selective Prediction)**: 研究是否可以讓模型
   在不確定時拒絕回答，從而在願意回答的題目上達到更高準確率。
   這對金融應用場景尤其重要 -- 錯誤的金融建議比「不知道」更危險。

4. **不同難度下的校準**: 分析模型在簡單題 (CFA-Easy) 和困難題
   (CFA-Challenge) 上的校準差異。

### 6.4 RPO 使用 Binary Outcome Signal -- 可設計更細粒度的 Process Reward Model

**FinDAP 的局限:**
雖然 FinDAP 提出了 dual-signal preference learning，
但其 outcome signal 仍然是 binary 的（答案正確/不正確），
process signal 的粒度也相對粗糙。

**我們可以做的:**

1. **Fine-grained Process Reward Model (PRM)**:
   為推理鏈的每一步驟設計獨立的獎勵信號：
   - 步驟的邏輯正確性 (0-1)
   - 步驟與前一步的連貫性 (0-1)
   - 步驟使用的金融知識是否正確 (0-1)
   - 步驟的計算是否正確 (0-1)

2. **Outcome Reward 的細粒度化**:
   對於數值計算題，不僅看最終答案是否正確，
   還可以評估答案與正確值的距離（partial credit）。

3. **Human-in-the-loop Reward**: 邀請 CFA 持證人為推理步驟打分，
   建立高品質的 process reward 訓練資料。

4. **Iterative Preference Learning**: FinDAP 的程式碼中已有
   iterative 的跡象（`rpo_iter_1` 等資料集名稱），
   但論文未深入探討多輪迭代的效果。我們可以系統性研究
   迭代次數對模型品質的影響。

### 6.5 僅評估準確率 -- 可加入多維度評估

**FinDAP 的局限:**
FinEval 雖然設計了多維度的評估框架，但最終的量化指標仍以 accuracy 為主。
對於金融 LLM 而言，這遠遠不夠。

**我們可以做的:**

1. **推理品質評估**:
   - 推理步驟數量是否合理
   - 每步推理是否必要（有無冗餘步驟）
   - 推理鏈的邏輯連貫性
   - 是否正確引用金融公式

2. **校準評估** (如 6.3 所述):
   - ECE, MCE (Maximum Calibration Error)
   - AUROC, AUPRC

3. **效率評估**:
   - 生成 token 數量 vs 答案品質的 trade-off
   - 推理延遲 (latency)
   - 不同模型大小下的性價比

4. **魯棒性評估**:
   - 同一題目的不同表述 (paraphrase) 下的穩定性
   - 對數值干擾項 (distractor) 的抵抗能力
   - 題目中加入無關資訊時的表現

5. **公平性評估**:
   - 不同 CFA Level 之間的表現差異
   - 不同知識領域 (Ethics, Quant, FRA, Equity 等) 之間的表現差異

### 6.6 無工具增強 -- CFA 考試需要計算器

**FinDAP 的局限:**
CFA 考試允許考生使用金融計算器 (BA II Plus / HP 12C)，
許多題目涉及 TVM (Time Value of Money)、IRR、統計計算等，
需要高精度數值運算。LLM 的浮點計算能力天生薄弱，
但 FinDAP 完全沒有探討工具增強的可能性。

**我們可以做的:**

1. **Financial Calculator Tool Use**:
   讓模型在推理過程中呼叫計算器 API，處理：
   - TVM 計算 (PV, FV, PMT, N, I/Y)
   - NPV / IRR 計算
   - 統計計算 (mean, std, correlation, regression)
   - Bond pricing (YTM, duration, convexity)

2. **Code Interpreter Integration**:
   讓模型生成 Python 程式碼來執行計算，
   這比純文字推理更精確且可驗證。

3. **Financial Data Lookup**:
   在需要查閱特定數據（如利率、匯率、歷史價格）的題目中，
   提供資料查詢工具。

4. **Tool Use vs Pure Reasoning 對比研究**:
   系統性比較有工具和無工具情境下的表現差異，
   量化工具增強的具體收益。

---

## 七、技術實作細節備註

以下記錄在閱讀程式碼時發現的重要技術細節，供後續研究參考。

### 7.1 資料平衡策略

在 joint CPT+SFT 訓練中，CPT 資料通常遠多於 SFT 資料。
FinDAP 提供兩種策略：

- **Downsample** (`--downsample`): 隨機抽取 CPT 資料，使其量等於 SFT 資料量
- **Upsample** (`--upsample`): 重複 SFT 資料，使其量等於 CPT 資料量

論文主要使用 downsample 策略。

### 7.2 Instruction Masking

`--instruction_mask` 確保在計算 loss 時，指令部分的 token 被 mask 掉 (label = -100)，
只對回應部分計算 loss。這是 SFT 的標準做法，但在 CPT+SFT 混合訓練中需要特別注意：
CPT 資料沒有指令/回應的邊界，其所有 token 都參與 loss 計算。

### 7.3 Attention Isolation

`--isolate_attention` 與 sequence packing 搭配使用。
當多個序列被打包進同一個 batch 時，需要確保它們之間的 attention 互不干擾。
這透過 monkey-patch Flash Attention 的 `_get_unpad_data` 函數實現。

### 7.4 DPO Trainer 的 Accelerator Hack

在 `approaches/posttrain.py` 的 `dpo_trainer()` 方法中，
有一個值得注意的 hack：手動 prepare model 和 optimizer 後，
將 `trainer.accelerator.prepare_model` monkey-patch 為 no-op。
這是為了解決 TRL 的 DPOTrainer 與 FSDP 的相容性問題
（參見 https://github.com/huggingface/trl/issues/1147）。

### 7.5 序列長度差異

Stage 1 和 2 使用 `max_seq_length=8000`，
Stage 3 使用 `max_seq_length=2048`。
這是因為 CPT 資料（如 book_fineweb）包含長文本需要較長序列，
而 DPO 偏好對通常較短，且更長的序列在 DPO 訓練中會導致記憶體不足。

### 7.6 HuggingFace Hub 資料集命名規律

- CPT/SFT 資料: `ZixuanKe/posttrain_tokenized_{name}_qwen2.5-32b-instruct`
- DPO 偏好資料: `ZixuanKe/{name}_binarized_F2048`

所有資料都已預先 tokenize，使用 Qwen2.5-32B-Instruct 的 tokenizer。
這表示 FinDAP 的最終目標模型可能是基於 Qwen 而非僅限於 Llama。

---

## 八、總結：FinDAP 的定位與我們的機會

FinDAP 是第一個系統性研究金融 LLM domain-adaptive post-training 的工作，
其貢獻在於方法論層面：它告訴我們「怎麼訓練一個好的金融 LLM」。

但 FinDAP 並未回答以下問題：
- 訓練好的模型如何最佳地解決金融問題？（推理策略）
- 模型犯了什麼錯？為什麼犯錯？（錯誤分析）
- 模型對自己的答案有多確定？（校準）
- 如何更精確地引導模型的推理過程？（細粒度 reward）
- 除了準確率，還有什麼值得衡量的？（多維度評估）
- 模型能否使用工具來彌補自身弱點？（工具增強）

這些問題恰恰是我們可以進行的研究方向，
且每一個方向都與 FinDAP 互補而非競爭。
我們可以站在 FinDAP 的肩膀上（使用其訓練出的 Llama-Fin-8b 模型），
專注於上述改進方向，產出具有獨立貢獻的研究成果。

---

最後更新：2026 年 1 月
