"""
检查向量数据库状态
"""

import chromadb
import os

def check_database(db_path: str = "./data/vector_db"):
    """检查数据库状态"""

    print("="*50)
    print("📊 向量数据库状态检查")
    print("="*50)

    try:
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_collection("nus_docs")

        count = collection.count()
        print(f"\n✅ 数据库路径: {db_path}")
        print(f"✅ 集合名称: nus_docs")
        print(f"✅ 文档总数: {count}")

        if count > 0:
            # 获取一些示例
            results = collection.get(limit=5)
            print(f"\n📄 示例文档（前5个）:")
            for i, doc in enumerate(results['documents'], 1):
                preview = doc[:100] + "..." if len(doc) > 100 else doc
                metadata = results['metadatas'][i-1] if results['metadatas'] else {}
                print(f"\n   [{i}] 来源: {metadata.get('source', 'Unknown')}")
                print(f"       内容: {preview}")
        else:
            print("\n⚠️  数据库为空！")
            print("💡 请运行 build_vector_db.py 来构建数据库")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("💡 请确保已经运行过 build_vector_db.py")

    print("\n" + "="*50)

if __name__ == "__main__":
    check_database()

