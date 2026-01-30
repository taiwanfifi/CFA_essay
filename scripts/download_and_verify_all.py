#!/usr/bin/env python3
"""
下載所有CFA相關數據集並驗證數據質量
"""
from pathlib import Path
from datasets import load_dataset
import json
import sys

BASE = Path(__file__).parent
DATASETS_DIR = BASE / "datasets"

# 需要下載的數據集配置
DATASETS_TO_DOWNLOAD = [
    # FinEval系列（評估數據）
    {
        "repo": "Salesforce/FinEval",
        "config": "CFA-Challenge",
        "dirname": "FinEval/CFA_Challenge",
        "split": "test",
        "type": "eval"
    },
    {
        "repo": "Salesforce/FinEval",
        "config": "CFA-Easy",
        "dirname": "FinEval/CFA_Easy",
        "split": "test",
        "type": "eval"
    },
    {
        "repo": "Salesforce/FinEval",
        "config": "CRA-Bigdata",
        "dirname": "FinEval/CRA_Bigdata",
        "split": "test",
        "type": "eval"
    },
    # FinTrain系列（訓練數據）
    {
        "repo": "Salesforce/FinTrain",
        "config": "cfa_exercise_sup",
        "dirname": "FinTrain/cfa_exercise",
        "split": "train",
        "type": "train"
    },
    {
        "repo": "Salesforce/FinTrain",
        "config": "apex_instruct_for_annealing_sup",
        "dirname": "FinTrain/apex_instruct",
        "split": "train",
        "type": "train"
    },
    {
        "repo": "Salesforce/FinTrain",
        "config": "book_fineweb_unsup",
        "dirname": "FinTrain/book_fineweb",
        "split": "train",
        "type": "train"
    },
    # CFA_Extracted系列
    {
        "repo": "ZixuanKe/cfa_extracted_qa_gpt4_verify_sup_chunk_0",
        "config": None,
        "dirname": "CFA_Extracted/chunk_0",
        "split": "train",
        "type": "train"
    },
    {
        "repo": "ZixuanKe/cfa_extracted_qa_gpt4_verify_sft_without_material_gpt4_answer",
        "config": None,
        "dirname": "CFA_Extracted/sft",
        "split": "train",
        "type": "train"
    },
    # 其他
    {
        "repo": "TheFinAI/flare-cfa",
        "config": None,
        "dirname": "flare_cfa",
        "split": "test",
        "type": "eval"
    },
    {
        "repo": "alvinming/CFA-Level-III",
        "config": None,
        "dirname": "CFA_Level_III",
        "split": "train",
        "type": "eval"
    },
]

def download_and_verify_dataset(ds_config):
    """下載並驗證單個數據集"""
    repo = ds_config["repo"]
    config = ds_config["config"]
    dirname = ds_config["dirname"]
    split = ds_config["split"]
    ds_type = ds_config["type"]
    
    print(f"\n{'='*60}")
    print(f"處理: {repo} ({config or 'default'})")
    print(f"類型: {ds_type.upper()}")
    print(f"{'='*60}")
    
    try:
        # 下載數據集
        if config:
            ds = load_dataset(repo, config, split=split)
        else:
            ds = load_dataset(repo, split=split)
        
        # 創建目錄
        target_dir = DATASETS_DIR / dirname
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存基本信息
        info = {
            "repo": repo,
            "config": config,
            "split": split,
            "type": ds_type,
            "num_samples": len(ds),
            "features": list(ds.features.keys()) if hasattr(ds, 'features') else []
        }
        
        with open(target_dir / "info.json", "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        
        # 驗證數據質量
        print(f"\n✓ 下載成功")
        print(f"  樣本數: {len(ds)}")
        print(f"  字段: {list(ds.features.keys()) if hasattr(ds, 'features') else 'N/A'}")
        
        # 抽樣檢查數據
        print(f"\n  抽樣檢查（前3個樣本）:")
        for i in range(min(3, len(ds))):
            sample = ds[i]
            print(f"\n  樣本 {i+1}:")
            # 只顯示關鍵字段的前100字符
            for key, value in list(sample.items())[:5]:
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:100] + "..."
                print(f"    {key}: {value_str}")
        
        # 檢查數據真實性
        print(f"\n  數據真實性檢查:")
        issues = []
        
        # 檢查是否有空值
        for i in range(min(10, len(ds))):
            sample = ds[i]
            for key, value in sample.items():
                if value is None or (isinstance(value, str) and len(value.strip()) == 0):
                    issues.append(f"樣本{i}的{key}為空")
        
        if issues:
            print(f"    ⚠️ 發現問題: {issues[:5]}")
        else:
            print(f"    ✓ 前10個樣本無空值問題")
        
        # 檢查CFA相關性
        if ds_type == "eval":
            # 檢查是否包含CFA相關關鍵詞
            cfa_keywords = ["CFA", "cfa", "financial", "investment", "portfolio", "bond", "equity"]
            sample_text = json.dumps(ds[0], ensure_ascii=False).lower()
            has_cfa = any(kw in sample_text for kw in cfa_keywords)
            if has_cfa:
                print(f"    ✓ 包含CFA/金融相關內容")
            else:
                print(f"    ⚠️ 未明顯包含CFA/金融相關內容")
        
        # 保存分析結果
        analysis = {
            "download_status": "success",
            "num_samples": len(ds),
            "features": list(ds.features.keys()) if hasattr(ds, 'features') else [],
            "sample_data": {str(i): ds[i] for i in range(min(3, len(ds)))},
            "verification": {
                "has_empty_values": len(issues) > 0,
                "issues": issues[:10]
            }
        }
        
        with open(target_dir / "analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ 驗證完成，數據已保存到: {target_dir}")
        return True
        
    except Exception as e:
        print(f"\n✗ 錯誤: {e}")
        error_info = {
            "repo": repo,
            "config": config,
            "error": str(e),
            "download_status": "failed"
        }
        target_dir = DATASETS_DIR / dirname
        target_dir.mkdir(parents=True, exist_ok=True)
        with open(target_dir / "error.json", "w", encoding="utf-8") as f:
            json.dump(error_info, f, indent=2, ensure_ascii=False)
        return False

def main():
    print("="*60)
    print("下載並驗證所有CFA相關數據集")
    print("="*60)
    
    success_count = 0
    fail_count = 0
    
    for ds_config in DATASETS_TO_DOWNLOAD:
        if download_and_verify_dataset(ds_config):
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

