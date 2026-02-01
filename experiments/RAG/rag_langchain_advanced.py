"""
RAG LangChain Advanced - 强化版检索（rewrite + subquery + hybrid + rerank）
适配 thelma2 数据格式
"""
import os
import json
from tqdm import tqdm
from typing import List, Dict, Any, Sequence

from dotenv import load_dotenv
load_dotenv()

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
from pydantic import ConfigDict
import numpy as np

from data_loader import load_thelma2_dataset

print("--- 🚀 RAG LangChain Advanced (Rewrite + Subquery + Hybrid + Rerank) ---")

# =========================
# 配置
# =========================
OUTPUT_FILE = "./rag_langchain_advanced_results.json"
DB_PATH = "./rag_langchain_advanced_milvus.db"
COLLECTION_NAME = "rag_langchain_advanced_collection"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("🛑 請先設定 OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)

print(f"LLM: gpt-4o-mini")
print(f"Embedding: text-embedding-3-large\n")


# =========================
# 工具：Query Rewrite
# =========================
rewrite_prompt = ChatPromptTemplate.from_template(
    "将以下问题改写为更清晰的搜索友好查询：\n{question}"
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
    "将以下问题分解为 1-3 个子问题：\n\n{question}"
)
subq_chain = (
    {"question": RunnablePassthrough()}
    | subq_prompt
    | llm
    | StrOutputParser()
)


# =========================
# 工具：Reranker
# =========================
class OpenAIReranker(BaseDocumentCompressor):
    embed: OpenAIEmbeddings
    top_n: int = 8
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks=None
    ) -> Sequence[Document]:
        if not documents:
            return []
        
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
            md = dict(doc.metadata or {})
            md["rerank_score"] = score
            doc.metadata = md
            scored.append((score, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored[:self.top_n]]


reranker = OpenAIReranker(embed=embeddings, top_n=8)


# =========================
# 高级检索函数
# =========================
def advanced_retrieve(question: str, ensemble: EnsembleRetriever, reranker: OpenAIReranker) -> List[Document]:
    """执行高级检索流程：rewrite -> subquery -> hybrid -> rerank"""
    # Step 1: rewrite
    rewritten = query_rewriter.invoke({"question": question}).strip()
    
    # Step 2: sub-queries（最多 2 条）
    sub_queries_str = subq_chain.invoke({"question": rewritten})
    sub_queries = [q.strip() for q in sub_queries_str.split("\n") if q.strip()]
    sub_queries = sub_queries[:2] or [rewritten]
    
    # Step 3: hybrid 检索
    lists = ensemble.batch(sub_queries)
    pool = [doc for lst in lists for doc in lst]
    
    # 去重（以 doc_id）
    uniq = {}
    for d in pool:
        did = d.metadata.get("doc_id")
        if did and did not in uniq:
            uniq[did] = d
    pooled_docs = list(uniq.values())
    
    # Step 4: rerank
    final_docs = reranker.compress_documents(pooled_docs, rewritten)
    return final_docs


# =========================
# 主流程
# =========================
def main():
    # 1) 加载数据
    questions, docs = load_thelma2_dataset()
    
    # 2) 文本切片
    print("🔧 准备知识库...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    print(f"   - 原始文档: {len(docs)}, 切片后: {len(chunks)}")
    
    # 3) 建立 BM25 检索器
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 20
    
    # 4) 建立向量检索器
    vectorstore = Milvus(
        embedding_function=embeddings,
        connection_args={"uri": DB_PATH},
        collection_name=COLLECTION_NAME,
        drop_old=True,
        auto_id=True,
    )
    vectorstore.add_documents(chunks)
    milvus_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
    
    # 5) 组合 Ensemble Retriever
    ensemble = EnsembleRetriever(
        retrievers=[bm25_retriever, milvus_retriever],
        weights=[0.4, 0.6]  # 偏向向量检索
    )
    
    print("✅ 检索器准备完成\n")
    
    # 6) 执行检索
    print("--- 开始处理问题 ---")
    results_map: Dict[str, List[Dict[str, Any]]] = {}
    
    for qa in tqdm(questions, desc="处理进度"):
        qid = qa.get("question_id")
        q = qa.get("question")
        if not qid or not q:
            continue
        
        try:
            retrieved_docs = advanced_retrieve(q, ensemble, reranker)
            bundle = []
            for doc in retrieved_docs:
                bundle.append({
                    "page_content": doc.page_content,
                    "metadata": doc.metadata,
                })
            results_map[qid] = bundle
        except Exception as e:
            print(f"⚠️ 问题 {qid} 发生错误：{e}")
            results_map[qid] = []
    
    # 7) 输出结果
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results_map, f, ensure_ascii=False, indent=4)
    
    print(f"\n🎉 完成！检索结果已输出至 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

