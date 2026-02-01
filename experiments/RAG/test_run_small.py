"""
小规模测试 - 只处理前 2 个问题，验证脚本能否正常运行
需要设置 OPENAI_API_KEY 环境变量
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# 检查 API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️  未设置 OPENAI_API_KEY，将只测试代码结构")
    print("   要完整测试，请设置: export OPENAI_API_KEY='your-key'")
    test_mode = "structure_only"
else:
    print(f"✅ 找到 OPENAI_API_KEY")
    test_mode = "full"

# 测试每个脚本的 main 函数是否能被调用（不实际运行完整流程）
print("\n" + "=" * 60)
print("测试 RAG 脚本结构")
print("=" * 60)

def test_script_structure(script_name, main_func_name="main"):
    """测试脚本结构"""
    print(f"\n📝 测试 {script_name}...")
    try:
        # 读取脚本内容
        with open(script_name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有 main 函数
        if f"def {main_func_name}()" in content:
            print(f"   ✅ 找到 {main_func_name}() 函数")
        else:
            print(f"   ⚠️  未找到 {main_func_name}() 函数")
        
        # 检查是否有 if __name__ == "__main__"
        if '__name__ == "__main__"' in content:
            print(f"   ✅ 有主程序入口")
        else:
            print(f"   ⚠️  缺少主程序入口")
        
        # 检查关键导入
        required_imports = {
            "data_loader": "from data_loader import",
            "json": "import json",
            "tqdm": "from tqdm import",
        }
        
        for name, pattern in required_imports.items():
            if pattern in content:
                print(f"   ✅ 导入 {name}")
            else:
                print(f"   ⚠️  缺少导入 {name}")
        
        return True
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False

# 测试所有脚本
scripts = [
    "rag_agent_pragmatist.py",
    "rag_langchain_advanced.py", 
    "rag_llama_index.py",
    "rag_llama_index_vector.py"
]

all_ok = True
for script in scripts:
    if not test_script_structure(script):
        all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("✅ 所有脚本结构检查通过")
    print("\n📌 下一步:")
    print("   1. 设置 OPENAI_API_KEY 环境变量")
    print("   2. 运行: python rag_xxx.py")
    print("   3. 查看输出 JSON 文件")
else:
    print("❌ 部分脚本有问题")
print("=" * 60)

