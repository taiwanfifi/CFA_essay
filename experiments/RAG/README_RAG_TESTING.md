# RAG 测试脚本说明

本目录包含四个独立的 RAG 测试脚本，适配 thelma2 数据格式，可在新项目中直接运行。

## 📁 文件结构

```
RAG/
├── data_loader.py              # 数据加载工具（适配 thelma2 格式）
├── rag_agent_pragmatist.py     # LangGraph Agent 多轮检索版本
├── rag_langchain_advanced.py  # LangChain 强化版（rewrite + subquery + hybrid + rerank）
├── rag_llama_index.py          # LlamaIndex 标准版本
├── rag_llama_index_vector.py   # LlamaIndex 纯向量检索版本
└── README_RAG_TESTING.md       # 本说明文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install langchain langchain-openai langchain-milvus langchain-community
pip install langgraph llama-index llama-index-embeddings-openai
pip install pydantic numpy tqdm python-dotenv
```

### 2. 配置环境变量

创建 `.env` 文件或设置环境变量：

```bash
export OPENAI_API_KEY="your-api-key"
```

或在代码中直接设置（不推荐用于生产环境）。

### 3. 准备数据

确保 `../thelma2/qa_dataset.json` 文件存在，或修改 `data_loader.py` 中的路径。

数据格式应为：
```json
[
  {
    "id": 1,
    "query": "问题内容",
    "source_text": "标准答案/知识库内容"
  }
]
```

### 4. 运行测试

#### 选项 1: LangGraph Agent 多轮检索
```bash
python rag_agent_pragmatist.py
```
- 输出: `rag_agent_pragmatist_results.json`
- 特点: 多轮检索，自动规划查询策略

#### 选项 2: LangChain 强化版
```bash
python rag_langchain_advanced.py
```
- 输出: `rag_langchain_advanced_results.json`
- 特点: Query rewrite + Subquery + Hybrid (BM25+Vector) + Rerank

#### 选项 3: LlamaIndex 标准版
```bash
python rag_llama_index.py
```
- 输出: `rag_llama_index_results.json`
- 特点: 使用 LlamaIndex 的完整查询引擎

#### 选项 4: LlamaIndex 纯向量检索
```bash
python rag_llama_index_vector.py
```
- 输出: `rag_llama_index_vector_results.json`
- 特点: 仅使用向量相似度检索，无额外处理

## 📊 输出格式

所有脚本输出统一的 JSON 格式：

```json
{
  "question_id_1": [
    {
      "page_content": "检索到的文档内容",
      "metadata": {
        "doc_id": "doc_1"
      }
    }
  ],
  "question_id_2": [...]
}
```

## 🔧 配置说明

### 通用配置（所有脚本）

- **Embedding 模型**: `text-embedding-3-large` (3072 维)
- **LLM 模型**: `gpt-4o-mini` (用于查询改写、事实提取等)
- **向量数据库**: Milvus Lite (本地文件)

### 各脚本特定配置

#### rag_agent_pragmatist.py
- `RETRIEVER_K = 8`: 每轮检索文档数
- `AGENT_MAX_TURNS = 8`: 最大循环轮数
- `TOP_K_RETURN = 5`: 最终返回的文档数

#### rag_langchain_advanced.py
- `bm25_retriever.k = 20`: BM25 检索数
- `milvus_retriever.k = 20`: 向量检索数
- `reranker.top_n = 8`: Rerank 后保留数
- `weights = [0.4, 0.6]`: BM25 和向量的权重

#### rag_llama_index.py / rag_llama_index_vector.py
- `similarity_top_k = 5`: 返回的相似文档数

## 📝 注意事项

1. **首次运行**: 会建立向量索引，可能需要一些时间
2. **数据路径**: 默认从 `../thelma2/qa_dataset.json` 加载，可根据实际情况修改
3. **API 限制**: 注意 OpenAI API 的调用频率限制
4. **存储空间**: Milvus Lite 数据库文件会保存在当前目录

## 🔄 与原始脚本的区别

1. **数据格式适配**: 使用 `data_loader.py` 统一加载 thelma2 格式数据
2. **路径独立**: 所有路径使用相对路径，便于移植
3. **输出统一**: 所有脚本输出相同格式的 JSON，便于后续评估
4. **代码简化**: 移除了对 `ultimate_rag_challenge_questions.json` 格式的依赖

## 🐛 故障排除

### 找不到数据文件
- 检查 `../thelma2/qa_dataset.json` 是否存在
- 或修改 `data_loader.py` 中的 `filepath` 参数

### Milvus 连接错误
- 确保有写入权限
- 检查 `DB_URI` 路径是否正确

### API 错误
- 检查 `OPENAI_API_KEY` 是否正确设置
- 检查网络连接和 API 配额

## 📈 后续评估

检索结果可用于：
1. 与 thelma2 评估框架集成
2. 计算检索准确率、召回率等指标
3. 对比不同 RAG 策略的效果

