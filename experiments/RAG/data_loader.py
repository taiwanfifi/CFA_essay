"""
数据加载工具 - 适配 thelma2 数据格式
支持从 qa_dataset.json 加载数据并转换为 RAG 系统可用的格式
"""
import json
import os
from typing import List, Dict, Any
from langchain_core.documents import Document


def load_thelma2_dataset(filepath: str = None) -> tuple[List[Dict[str, Any]], List[Document]]:
    """
    加载 thelma2 格式的数据集
    
    Args:
        filepath: 数据文件路径，如果为 None 则自动查找
    
    Returns:
        questions: List[Dict] - 问题列表，每个包含 id, query, source_text
        documents: List[Document] - 知识库文档列表，每个包含 page_content 和 metadata
    """
    if filepath is None:
        # 尝试多个可能的路径
        possible_paths = [
            "../thelma2/qa_dataset.json",
            "./thelma2/qa_dataset.json",
            "thelma2/qa_dataset.json",
            "../qa_dataset.json",
            "./qa_dataset.json",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                filepath = path
                break
        if filepath is None:
            raise FileNotFoundError(f"找不到数据文件，已尝试以下路径: {possible_paths}")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"找不到数据文件: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 提取问题和知识库
    questions = []
    unique_docs: Dict[str, str] = {}  # doc_id -> text
    
    for item in data:
        qid = item.get("id", "")
        query = item.get("query", "")
        source_text = item.get("source_text", "") or item.get("標準解答", "")
        
        if query:
            questions.append({
                "question_id": str(qid),
                "question": query,
                "source_text": source_text
            })
        
        # 将 source_text 作为知识库文档（使用 id 作为 doc_id）
        if source_text and qid:
            doc_id = f"doc_{qid}"
            # 如果同一个 doc_id 已存在，合并文本（用换行分隔）
            if doc_id in unique_docs:
                unique_docs[doc_id] += f"\n\n{source_text}"
            else:
                unique_docs[doc_id] = source_text
    
    # 转换为 Document 对象
    documents = [
        Document(
            page_content=text,
            metadata={"doc_id": doc_id}
        )
        for doc_id, text in unique_docs.items()
    ]
    
    print(f"📊 加载数据: {len(questions)} 个问题, {len(documents)} 个文档")
    return questions, documents


def load_questions_only(filepath: str = None) -> List[Dict[str, Any]]:
    """仅加载问题列表"""
    questions, _ = load_thelma2_dataset(filepath)
    return questions

