#!/usr/bin/env python3
"""深入分析CFA数据集：年份、level、真实性"""
from datasets import load_dataset
from pathlib import Path
import json
import re

BASE = Path(__file__).parent
results = {}

# 检查数据集
datasets_to_check = [
    ("TheFinAI/flare-cfa", None, "flare_cfa"),
    ("Salesforce/FinEval", "CFA-Challenge", "FinEval_Challenge"),
    ("Salesforce/FinEval", "CFA-Easy", "FinEval_Easy"),
    ("alvinming/CFA-Level-III", None, "CFA_Level_III"),
    ("ZixuanKe/cfa_extracted_qa_gpt4_verify_sup_chunk_0", None, "CFA_Extracted_chunk0"),
    ("Salesforce/FinTrain", "cfa_exercise_sup", "FinTrain_cfa"),
]

def extract_info(text):
    """从文本中提取年份和level信息"""
    info = {"years": [], "levels": [], "sources": []}
    
    # 提取年份 (1997-2025)
    years = re.findall(r'\b(19|20)\d{2}\b', str(text))
    info["years"] = list(set(years))
    
    # 提取Level信息
    levels = re.findall(r'Level\s*[I123]|Level\s*II|Level\s*III', str(text), re.IGNORECASE)
    info["levels"] = list(set([l.upper() for l in levels]))
    
    # 提取来源信息
    if "SchweserNotes" in str(text):
        info["sources"].append("SchweserNotes")
    if "sample_test" in str(text):
        info["sources"].append("sample_test")
    if "CFA Institute" in str(text):
        info["sources"].append("CFA_Institute")
    
    return info

for repo, config, name in datasets_to_check:
    print(f"\n{'='*60}")
    print(f"分析: {name}")
    print(f"{'='*60}")
    
    try:
        ds = load_dataset(repo, config) if config else load_dataset(repo)
        
        analysis = {
            "repo": repo,
            "config": config,
            "splits": list(ds.keys()),
            "samples_analyzed": {},
            "years_found": set(),
            "levels_found": set(),
            "sources_found": set(),
            "sample_queries": []
        }
        
        # 分析每个split的前10个样本
        for split in ds.keys():
            print(f"  分析 {split} split...")
            samples = []
            years = set()
            levels = set()
            sources = set()
            
            # 检查前10个样本
            for i in range(min(10, len(ds[split]))):
                sample = ds[split][i]
                sample_text = json.dumps(sample, ensure_ascii=False)
                
                info = extract_info(sample_text)
                years.update(info["years"])
                levels.update(info["levels"])
                sources.update(info["sources"])
                
                # 保存样本的关键信息
                sample_info = {}
                for key in ["query", "questions", "title", "source", "topic"]:
                    if key in sample:
                        val = str(sample[key])
                        sample_info[key] = val[:200] if len(val) > 200 else val
                
                samples.append(sample_info)
            
            analysis["samples_analyzed"][split] = {
                "count": len(ds[split]),
                "checked": min(10, len(ds[split])),
                "samples": samples
            }
            analysis["years_found"].update(years)
            analysis["levels_found"].update(levels)
            analysis["sources_found"].update(sources)
        
        analysis["years_found"] = sorted(list(analysis["years_found"]))
        analysis["levels_found"] = sorted(list(analysis["levels_found"]))
        analysis["sources_found"] = sorted(list(analysis["sources_found"]))
        
        results[name] = analysis
        
        print(f"  ✓ 年份: {analysis['years_found']}")
        print(f"  ✓ Level: {analysis['levels_found']}")
        print(f"  ✓ 来源: {analysis['sources_found']}")
        
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        results[name] = {"error": str(e)}

# 保存结果
with open(BASE / "docs" / "深度分析.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n" + "="*60)
print("深度分析完成！结果保存在 docs/深度分析.json")
print("="*60)

