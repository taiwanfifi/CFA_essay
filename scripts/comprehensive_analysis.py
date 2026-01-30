#!/usr/bin/env python3
"""综合分析：年份、level、真实性、论文背书"""
from datasets import load_dataset
from pathlib import Path
import json

BASE = Path(__file__).parent

# 数据集配置：名称, repo, config, 论文背书, 真实性说明
DATASETS_INFO = [
    ("FinEval-CFA-Challenge", "Salesforce/FinEval", "CFA-Challenge", 
     "✅ EMNLP 2025 (FinDAP论文)", "模拟题/样本题，非官方真题"),
    ("FinEval-CFA-Easy", "Salesforce/FinEval", "CFA-Easy",
     "✅ EMNLP 2025 (FinDAP论文)", "模拟题/样本题，非官方真题"),
    ("flare-cfa", "TheFinAI/flare-cfa", None,
     "❓ 需查证", "第三方数据集，需验证"),
    ("CFA_Level_III", "alvinming/CFA-Level-III", None,
     "❌ 无论文", "2020 Mock PM模拟题"),
    ("CFA_Extracted系列", "ZixuanKe/cfa_extracted_qa_gpt4_verify_sup_chunk_0", None,
     "✅ EMNLP 2025 (FinDAP论文)", "SchweserNotes Level II 2020，非官方真题"),
    ("FinTrain-cfa_exercise", "Salesforce/FinTrain", "cfa_exercise_sup",
     "✅ EMNLP 2025 (FinDAP论文)", "SchweserNotes Level II，非官方真题"),
    ("CFA_Judgement", "xxuan-nlp/CFA_Judgement_Corpus_97-22", None,
     "❓ 需查证", "1997-2022判断题库，双语"),
]

def get_level_info(repo, config):
    """获取level信息"""
    try:
        ds = load_dataset(repo, config) if config else load_dataset(repo)
        # 检查title字段
        if 'train' in ds:
            sample = ds['train'][0]
            title = sample.get('title', '')
            if 'Level II' in str(title) or 'Level 2' in str(title):
                return "Level II"
            elif 'Level III' in str(title) or 'Level 3' in str(title):
                return "Level III"
            elif 'Level I' in str(title) or 'Level 1' in str(title):
                return "Level I"
        return "未明确"
    except:
        return "无法获取"

def get_year_info(repo, config):
    """获取年份信息"""
    try:
        ds = load_dataset(repo, config) if config else load_dataset(repo)
        if 'train' in ds:
            sample = ds['train'][0]
            title = str(sample.get('title', ''))
            # 提取年份
            import re
            years = re.findall(r'20\d{2}|19\d{2}', title)
            if years:
                return years[0]
        return "未明确"
    except:
        return "无法获取"

# 生成综合分析报告
report = "# CFA数据集深度分析报告\n\n"
report += "## 一、数据集真实性、年份、Level分析\n\n"
report += "| 数据集 | 样本数 | Level | 年份 | 来源 | 论文背书 | 真实性 |\n"
report += "|--------|--------|-------|------|------|----------|--------|\n"

for name, repo, config, paper, authenticity in DATASETS_INFO:
    try:
        ds = load_dataset(repo, config) if config else load_dataset(repo)
        count = sum(len(ds[split]) for split in ds.keys())
        level = get_level_info(repo, config)
        year = get_year_info(repo, config)
        
        report += f"| {name} | {count} | {level} | {year} | {repo} | {paper} | {authenticity} |\n"
    except Exception as e:
        report += f"| {name} | 错误 | - | - | {repo} | {paper} | {authenticity} |\n"

report += "\n## 二、关键发现\n\n"
report += "### 1. 论文背书情况\n\n"
report += "- **有论文背书**: FinEval系列、FinTrain系列、CFA_Extracted系列 (EMNLP 2025 FinDAP论文)\n"
report += "- **无论文背书**: CFA_Level_III (alvinming个人发布)\n"
report += "- **需查证**: flare-cfa、CFA_Judgement\n\n"

report += "### 2. 题目来源真实性\n\n"
report += "- **非官方真题**: 所有数据集都不是CFA Institute官方发布的真实考试题目\n"
report += "- **SchweserNotes**: CFA_Extracted和FinTrain-cfa_exercise来自SchweserNotes备考材料（Level II 2020）\n"
report += "- **模拟题**: FinEval-Challenge和CFA_Level_III包含2020 Mock PM模拟题\n"
report += "- **样本题**: FinEval-Easy和flare-cfa可能是样本题或练习题\n\n"

report += "### 3. Level分布\n\n"
report += "- **Level II**: CFA_Extracted系列、FinTrain-cfa_exercise (明确标注)\n"
report += "- **Level III**: CFA_Level_III (名称暗示，但需验证)\n"
report += "- **未明确**: FinEval系列、flare-cfa\n\n"

report += "### 4. 年份信息\n\n"
report += "- **2020**: 大部分数据集来自2020年材料\n"
report += "- **1997-2022**: CFA_Judgement覆盖25年跨度\n\n"

report += "\n## 三、LLM评估/训练建议\n\n"
report += "### 评估数据集选择\n\n"
report += "1. **FinEval系列** (推荐)\n"
report += "   - ✅ 有论文背书\n"
report += "   - ✅ 官方评估框架\n"
report += "   - ✅ 包含不同难度(Challenge/Easy)\n"
report += "   - ⚠️ 非官方真题，但格式规范\n\n"

report += "2. **flare-cfa** (备选)\n"
report += "   - ⚠️ 需查证来源和论文\n"
report += "   - ✅ 样本量较大(1032)\n\n"

report += "### 训练数据集选择\n\n"
report += "1. **FinTrain-cfa_exercise** (推荐)\n"
report += "   - ✅ 有论文背书\n"
report += "   - ✅ 样本量适中(2946)\n"
report += "   - ✅ 来自SchweserNotes Level II\n\n"

report += "2. **CFA_Extracted系列** (推荐)\n"
report += "   - ✅ 有论文背书\n"
report += "   - ✅ GPT-4验证\n"
report += "   - ✅ 包含材料上下文\n\n"

report += "3. **CFA_Judgement** (备选)\n"
report += "   - ⚠️ 需查证论文\n"
report += "   - ✅ 覆盖25年(1997-2022)\n"
report += "   - ✅ 样本量大(11099)\n\n"

report += "\n## 四、注意事项\n\n"
report += "1. **所有数据集都不是官方真题**，但可以用于评估LLM的金融知识能力\n"
report += "2. **SchweserNotes材料**是第三方备考材料，题目风格接近但非官方\n"
report += "3. **建议组合使用**：FinEval评估 + FinTrain训练，确保一致性\n"
report += "4. **Level信息不完整**，部分数据集未明确标注Level\n"
report += "5. **年份集中在2020**，可能无法反映最新考试趋势\n\n"

with open(BASE / "docs" / "深度分析报告.md", "w", encoding="utf-8") as f:
    f.write(report)

print("✓ 综合分析报告已生成: docs/深度分析报告.md")

