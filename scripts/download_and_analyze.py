#!/usr/bin/env python3
from datasets import load_dataset
from huggingface_hub import model_info, list_repo_files
from pathlib import Path
import json

BASE = Path(__file__).parent
DATASETS = [
    ("TheFinAI/flare-cfa", None, "flare_cfa"),
    ("Salesforce/FinEval", "CFA-Challenge", "FinEval/CFA_Challenge"),
    ("Salesforce/FinEval", "CFA-Easy", "FinEval/CFA_Easy"),
    ("Salesforce/FinEval", "CRA-Bigdata", "FinEval/CRA_Bigdata"),
    ("xxuan-nlp/CFA_Judgement_Corpus_97-22", None, "CFA_Judgement"),
    ("ZixuanKe/cfa_rule_unsup", None, "CFA_Rule"),
    ("ZixuanKe/cfa_clean_knowledgeable_answer_unsup", None, "CFA_Knowledgeable"),
    ("alvinming/CFA-Level-III", None, "CFA_Level_III"),
    ("ZixuanKe/cfa_extracted_qa_gpt4_verify_sup_chunk_0", None, "CFA_Extracted/chunk_0"),
    ("ZixuanKe/cfa_extracted_qa_gpt4_verify_sft_without_material_gpt4_answer", None, "CFA_Extracted/sft"),
    ("Salesforce/FinTrain", "apex_instruct_for_annealing_sup", "FinTrain/apex_instruct"),
    ("Salesforce/FinTrain", "book_fineweb_unsup", "FinTrain/book_fineweb"),
    ("Salesforce/FinTrain", "cfa_exercise_sup", "FinTrain/cfa_exercise"),
]
MODELS = [
    ("Salesforce/Llama-Fin-8b", "Llama_Fin_8b"),
    ("tarun7r/Finance-Llama-8B", "Finance_Llama_8B"),
]

def analyze_ds(ds):
    result = {}
    for split in ds.keys():
        result[split] = {
            "count": len(ds[split]),
            "features": list(ds[split].features.keys()),
            "sample": {k: str(v)[:200] if isinstance(v, str) and len(str(v)) > 200 else v 
                      for k, v in ds[split][0].items()} if len(ds[split]) > 0 else {}
        }
    return result

# 下载datasets
for repo, config, dirname in DATASETS:
    print(f"\n处理: {repo} {config or ''}")
    try:
        path = BASE / "datasets" / dirname
        path.mkdir(parents=True, exist_ok=True)
        ds = load_dataset(repo, config) if config else load_dataset(repo)
        analysis = analyze_ds(ds)
        with open(path / "info.json", "w", encoding="utf-8") as f:
            json.dump({"repo": repo, "config": config, "analysis": analysis}, f, indent=2, ensure_ascii=False)
        print(f"✓ {dirname}")
    except Exception as e:
        print(f"✗ 错误: {e}")

# 获取模型信息
for repo, dirname in MODELS:
    print(f"\n处理模型: {repo}")
    try:
        path = BASE / "models" / dirname
        path.mkdir(parents=True, exist_ok=True)
        info = model_info(repo)
        files = list_repo_files(repo)[:10]
        with open(path / "info.json", "w", encoding="utf-8") as f:
            json.dump({
                "repo": repo,
                "sha": getattr(info, "sha", ""),
                "tags": getattr(info, "tags", []),
                "files": files
            }, f, indent=2, ensure_ascii=False)
        print(f"✓ {dirname}")
    except Exception as e:
        print(f"✗ 错误: {e}")

print("\n完成！")
