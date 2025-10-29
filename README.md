# NUS Kaki - Your NUS Campus Assistant 🎓

一个集成了 RAG（检索增强生成）技术的 NUS 校园智能助手聊天机器人。

## ✨ 特性

- 🤖 基于本地 Ollama LLM (llama3.2:3b)
- 📚 RAG 增强：基于自定义知识库的智能问答
- 🎨 美观的聊天界面（基于 Vue 3）
- 💬 实时对话功能
- 🔒 完全本地运行，数据隐私安全

## 🏗️ 系统架构

```
前端 (Vue.js)  ←→  Node.js 后端  ←→  RAG 服务 (Python)  ←→  Ollama (LLM)
   :8080              :3000              :8000              :11434
```

## 📋 前置要求

1. **Node.js** (v14+)
2. **Python** (v3.8+)
3. **Ollama** - [下载安装](https://ollama.ai/)
4. **Git**

## 🚀 快速开始

### 1. 安装前端依赖

```bash
npm install
# 或
yarn install
```

### 2. 安装 RAG 服务依赖

```bash
cd rag_backend
pip install -r requirements.txt
```

### 3. 准备学习数据

将 NUS 相关的文本文件（.txt 格式）放入 `rag_backend/data/txt_files/` 文件夹。

已包含示例文件：`sample_nus_info.txt`

### 4. 构建向量数据库

```bash
cd rag_backend
python build_vector_db.py
```

### 5. 启动所有服务

#### 方式一：一键启动（推荐）

确保 Ollama 服务正在运行，然后双击：

```
start-all-services.bat
```

#### 方式二：手动启动

在 4 个不同的终端窗口中依次运行：

```bash
# 终端 1: 启动 Ollama
ollama serve

# 终端 2: 启动 RAG 服务
cd rag_backend
python rag_service.py

# 终端 3: 启动 Node.js 后端
node server.js

# 终端 4: 启动 Vue 前端
npm run serve
```

### 6. 访问应用

打开浏览器访问: **http://localhost:8080**

## 📁 项目结构

```
nuskaki/
├── rag_backend/              # RAG 后端服务
│   ├── data/
│   │   ├── txt_files/       # 📝 存放学习数据（txt 文件）
│   │   └── vector_db/       # 💾 向量数据库（自动生成）
│   ├── rag_core.py          # RAG 核心逻辑
│   ├── rag_service.py       # FastAPI 服务
│   ├── build_vector_db.py   # 构建数据库脚本
│   ├── check_db.py          # 检查数据库脚本
│   └── requirements.txt     # Python 依赖
├── src/                     # Vue 前端源码
│   ├── components/          # 组件
│   ├── assets/             # 静态资源
│   └── App.vue             # 主应用
├── server.js               # Node.js 后端
├── package.json            # Node.js 依赖
├── start-all-services.bat  # 一键启动脚本
└── RAG_SETUP_GUIDE.md      # 详细部署指南
```

## 📚 如何添加新的知识

1. 创建或编辑 `.txt` 文件并放入 `rag_backend/data/txt_files/`
2. 运行 `python build_vector_db.py` 重建数据库
3. 重启 RAG 服务

## 🔧 开发命令

### 前端开发

```bash
# 启动开发服务器
npm run serve

# 构建生产版本
npm run build

# 代码检查
npm run lint
```

### RAG 服务

```bash
# 构建向量数据库
cd rag_backend
python build_vector_db.py

# 检查数据库状态
python check_db.py

# 启动 RAG 服务
python rag_service.py
```

## 🌐 部署到生产环境

详细的部署指南请查看 [RAG_SETUP_GUIDE.md](./RAG_SETUP_GUIDE.md)

简要步骤：

1. **打包前端**: `npm run build`
2. **配置 Nginx** 反向代理
3. **使用 PM2** 运行 Node.js 后端
4. **使用 systemd** 运行 RAG 服务
5. **后台运行** Ollama 服务

## 🐛 常见问题

### Q: RAG 服务无法启动

**A:** 检查 Python 依赖是否完整安装：
```bash
cd rag_backend
pip install -r requirements.txt
```

### Q: 聊天机器人无响应

**A:** 确认以下服务都在运行：
- Ollama (http://localhost:11434)
- RAG 服务 (http://localhost:8000)
- Node.js 后端 (http://localhost:3000)

### Q: 向量数据库为空

**A:** 运行构建脚本：
```bash
cd rag_backend
python build_vector_db.py
```

## 📖 相关文档

- [RAG 完整部署指南](./RAG_SETUP_GUIDE.md)
- [RAG 后端说明](./rag_backend/README.md)
- [Vue CLI 配置](https://cli.vuejs.org/config/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License

## 👥 作者

NUS Kaki Team

---

**享受与 NUS Kaki 的对话吧！** 🎉
