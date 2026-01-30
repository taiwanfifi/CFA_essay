# CFA 資料集快速索引

## 資料集總覽

| 資料集 | 路徑 | 樣本數 | Level | 用途 | 狀態 |
|--------|------|--------|-------|------|------|
| FinEval-CFA-Challenge | `FinEval/CFA_Challenge/` | 90 | ~L2/L3 | 評估（高難度） | 使用中 |
| FinEval-CFA-Easy | `FinEval/CFA_Easy/` | 1,032 | 未標註 | 評估（標準） | 使用中 |
| FinEval-CRA-Bigdata | `FinEval/CRA_Bigdata/` | 1,472 | 未標註 | 評估（大數據） | 使用中 |
| FinTrain-apex_instruct | `FinTrain/apex_instruct/` | 1,472,062 | 未標註 | 訓練（通用指令） | 使用中 |
| FinTrain-book_fineweb | `FinTrain/book_fineweb/` | 4,500 | 未標註 | 訓練（CPT 文本） | 使用中 |
| FinTrain-cfa_exercise | `FinTrain/cfa_exercise/` | 2,946 | Level II | 訓練（CFA 習題） | 使用中 |
| CFA_Extracted-chunk_0 | `CFA_Extracted/` | 1,124 | Level II | 訓練/RAG（含教材） | 使用中 |
| CFA_Extracted-sft | `CFA_Extracted/` | 2,946 | Level II | 訓練（SFT 格式） | 使用中 |
| CFA_Level_III | `CFA_Level_III/` | 90 | Level III | 跨級別比較（僅 MCQ） | 使用中 |
| FinDAP 訓練框架 | `FinDap/FinDAP/` | — | — | 訓練程式碼 | 參考用 |
| flare-cfa | `archived/flare_cfa/` | 1,032 | 未標註 | — | **已歸檔（與 CFA-Easy 重複）** |

## 推薦使用方案

### 評估
- **主要**：FinEval-CFA-Challenge (90 題) + FinEval-CFA-Easy (1,032 題)
- **輔助**：FinEval-CRA-Bigdata (1,472 題)
- **跨級別**：CFA_Level_III (90 題，僅 MCQ)

### 訓練
- **SFT**：FinTrain-cfa_exercise (2,946 題) + CFA_Extracted-sft (2,946 題)
- **CPT**：FinTrain-book_fineweb (4,500 篇)
- **RAG**：CFA_Extracted-chunk_0 (1,124 題，含 material 欄位)

### 不使用
- **flare-cfa**：與 FinEval-CFA-Easy 幾乎完全相同（已歸檔至 `archived/`）
- **CFA_Judgement**：實為香港法律案例，非 CFA 資料（已刪除）

## 資料來源

所有資料集均來自 HuggingFace Hub：
- FinEval / FinTrain：`Salesforce/` 命名空間（EMNLP 2025 FinDAP 論文背書）
- CFA_Extracted：`ZixuanKe/` 命名空間（FinDAP 第一作者）
- CFA_Level_III：`alvinming/` 命名空間（個人發布，無論文背書）

詳細資料集分析請參閱 `docs/01-數據集完整手冊.md`。
