"""
测试数据加载器
"""
from data_loader import load_thelma2_dataset, load_questions_only

def test_load_data():
    """测试数据加载"""
    try:
        questions, docs = load_thelma2_dataset()
        print(f"✅ 成功加载数据:")
        print(f"   - 问题数量: {len(questions)}")
        print(f"   - 文档数量: {len(docs)}")
        
        if questions:
            print(f"\n📝 第一个问题示例:")
            print(f"   ID: {questions[0].get('question_id')}")
            print(f"   问题: {questions[0].get('question')[:50]}...")
        
        if docs:
            print(f"\n📄 第一个文档示例:")
            print(f"   Doc ID: {docs[0].metadata.get('doc_id')}")
            print(f"   内容: {docs[0].page_content[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return False

if __name__ == "__main__":
    test_load_data()

