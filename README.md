# CFA + LLM 研究專案

本專案以 **FinDAP** (Demystifying Domain-adaptive Post-training for Financial LLMs, EMNLP 2025 Oral) 為技術基礎，研究如何提升大型語言模型在 CFA 特許金融分析師考試上的推理能力。

---

## 專案結構

```
CFA/
├── docs/                      # 核心研究文件（5 個）
│   ├── 01-數據集完整手冊.md   # 12 個資料集的權威參考
│   ├── 02-文獻綜述與研究定位.md # 5 篇核心論文 + 6 個研究空白
│   ├── 03-研究方向深度設計.md  # 7 個研究方向 + 論文拆分策略 ★
│   ├── 04-FinDAP框架解析.md   # 程式碼架構 + 局限與改進空間
│   └── 05-審稿人挑戰與應對策略.md # 6 大挑戰 + 量化防禦
│
├── datasets/                  # 資料集（詳見 datasets/README.md）
│   ├── FinEval/               # 評估資料集（Challenge / Easy / CRA）
│   ├── FinTrain/              # 訓練資料集（apex / book / cfa_exercise）
│   ├── CFA_Extracted/         # CFA QA 對（含教材原文）
│   ├── CFA_Level_III/         # Level III MCQ
│   ├── FinDap/                # FinDAP 訓練框架程式碼
│   └── archived/              # 已歸檔：flare_cfa（與 CFA-Easy 重複）
│
├── scripts/                   # 資料集下載與分析腳本
├── reference/                 # 技術參考資料（JSON / 對比表）
├── archive/                   # 原始文件備份（不再使用）
│   ├── original-docs/         # docs/ 下 14 個舊 .md + 2 .json
│   └── original-dataset-docs/ # datasets/ 下 6 個舊 .md + 1 .json
└── models/                    # 模型資訊
```

## 建議閱讀順序

1. **快速了解數據**：`docs/01-數據集完整手冊.md`
2. **了解研究現狀**：`docs/02-文獻綜述與研究定位.md`
3. **核心——研究方向**：`docs/03-研究方向深度設計.md` ★
4. **技術參考**：`docs/04-FinDAP框架解析.md`
5. **論文防禦**：`docs/05-審稿人挑戰與應對策略.md`

## 關鍵發現

- 所有 CFA 資料集均非官方真題（SchweserNotes 來源，有 EMNLP 2025 論文背書）
- 最佳模型 (o4-mini) 在 CFA Level III 上準確率 79.1%，仍有 20%+ 錯誤率
- GPT-4o 在金融數學推理上僅 60.9%（vs 人類 92%），差距 31%
- 本專案已完成 7 個具體研究方向的設計，可拆分為 4-5 篇論文

## 環境設定

```bash
conda create -n FinDAP python=3.10 && conda activate FinDAP
cd datasets/FinDap/FinDAP
pip install -r requirements.txt
```

## 常用指令

```bash
# 資料集下載與分析
python scripts/download_and_analyze.py
python scripts/analyze_comparison.py

# 模型評估
lm_eval --apply_chat_template --model vllm \
  --model_args pretrained=Salesforce/Llama-Fin-8b,max_length=8000,dtype=bfloat16 \
  --tasks cfa-challenge --device cuda
```
