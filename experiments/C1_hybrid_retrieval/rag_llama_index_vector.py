"""
RAG LlamaIndex Vector Only - 纯向量检索版本
适配 thelma2 数据格式
"""
import os
import json
from tqdm import tqdm
from typing import List, Dict, Any

from dotenv import load_dotenv
load_dotenv()

from llama_index.core import (
    Document,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from data_loader import load_thelma2_dataset

print("--- 🚀 RAG LlamaIndex Vector Only (Pure Vector Retrieval) ---")

# =========================
# 配置
# =========================
OUTPUT_FILE = "./rag_llama_index_vector_results.json"
KB_PERSIST_DIR = "./rag_llama_index_vector_storage"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("🛑 請先設定 OPENAI_API_KEY 環境變數")

# 设置 LlamaIndex（LLM 仅作为占位符，实际不使用）
Settings.llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-large", api_key=OPENAI_API_KEY
)

print("✅ LlamaIndex 设置完成：Vector-only mode")
print("   - Embedding: text-embedding-3-large")
print("   - LLM: gpt-4o-mini (not used in query pipeline)\n")


# =========================
# 主流程
# =========================
def main():
    # 1) 加载数据
    questions, docs = load_thelma2_dataset()
    
    # 2) 转换为 LlamaIndex Document 格式
    llama_docs = [
        Document(text=doc.page_content, metadata=doc.metadata)
        for doc in docs
    ]
    
    # 3) 建立或加载索引
    if not os.path.exists(KB_PERSIST_DIR):
        print("📂 建立新索引...")
        print(f"   - 共 {len(llama_docs)} 份文件")
        index = VectorStoreIndex.from_documents(llama_docs, show_progress=True)
        index.storage_context.persist(persist_dir=KB_PERSIST_DIR)
        print("✅ 索引建立完成\n")
    else:
        print("✅ 从既有索引载入")
        storage_context = StorageContext.from_defaults(persist_dir=KB_PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        print()
    
    # 4) 建立纯向量检索器
    retriever = index.as_retriever(similarity_top_k=5)
    
    # 5) 执行检索
    print("--- 开始处理问题 ---")
    results_map: Dict[str, List[Dict[str, Any]]] = {}
    
    for qa in tqdm(questions, desc="处理进度"):
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
            print(f"⚠️ 问题 {qid} 发生错误：{e}")
            results_map[qid] = []
    
    # 6) 输出结果
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results_map, f, ensure_ascii=False, indent=4)
    
    print(f"\n🎉 完成！检索结果已输出至 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

