import os
import json
from tqdm import tqdm
from typing import List, Dict, Any

from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    Document,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

print("--- 🚀 LlamaIndex 評估執行器 (OpenAI 版) ---")

# ========================
# 0. 環境檢查
# ========================
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("🛑 請先設定環境變數 OPENAI_API_KEY")

# ========================
# 1. 設定 LLM & Embedding
# ========================
Settings.llm = OpenAI(model="gpt-4o-mini", request_timeout=120.0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")

print("✅ 已設定 LlamaIndex 使用 OpenAI")
print(f"   - LLM: gpt-4o-mini")
print(f"   - Embedding: text-embedding-3-large\n")

# ========================
# 2. 資料與輸出路徑
# ========================
DATA_FILE_PATH = "./data/ultimate_rag_challenge_questions.json"
OUTPUT_FILE_PATH = "./llama_index_retrieval_results.json"
KB_PERSIST_DIR = "./llama_index_kb_storage"

# ========================
# 3. 準備知識庫
# ========================
if not os.path.exists(KB_PERSIST_DIR):
    print("📂 未找到索引，建立新索引中...")
    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        eval_data = json.load(f)

    unique_evidence: Dict[str, str] = {}
    for item in eval_data:
        for ev in item.get("gold_evidence", []):
            did = ev.get("doc_id")
            txt = ev.get("text_snippet")
            if did and isinstance(txt, str):
                unique_evidence[did] = txt

    docs = [Document(text=txt, metadata={"doc_id": did}) for did, txt in unique_evidence.items()]
    print(f"   - 找到 {len(docs)} 份文件，正在建立索引...")

    index = VectorStoreIndex.from_documents(docs, show_progress=True)
    os.makedirs(KB_PERSIST_DIR, exist_ok=True)
    index.storage_context.persist(persist_dir=KB_PERSIST_DIR)
else:
    print("✅ 從既有索引載入")
    storage_context = StorageContext.from_defaults(persist_dir=KB_PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine(similarity_top_k=5)

# ========================
# 4. 逐題檢索
# ========================
print("\n--- 開始處理評估問題 ---")
with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
    eval_data_for_questions = json.load(f)

results_map: Dict[str, List[Dict[str, Any]]] = {}

for qa_pair in tqdm(eval_data_for_questions, desc="評估進度"):
    q_id = qa_pair.get("question_id")
    question = qa_pair.get("question")
    if not q_id or not question:
        continue

    try:
        response = query_engine.query(question)
        retrieved_nodes = response.source_nodes or []

        bundle: List[Dict[str, Any]] = []
        for sn in retrieved_nodes:
            node = sn.node
            did = node.metadata.get("doc_id")
            if did:
                bundle.append({
                    "page_content": node.get_content(),
                    "metadata": {"doc_id": did},
                })
        results_map[q_id] = bundle

    except Exception as e:
        results_map[q_id] = []
        print(f"\n⚠️ 問題 {q_id} 發生錯誤：{e}")

# ========================
# 5. 輸出
# ========================
with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(results_map, f, ensure_ascii=False, indent=4)

print(f"\n🎉 完成！檢索結果已輸出至 {OUTPUT_FILE_PATH}")
print("下一步：執行 `python evaluate.py` 查看完整報告。")
