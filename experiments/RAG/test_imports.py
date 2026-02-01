"""
测试所有 RAG 脚本的导入和基本结构
"""
import sys
import os

def test_imports():
    """测试所有必要的导入"""
    print("🔍 测试导入...")
    
    errors = []
    
    # 测试基础库
    try:
        import json
        import itertools
        from typing import List, Dict, Any, Set, TypedDict
        print("✅ 基础库导入成功")
    except Exception as e:
        errors.append(f"基础库: {e}")
    
    # 测试 dotenv
    try:
        from dotenv import load_dotenv
        print("✅ dotenv 导入成功")
    except Exception as e:
        errors.append(f"dotenv: {e}")
    
    # 测试 LangChain
    try:
        from langchain_core.documents import Document
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
        print("✅ LangChain 核心库导入成功")
    except Exception as e:
        errors.append(f"LangChain 核心: {e}")
    
    try:
        from langchain_milvus import Milvus
        print("✅ langchain_milvus 导入成功")
    except Exception as e:
        errors.append(f"langchain_milvus: {e}")
    
    try:
        from langchain_community.retrievers import BM25Retriever
        from langchain.retrievers import EnsembleRetriever
        print("✅ LangChain 检索器导入成功")
    except Exception as e:
        errors.append(f"LangChain 检索器: {e}")
    
    # 测试 LangGraph
    try:
        from langgraph.graph import StateGraph, END
        print("✅ LangGraph 导入成功")
    except Exception as e:
        errors.append(f"LangGraph: {e}")
    
    # 测试 LlamaIndex
    try:
        from llama_index.core import VectorStoreIndex, Document, Settings
        print("✅ LlamaIndex 核心导入成功")
    except Exception as e:
        errors.append(f"LlamaIndex 核心: {e}")
    
    try:
        from llama_index.embeddings.openai import OpenAIEmbedding
        from llama_index.llms.openai import OpenAI
        print("✅ LlamaIndex OpenAI 导入成功")
    except Exception as e:
        errors.append(f"LlamaIndex OpenAI: {e}")
    
    # 测试 Pydantic
    try:
        from pydantic import BaseModel, Field, ConfigDict
        print("✅ Pydantic 导入成功")
    except Exception as e:
        errors.append(f"Pydantic: {e}")
    
    # 测试其他
    try:
        import numpy as np
        from tqdm import tqdm
        print("✅ NumPy, tqdm 导入成功")
    except Exception as e:
        errors.append(f"NumPy/tqdm: {e}")
    
    if errors:
        print("\n❌ 导入错误:")
        for err in errors:
            print(f"   - {err}")
        return False
    else:
        print("\n✅ 所有导入测试通过！")
        return True


def test_data_loader():
    """测试数据加载器"""
    print("\n🔍 测试数据加载器...")
    try:
        from data_loader import load_thelma2_dataset
        questions, docs = load_thelma2_dataset()
        print(f"✅ 数据加载成功: {len(questions)} 个问题, {len(docs)} 个文档")
        return True
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return False


def test_script_syntax():
    """测试脚本语法（不实际运行）"""
    print("\n🔍 测试脚本语法...")
    scripts = [
        "rag_agent_pragmatist.py",
        "rag_langchain_advanced.py",
        "rag_llama_index.py",
        "rag_llama_index_vector.py"
    ]
    
    all_ok = True
    for script in scripts:
        try:
            with open(script, 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, script, 'exec')
            print(f"✅ {script} 语法正确")
        except SyntaxError as e:
            print(f"❌ {script} 语法错误: {e}")
            all_ok = False
        except Exception as e:
            print(f"⚠️ {script} 检查时出错: {e}")
    
    return all_ok


if __name__ == "__main__":
    print("=" * 50)
    print("RAG 脚本测试")
    print("=" * 50)
    
    result1 = test_imports()
    result2 = test_data_loader()
    result3 = test_script_syntax()
    
    print("\n" + "=" * 50)
    if result1 and result2 and result3:
        print("✅ 所有测试通过！")
        print("\n注意: 实际运行需要设置 OPENAI_API_KEY 环境变量")
    else:
        print("❌ 部分测试失败，请检查上述错误")
    print("=" * 50)

