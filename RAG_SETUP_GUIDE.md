# NUS Kaki - RAG 集成运行指南

## 📋 系统架构

```
前端 (Vue.js)  ←→  Node.js 后端  ←→  RAG 服务 (Python)  ←→  Ollama (本地 LLM)
   :8080              :3000              :8000              :11434
```

## 🚀 完整启动步骤

### 步骤 1: 安装 Python 依赖

```bash
cd rag_backend
pip install -r requirements.txt
```

### 步骤 2: 准备学习数据（重要！）

1. 将 NUS 相关的文本文件（.txt 格式）放入 `rag_backend/data/txt_files/` 文件夹
2. 目前已有示例文件 `sample_nus_info.txt`，你可以添加更多文件

文件示例：
```
rag_backend/data/txt_files/
├── sample_nus_info.txt          （已包含）
├── nus_facilities.txt           （可添加）
├── nus_student_services.txt     （可添加）
└── nus_courses.txt              （可添加）
```

### 步骤 3: 构建向量数据库

```bash
cd rag_backend
python build_vector_db.py
```

这会读取所有 txt 文件并构建向量数据库到 `data/vector_db/`。

**重要：** 每次更新 txt 文件后，都需要重新运行此脚本！

### 步骤 4: 启动 Ollama 服务

在新的命令行窗口运行：

```bash
ollama serve
```

确保模型已下载：

```bash
ollama pull llama3.2:3b
```

### 步骤 5: 启动 RAG 服务

**方式一：使用批处理文件（推荐）**

双击运行：`rag_backend/start_rag_service.bat`

**方式二：命令行**

```bash
cd rag_backend
python rag_service.py
```

服务启动后会显示：
```
🚀 启动 RAG 服务
📍 运行地址: http://localhost:8000
```

### 步骤 6: 启动 Node.js 后端

**方式一：使用批处理文件**

双击运行：`start-backend.bat`

**方式二：命令行**

```bash
node server.js
```

### 步骤 7: 启动 Vue 前端

**方式一：使用批处理文件**

双击运行：`start-frontend.bat`

**方式二：命令行**

```bash
npm run serve
```

前端将在 `http://localhost:8080` 运行。

## ✅ 验证运行状态

访问以下 URL 检查各服务是否正常：

1. **前端**: http://localhost:8080
2. **Node.js 后端**: http://localhost:3000/api/health
3. **RAG 服务**: http://localhost:8000/api/health
4. **Ollama**: http://localhost:11434

## 🎯 快速启动顺序（记住这个顺序！）

```
1. ollama serve            （终端1 - 保持运行）
2. python rag_service.py   （终端2 - 保持运行）
3. node server.js          （终端3 - 保持运行）
4. npm run serve           （终端4 - 保持运行）
```

或者更简单：

```
1. ollama serve                          （终端1）
2. 双击 start_rag_service.bat           （自动打开新窗口）
3. 双击 start-backend.bat               （自动打开新窗口）
4. 双击 start-frontend.bat              （自动打开新窗口）
```

## 📝 添加新的学习数据

1. 将新的 .txt 文件放入 `rag_backend/data/txt_files/`
2. 运行 `python build_vector_db.py` 重建数据库
3. 重启 RAG 服务（如果正在运行）

## 🔧 常见问题

### Q1: RAG 服务启动失败

**解决方案：**
```bash
# 检查 Python 依赖
cd rag_backend
pip install -r requirements.txt

# 检查端口是否被占用
netstat -ano | findstr :8000
```

### Q2: 向量数据库为空

**解决方案：**
- 确保 `data/txt_files/` 文件夹中有 .txt 文件
- 重新运行 `python build_vector_db.py`

### Q3: Ollama 连接失败

**解决方案：**
```bash
# 启动 Ollama
ollama serve

# 下载模型
ollama pull llama3.2:3b
```

### Q4: 前端无法发送消息

**解决方案：**
- 检查所有 4 个服务是否都在运行
- 检查浏览器控制台的错误信息
- 确认 Node.js 后端能访问 RAG 服务

## 🌐 部署到服务器（Nginx）

### 1. 打包前端

```bash
npm run build
```

### 2. Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 静态文件（前端）
    location / {
        root /path/to/dist;
        try_files $uri $uri/ /index.html;
    }

    # Node.js 后端
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 3. 后端服务部署

在服务器上需要运行：

1. **Ollama 服务** (后台运行)
```bash
nohup ollama serve > ollama.log 2>&1 &
```

2. **RAG 服务** (使用 systemd 或 supervisor)
```bash
cd rag_backend
nohup python rag_service.py > rag.log 2>&1 &
```

3. **Node.js 后端** (使用 PM2)
```bash
pm2 start server.js --name nuskaki-backend
pm2 save
pm2 startup
```

## 📊 数据库统计

运行以下脚本查看向量数据库信息：

```python
# 在 rag_backend 文件夹创建 check_db.py
import chromadb

client = chromadb.PersistentClient(path="./data/vector_db")
collection = client.get_collection("nus_docs")
print(f"文档总数: {collection.count()}")
```

运行：
```bash
cd rag_backend
python check_db.py
```

## 📚 项目文件结构

```
nuskaki/
├── rag_backend/              # RAG 后端服务
│   ├── data/
│   │   ├── txt_files/       # 📝 放置学习数据的 txt 文件
│   │   └── vector_db/       # 💾 向量数据库（自动生成）
│   ├── rag_core.py          # RAG 核心逻辑
│   ├── rag_service.py       # FastAPI 服务
│   ├── build_vector_db.py   # 构建数据库脚本
│   ├── requirements.txt     # Python 依赖
│   └── README.md            # RAG 服务文档
├── server.js                # Node.js 后端
├── src/                     # Vue 前端源码
├── package.json             # Node.js 依赖
└── README.md                # 项目主文档
```

## 🎉 完成！

现在你的 NUS Kaki 聊天机器人已经集成了 RAG 增强功能，可以基于你提供的文档数据进行智能问答！

