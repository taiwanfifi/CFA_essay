#!/usr/bin/env python3
"""生成数据集对比分析文档"""
import json
from pathlib import Path

BASE = Path(__file__).parent
DATASETS_DIR = BASE / "datasets"

# 数据集映射
DS_MAP = {
    "flare_cfa": ("TheFinAI/flare-cfa", None, "评估数据集"),
    "FinEval/CFA_Challenge": ("Salesforce/FinEval", "CFA-Challenge", "评估数据集-挑战级"),
    "FinEval/CFA_Easy": ("Salesforce/FinEval", "CFA-Easy", "评估数据集-简单级"),
    "FinEval/CRA_Bigdata": ("Salesforce/FinEval", "CRA-Bigdata", "评估数据集-大数据"),
    "CFA_Judgement": ("xxuan-nlp/CFA_Judgement_Corpus_97-22", None, "训练数据-判断题库"),
    "CFA_Rule": ("ZixuanKe/cfa_rule_unsup", None, "训练数据-规则(无监督)"),
    "CFA_Knowledgeable": ("ZixuanKe/cfa_clean_knowledgeable_answer_unsup", None, "训练数据-知识问答(无监督)"),
    "CFA_Level_III": ("alvinming/CFA-Level-III", None, "训练数据-三级考试"),
    "CFA_Extracted/chunk_0": ("ZixuanKe/cfa_extracted_qa_gpt4_verify_sup_chunk_0", None, "训练数据-提取QA(有监督)"),
    "CFA_Extracted/sft": ("ZixuanKe/cfa_extracted_qa_gpt4_verify_sft_without_material_gpt4_answer", None, "训练数据-SFT"),
    "FinTrain/apex_instruct": ("Salesforce/FinTrain", "apex_instruct_for_annealing_sup", "训练数据-指令微调"),
    "FinTrain/book_fineweb": ("Salesforce/FinTrain", "book_fineweb_unsup", "训练数据-书籍网页(无监督)"),
    "FinTrain/cfa_exercise": ("Salesforce/FinTrain", "cfa_exercise_sup", "训练数据-CFA练习(有监督)"),
}

def load_analysis(dirname):
    path = DATASETS_DIR / dirname / "analysis.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# 生成文档
doc = "# CFA数据集完整对比分析\n\n"
doc += "## 数据集分类\n\n"

# 按用途分类
eval_ds = []
train_ds = []
for name, (repo, config, usage) in DS_MAP.items():
    info = load_analysis(name)
    if info:
        analysis = info.get("analysis", {})
        total = sum(analysis.get("sample_counts", {}).values())
        features = list(analysis.get("features", {}).values())[0] if analysis.get("features") else []
        item = (name, repo, config, total, usage, features)
        if "评估" in usage:
            eval_ds.append(item)
        else:
            train_ds.append(item)

doc += "### 评估数据集 (Evaluation Datasets)\n\n"
doc += "| 数据集 | Repository | Config | 样本数 | 字段 |\n"
doc += "|--------|-----------|--------|--------|------|\n"
for name, repo, config, total, usage, features in eval_ds:
    doc += f"| {name} | {repo} | {config or '-'} | {total} | {', '.join(features[:3])}... |\n"

doc += "\n### 训练数据集 (Training Datasets)\n\n"
doc += "| 数据集 | Repository | Config | 样本数 | 用途 | 字段 |\n"
doc += "|--------|-----------|--------|--------|------|------|\n"
for name, repo, config, total, usage, features in train_ds:
    doc += f"| {name} | {repo} | {config or '-'} | {total} | {usage} | {', '.join(features[:3])}... |\n"

doc += "\n## 详细分析\n\n"
for name, (repo, config, usage) in DS_MAP.items():
    info = load_analysis(name)
    if not info:
        continue
    doc += f"### {name}\n\n"
    doc += f"- **用途**: {usage}\n"
    doc += f"- **Repository**: `{repo}`\n"
    if config:
        doc += f"- **Config**: `{config}`\n"
    analysis = info.get("analysis", {})
    for split in analysis.get("splits", []):
        count = analysis.get("sample_counts", {}).get(split, 0)
        features = analysis.get("features", {}).get(split, [])
        doc += f"- **{split}**: {count} 样本\n"
        doc += f"  - 字段: {', '.join(features)}\n"
    sample = analysis.get("sample_data", {})
    if sample:
        first_split = list(sample.keys())[0]
        doc += f"- **示例** ({first_split}):\n"
        doc += f"```json\n{json.dumps(sample[first_split], indent=2, ensure_ascii=False)}\n```\n"
    doc += "\n"

doc += "\n## 数据集关系与差异\n\n"
doc += "### 评估数据集\n"
doc += "- **FinEval系列**: Salesforce官方评估套件，包含不同难度级别\n"
doc += "- **flare-cfa**: 第三方CFA评估数据集\n\n"
doc += "### 训练数据集\n"
doc += "- **FinTrain系列**: Salesforce官方训练数据，包含指令、无监督、有监督数据\n"
doc += "- **CFA_Extracted系列**: 从材料中提取的QA对，GPT-4验证\n"
doc += "- **CFA_Judgement**: 1997-2022年判断题库\n"
doc += "- **CFA_Level_III**: 三级考试题目\n"
doc += "- **CFA_Rule/Knowledgeable**: 规则和知识问答数据\n\n"

with open(BASE / "docs" / "数据集对比.md", "w", encoding="utf-8") as f:
    f.write(doc)

print("✓ 对比文档已生成: docs/数据集对比.md")
