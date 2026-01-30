#!/usr/bin/env python3
"""
真正下載所有數據集的完整數據到本地
"""
from datasets import load_dataset
from pathlib import Path
import json
import pickle

BASE = Path(__file__).parent
DATASETS_DIR = BASE / "datasets"

# 所有需要下載的數據集
DATASETS_CONFIG = [
    # FinEval系列
    {
        "repo": "Salesforce/FinEval",
        "config": "CFA-Challenge",
        "dirname": "FinEval/CFA_Challenge",
        "split": "test"
    },
    {
        "repo": "Salesforce/FinEval",
        "config": "CFA-Easy",
        "dirname": "FinEval/CFA_Easy",
        "split": "test"
    },
    {
        "repo": "Salesforce/FinEval",
        "config": "CRA-Bigdata",
        "dirname": "FinEval/CRA_Bigdata",
        "split": "test"
    },
    # FinTrain系列
    {
        "repo": "Salesforce/FinTrain",
        "config": "cfa_exercise_sup",
        "dirname": "FinTrain/cfa_exercise",
        "split": "train"
    },
    {
        "repo": "Salesforce/FinTrain",
        "config": "apex_instruct_for_annealing_sup",
        "dirname": "FinTrain/apex_instruct",
        "split": "train"
    },
    {
        "repo": "Salesforce/FinTrain",
        "config": "book_fineweb_unsup",
        "dirname": "FinTrain/book_fineweb",
        "split": "train"
    },
    # CFA_Extracted系列
    {
        "repo": "ZixuanKe/cfa_extracted_qa_gpt4_verify_sup_chunk_0",
        "config": None,
        "dirname": "CFA_Extracted/chunk_0",
        "split": "train"
    },
    {
        "repo": "ZixuanKe/cfa_extracted_qa_gpt4_verify_sft_without_material_gpt4_answer",
        "config": None,
        "dirname": "CFA_Extracted/sft",
        "split": "train"
    },
    # 其他
    {
        "repo": "TheFinAI/flare-cfa",
        "config": None,
        "dirname": "flare_cfa",
        "split": "test"
    },
    {
        "repo": "alvinming/CFA-Level-III",
        "config": None,
        "dirname": "CFA_Level_III",
        "split": "train"
    },
    {
        "repo": "ZixuanKe/cfa_clean_knowledgeable_answer_unsup",
        "config": None,
        "dirname": "CFA_Knowledgeable",
        "split": "train"
    },
    {
        "repo": "ZixuanKe/cfa_rule_unsup",
        "config": None,
        "dirname": "CFA_Rule",
        "split": "train"
    },
]

def download_full_dataset(ds_config):
    """下載完整數據集到本地"""
    repo = ds_config["repo"]
    config = ds_config["config"]
    dirname = ds_config["dirname"]
    split = ds_config["split"]
    
    print(f"\n{'='*60}")
    print(f"下載: {repo} ({config or 'default'})")
    print(f"保存到: {dirname}")
    print(f"{'='*60}")
    
    try:
        # 加載數據集
        if config:
            ds = load_dataset(repo, config, split=split)
        else:
            ds = load_dataset(repo, split=split)
        
        print(f"✓ 加載成功，樣本數: {len(ds):,}")
        
        # 創建目錄
        target_dir = DATASETS_DIR / dirname
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存完整數據為JSON格式
        print(f"正在保存數據...")
        all_data = []
        batch_size = 1000
        
        for i in range(0, len(ds), batch_size):
            end_idx = min(i + batch_size, len(ds))
            batch = [ds[j] for j in range(i, end_idx)]
            all_data.extend(batch)
            if (i // batch_size + 1) % 10 == 0:
                print(f"  已處理: {end_idx:,} / {len(ds):,}")
        
        # 保存為JSON
        data_file = target_dir / "data.json"
        print(f"正在寫入文件: {data_file}")
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        file_size_mb = data_file.stat().st_size / (1024 * 1024)
        print(f"✓ 保存完成")
        print(f"  文件: {data_file}")
        print(f"  大小: {file_size_mb:.2f} MB")
        print(f"  樣本數: {len(all_data):,}")
        
        # 保存統計信息
        stats = {
            "repo": repo,
            "config": config,
            "split": split,
            "num_samples": len(all_data),
            "file_size_mb": round(file_size_mb, 2),
            "data_file": str(data_file.relative_to(BASE))
        }
        
        with open(target_dir / "download_stats.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"✗ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*60)
    print("下載所有數據集的完整數據")
    print("="*60)
    
    success_count = 0
    fail_count = 0
    
    for ds_config in DATASETS_CONFIG:
        if download_full_dataset(ds_config):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n{'='*60}")
    print(f"下載完成")
    print(f"成功: {success_count}")
    print(f"失敗: {fail_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

