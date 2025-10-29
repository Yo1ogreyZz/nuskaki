# RAG Backend

这个文件夹包含 RAG（检索增强生成）系统的后端服务。

## 📁 文件结构

```
rag_backend/
├── data/                      # 数据文件夹
│   ├── txt_files/            # 📝 存放学习数据的 txt 文件（请将 NUS 相关文档放这里）
│   └── vector_db/            # 💾 向量数据库存储位置（自动生成）
├── rag_core.py               # RAG 系统核心逻辑
├── rag_service.py            # FastAPI 服务（提供 HTTP API）
├── build_vector_db.py        # 构建向量数据库的脚本
├── requirements.txt          # Python 依赖
└── start_rag_service.bat     # Windows 启动脚本
```

## 🚀 使用步骤

### 1. 安装 Python 依赖

```bash
cd rag_backend
pip install -r requirements.txt
```

### 2. 准备学习数据

将 NUS 相关的文本文件（.txt 格式）放入 `data/txt_files/` 文件夹。例如：
- nus_facilities.txt
- nus_courses.txt
- nus_student_services.txt
- 等等...

### 3. 构建向量数据库

```bash
python build_vector_db.py
```

这会读取 `data/txt_files/` 中的所有 txt 文件，并构建向量数据库到 `data/vector_db/`。

### 4. 启动 RAG 服务

**方式一：使用批处理文件（推荐）**
```
双击 start_rag_service.bat
```

**方式二：命令行**
```bash
python rag_service.py
```

服务将在 `http://localhost:8000` 启动。

## 📡 API 接口

### POST /api/rag_query

发送查询请求到 RAG 系统。

**请求体：**
```json
{
  "question": "Where is the library?",
  "model": "llama3.2:3b",
  "question_type": "factual",
  "top_k": 5
}
```

**响应：**
```json
{
  "question": "Where is the library?",
  "question_type": "factual",
  "model": "llama3.2:3b",
  "retrieved_docs": [...],
  "answer": "The Central Library is located...",
  "success": true,
  "error": null
}
```

## 🔄 与主项目集成

主项目的 Node.js 后端（`server.js`）会调用这个 RAG 服务的 API。

确保：
1. RAG 服务在 `http://localhost:8000` 运行
2. Node.js 后端在 `http://localhost:3000` 运行
3. Vue 前端通过 Node.js 后端间接访问 RAG 服务

## 📝 注意事项

- 确保 Ollama 服务正在运行（`ollama serve`）
- 确保已经下载了模型（`ollama pull llama3.2:3b`）
- 每次更新 txt 文件后，需要重新运行 `build_vector_db.py`
- 向量数据库使用 ChromaDB，数据持久化在 `data/vector_db/` 文件夹

