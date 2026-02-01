# run_langchain_advanced_eval.py
# LangChain 強化版：模仿 LlamaIndex pipeline (rewrite + subquery + hybrid + rerank)

import os
import json
from tqdm import tqdm
from typing import List, Dict, Any

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_milvus import Milvus
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import numpy as np

print("--- 🚀 LangChain 強化版 評估器 ---")

# =========================
# 基本設定
# =========================
DATA_FILE_PATH = "./data/ultimate_rag_challenge_questions.json"
OUTPUT_FILE_PATH = "./langchain_advanced_results.json"
DB_PATH = "./langchain_eval_milvus.db"
COLLECTION_NAME = "langchain_advanced_eval_v1"

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("🛑 請先設定 OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)

# =========================
# KB 準備
# =========================
with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
    eval_data = json.load(f)

unique_evidence: Dict[str, str] = {
    ev["doc_id"]: ev["text_snippet"]
    for item in eval_data
    for ev in item.get("gold_evidence", [])
    if ev.get("doc_id") and isinstance(ev.get("text_snippet"), str)
}

docs = [Document(page_content=txt, metadata={"doc_id": did}) for did, txt in unique_evidence.items()]
print(f"📄 Evidence docs: {len(docs)}")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)

bm25_retriever = BM25Retriever.from_documents(chunks)
# bm25_retriever.k = 10
bm25_retriever.k = 20  # ← 10 -> 20


vectorstore = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": DB_PATH},
    collection_name=COLLECTION_NAME,
    drop_old=True,  # always rebuild fresh
    auto_id=True,
)
vectorstore.add_documents(chunks)
# milvus_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
milvus_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})  # ← 10 -> 20

# =========================
# 工具：Query Rewrite
# =========================
rewrite_prompt = ChatPromptTemplate.from_template(
    "Rewrite the following question into a clearer search-friendly query:\n{question}"
)
query_rewriter = (
    {"question": RunnablePassthrough()}
    | rewrite_prompt
    | llm
    | StrOutputParser()
)

# =========================
# 工具：Sub-query decomposition
# =========================
subq_prompt = PromptTemplate.from_template(
    "Decompose the following question into 1-3 sub-questions:\n\n{question}"
)
subq_chain = (
    {"question": RunnablePassthrough()}
    | subq_prompt
    | llm
    | StrOutputParser()
)

def subquery_retrieve(question: str) -> List[Document]:
    sub_queries_str = subq_chain.invoke({"question": question})
    sub_queries = [q.strip() for q in sub_queries_str.split("\n") if q.strip()]
    if not sub_queries:
        return milvus_retriever.invoke(question)

    all_docs = []
    for sq in sub_queries:
        all_docs.extend(milvus_retriever.invoke(sq))
    # unique by doc_id
    uniq = {doc.metadata.get("doc_id"): doc for doc in all_docs}
    return list(uniq.values())


# 追加：Pydantic v2 ConfigDict
from pydantic import ConfigDict
from typing import Sequence

# =========================
# 工具：Reranker (cosine on embeddings)  — 修正版
# =========================
class OpenAIReranker(BaseDocumentCompressor):
    # 宣告為 Pydantic 欄位（不要覆寫 __init__）
    embed: OpenAIEmbeddings
    top_n: int = 5

    # 允許任意型別（OpenAIEmbeddings 不是 pydantic model）
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks=None
    ) -> Sequence[Document]:
        if not documents:
            return []

        # 向量化
        doc_texts = [doc.page_content for doc in documents]
        doc_vecs = self.embed.embed_documents(doc_texts)
        q_vec = self.embed.embed_query(query)

        q = np.asarray(q_vec, dtype=np.float32)
        q_norm = np.linalg.norm(q) or 1.0

        scored = []
        for v, doc in zip(doc_vecs, documents):
            dv = np.asarray(v, dtype=np.float32)
            denom = (np.linalg.norm(dv) * q_norm) or 1.0
            score = float(np.dot(dv, q) / denom)
            # 記到 metadata 方便後續檢視
            md = dict(doc.metadata or {})
            md["rerank_score"] = score
            doc.metadata = md
            scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored[: self.top_n]]


# reranker = OpenAIReranker(embed=embeddings, top_n=5)
reranker = OpenAIReranker(embed=embeddings, top_n=8)

# =========================
# 組合：Hybrid Ensemble + Rewrite + Subquery + Rerank
# =========================
ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, milvus_retriever],
    weights=[0.4, 0.6]  # ← 原 0.5/0.5 改成偏向向量
    # weights=[0.5, 0.5]
)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=ensemble
)


def advanced_retrieve(question: str) -> List[Document]:
    # Step 1: rewrite
    rewritten = query_rewriter.invoke({"question": question}).strip()

    # Step 2: sub-queries（最多 2 條）
    sub_queries_str = subq_chain.invoke({"question": rewritten})
    sub_queries = [q.strip() for q in sub_queries_str.split("\n") if q.strip()]
    sub_queries = sub_queries[:2] or [rewritten]

    # Step 3: hybrid 檢索（一次 batch）
    lists = ensemble.batch(sub_queries)       # List[List[Document]]
    pool = [doc for lst in lists for doc in lst]

    # 去重（以 doc_id）
    uniq = {}
    for d in pool:
        did = d.metadata.get("doc_id")
        if did and did not in uniq:
            uniq[did] = d
    pooled_docs = list(uniq.values())

    # Step 4: rerank on rewritten
    final_docs = reranker.compress_documents(pooled_docs, rewritten)  # top_n=8 已在實例上控制
    return final_docs


# =========================
# 主流程：跑題目
# =========================
print("\n--- 開始處理評估問題 ---")
results_map: Dict[str, List[Dict[str, Any]]] = {}

for qa in tqdm(eval_data, desc="評估進度"):
    qid = qa.get("question_id")
    q = qa.get("question")
    if not qid or not q:
        continue

    try:
        retrieved_docs = advanced_retrieve(q)
        bundle = []
        for doc in retrieved_docs:
            bundle.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata,
            })
        results_map[qid] = bundle
    except Exception as e:
        print(f"⚠️ 問題 {qid} 發生錯誤：{e}")
        results_map[qid] = []

with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(results_map, f, ensure_ascii=False, indent=4)

print(f"\n🎉 完成！檢索結果已輸出至 {OUTPUT_FILE_PATH}")
print("👉 現在你可以執行 `python evaluate.py` 加入這個系統比較。")
