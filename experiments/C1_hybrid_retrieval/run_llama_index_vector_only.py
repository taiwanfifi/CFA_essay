# run_llama_index_vector_only.py
# 公平比較版：只跑純 Vector 檢索，不啟用 rewrite/sub-query/hybrid
import os
import json
from tqdm import tqdm
from typing import List, Dict, Any

from dotenv import load_dotenv
from llama_index.core import (
    Document,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

print("--- 🚀 LlamaIndex 純 Vector 檢索 評估器 ---")

# =========================
# 基本設定
# =========================
DATA_FILE_PATH = "./data/ultimate_rag_challenge_questions.json"
OUTPUT_FILE_PATH = "./llama_index_vector_only_results.json"
KB_PERSIST_DIR = "./llama_index_vector_only_storage"

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("🛑 請先設定 OPENAI_API_KEY 環境變數")

# 用 OpenAI GPT-4o-mini 當 dummy LLM（不會真的用到）
Settings.llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# 嵌入 = text-embedding-3-large (3072 維)
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-large", api_key=OPENAI_API_KEY
)

print("✅ LlamaIndex 設定完成：Vector-only mode")
print("   - Embedding: text-embedding-3-large")
print("   - LLM: gpt-4o-mini (not used in query pipeline)\n")

# =========================
# 建立知識庫
# =========================
if not os.path.exists(KB_PERSIST_DIR):
    print("--- 建立新索引 ---")
    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        eval_data = json.load(f)

    unique_evidence: Dict[str, str] = {
        ev["doc_id"]: ev["text_snippet"]
        for item in eval_data
        for ev in item.get("gold_evidence", [])
        if ev.get("doc_id") and isinstance(ev.get("text_snippet"), str)
    }

    docs = [Document(text=txt, metadata={"doc_id": did}) for did, txt in unique_evidence.items()]
    print(f"   - 共 {len(docs)} 份文件加入索引")

    index = VectorStoreIndex.from_documents(docs, show_progress=True)
    index.storage_context.persist(persist_dir=KB_PERSIST_DIR)
else:
    print("--- 載入既有索引 ---")
    storage_context = StorageContext.from_defaults(persist_dir=KB_PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# 建立 Retriever（純 vector search, top_k=5）
retriever = index.as_retriever(similarity_top_k=5)

# =========================
# 執行檢索
# =========================
print("\n--- 開始處理評估問題 ---")
with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
    eval_data = json.load(f)

results_map: Dict[str, List[Dict[str, Any]]] = {}

for qa in tqdm(eval_data, desc="評估進度"):
    qid = qa.get("question_id")
    q = qa.get("question")
    if not qid or not q:
        continue

    try:
        retrieved_nodes = retriever.retrieve(q)
        bundle: List[Dict[str, Any]] = []
        for node in retrieved_nodes:
            did = node.metadata.get("doc_id")
            if did:
                bundle.append({
                    "page_content": node.get_content(),
                    "metadata": {"doc_id": did},
                })
        results_map[qid] = bundle
    except Exception as e:
        print(f"⚠️ 問題 {qid} 發生錯誤：{e}")
        results_map[qid] = []

# =========================
# 輸出結果
# =========================
with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(results_map, f, ensure_ascii=False, indent=4)

print(f"\n🎉 完成！檢索結果已輸出至 {OUTPUT_FILE_PATH}")
print("👉 現在你可以執行 `python evaluate.py` 加入這個系統做公平比較。")
