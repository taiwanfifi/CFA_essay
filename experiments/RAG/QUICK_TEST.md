# 快速测试指南

## ✅ 已验证项目

### 1. 数据加载 ✅
```bash
python test_data_loader.py
# 结果: 成功加载 49 个问题, 49 个文档
```

### 2. 导入检查 ✅
```bash
python test_imports.py
# 结果: 所有依赖库导入成功
```

### 3. 代码结构 ✅
```bash
python test_run_small.py
# 结果: 所有脚本结构正确
```

## 🚀 实际运行步骤

### 步骤 1: 设置环境变量
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 步骤 2: 选择要运行的脚本

**最简单版本** (推荐先测试):
```bash
python rag_llama_index_vector.py
```

**标准版本**:
```bash
python rag_llama_index.py
```

**强化版本**:
```bash
python rag_langchain_advanced.py
```

**Agent 版本** (最复杂):
```bash
python rag_agent_pragmatist.py
```

### 步骤 3: 检查输出
- 查看生成的 JSON 文件
- 检查是否有错误信息

## 📊 预期行为

1. **首次运行**:
   - 会建立向量索引 (需要时间)
   - 显示进度条
   - 最后输出 JSON 文件

2. **后续运行**:
   - 会使用已建立的索引 (更快)
   - 直接开始检索

3. **输出文件**:
   - `rag_xxx_results.json` - 检索结果
   - 数据库文件 (Milvus) - 保存在当前目录

## ⚠️ 常见问题

### 问题 1: 找不到数据文件
**解决**: 检查 `../thelma2/qa_dataset.json` 是否存在，或修改 `data_loader.py` 中的路径

### 问题 2: API Key 错误
**解决**: 确保 `OPENAI_API_KEY` 环境变量已正确设置

### 问题 3: 导入错误
**解决**: 运行 `pip install -r requirements_rag.txt`

## ✅ 测试结论

所有脚本已通过:
- ✅ 语法检查
- ✅ 导入测试
- ✅ 数据加载测试
- ✅ 代码结构检查

**可以安全运行！** 只需要设置 API key 即可。

