"""
构建向量数据库
从 txt_files 文件夹读取文本文件并构建向量数据库
"""

import chromadb
import os
from pathlib import Path

def build_vector_db(txt_folder: str = "./data/txt_files", db_path: str = "./data/vector_db"):
    """
    从 txt 文件构建向量数据库

    Args:
        txt_folder: 存放 txt 文件的文件夹路径
        db_path: 向量数据库保存路径
    """

    print(f"📚 开始构建向量数据库...")
    print(f"📂 读取文件夹: {txt_folder}")
    print(f"💾 数据库路径: {db_path}")

    # 初始化 ChromaDB
    client = chromadb.PersistentClient(path=db_path)

    # 删除旧的集合（如果存在）
    try:
        client.delete_collection("nus_docs")
        print("🗑️ 删除旧数据库")
    except:
        pass

    # 创建新集合
    collection = client.create_collection("nus_docs")
    print("✅ 创建新数据库")

    # 读取所有 txt 文件
    txt_folder_path = Path(txt_folder)
    txt_files = list(txt_folder_path.glob("*.txt"))

    if not txt_files:
        print(f"⚠️ 警告: {txt_folder} 文件夹中没有找到 txt 文件")
        print("💡 提示: 请将 NUS 相关的文本文件放入 data/txt_files/ 文件夹")
        return

    print(f"📄 找到 {len(txt_files)} 个文本文件")

    # 处理每个文件
    all_documents = []
    all_metadatas = []
    all_ids = []

    doc_id = 0
    for txt_file in txt_files:
        print(f"   处理: {txt_file.name}")

        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 简单分块（按段落）
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        for para in paragraphs:
            if len(para) > 50:  # 只保留有意义的段落
                all_documents.append(para)
                all_metadatas.append({
                    'source': txt_file.name,
                    'type': 'document'
                })
                all_ids.append(f"doc_{doc_id}")
                doc_id += 1

    # 添加到数据库
    if all_documents:
        print(f"💾 正在添加 {len(all_documents)} 个文档块到数据库...")
        collection.add(
            documents=all_documents,
            metadatas=all_metadatas,
            ids=all_ids
        )
        print(f"✅ 向量数据库构建完成！共 {len(all_documents)} 个文档块")
    else:
        print("⚠️ 没有有效的文档内容")

    print("\n" + "="*50)
    print("📊 数据库统计:")
    print(f"   文件数: {len(txt_files)}")
    print(f"   文档块数: {len(all_documents)}")
    print(f"   数据库路径: {db_path}")
    print("="*50)

if __name__ == "__main__":
    build_vector_db()

