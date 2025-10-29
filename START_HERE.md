# 🚀 NUS Kaki 启动指南

## ⚡ 快速启动（5 步搞定！）

### 第 1 步：安装 Ollama 并下载模型

如果还没安装 Ollama：
1. 访问 https://ollama.ai/ 下载安装
2. 安装完成后，打开命令行运行：

```bash
ollama pull llama3.2:3b
```

### 第 2 步：安装 Python 依赖

打开命令行，进入项目文件夹：

```bash
cd D:\Coding_Nus\nuskaki\rag_backend
pip install -r requirements.txt
```

### 第 3 步：构建向量数据库

```bash
python build_vector_db.py
```

你会看到类似这样的输出：
```
📚 开始构建向量数据库...
📄 找到 1 个文本文件
✅ 向量数据库构建完成！
```

### 第 4 步：启动 Ollama 服务

**打开一个新的命令行窗口**，运行：

```bash
ollama serve
```

保持这个窗口运行！

### 第 5 步：一键启动所有服务

**双击运行**: `start-all-services.bat`

或者在命令行运行：
```bash
cd D:\Coding_Nus\nuskaki
start-all-services.bat
```

等待所有服务启动后，浏览器会自动打开 http://localhost:8080

---

## 🎯 手动启动（如果一键启动不工作）

如果 `start-all-services.bat` 有问题，可以手动启动：

### 1️⃣ 启动 Ollama（如果还没启动）

**新命令行窗口 1:**
```bash
ollama serve
```

### 2️⃣ 启动 RAG 服务

**新命令行窗口 2:**
```bash
cd D:\Coding_Nus\nuskaki\rag_backend
python rag_service.py
```

你应该看到：
```
🚀 启动 RAG 服务
📍 运行地址: http://localhost:8000
```

### 3️⃣ 启动 Node.js 后端

**新命令行窗口 3:**
```bash
cd D:\Coding_Nus\nuskaki
node server.js
```

你应该看到：
```
🚀 后端服务器已启动!
📍 运行地址: http://localhost:3000
```

### 4️⃣ 启动 Vue 前端

**新命令行窗口 4:**
```bash
cd D:\Coding_Nus\nuskaki
npm run serve
```

等待编译完成后，访问：http://localhost:8080

---

## ✅ 验证是否成功

访问以下地址检查：

1. **前端界面**: http://localhost:8080 ✨
2. **Node.js 后端**: http://localhost:3000/api/health
3. **RAG 服务**: http://localhost:8000/api/health
4. **Ollama**: http://localhost:11434

如果都能访问，说明启动成功！🎉

---

## 💡 添加更多学习数据

1. 将 NUS 相关的 txt 文件放入：`rag_backend/data/txt_files/`
2. 重新构建数据库：
   ```bash
   cd rag_backend
   python build_vector_db.py
   ```
3. 重启 RAG 服务

---

## ❌ 遇到问题？

### 问题 1: `pip install` 失败

**解决方案：**
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2: 端口被占用

**解决方案：**
```bash
# 查看端口占用
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :8080

# 结束占用端口的进程
taskkill /PID <进程ID> /F
```

### 问题 3: Ollama 找不到模型

**解决方案：**
```bash
ollama pull llama3.2:3b
```

### 问题 4: RAG 服务启动失败

**解决方案：**
```bash
cd rag_backend
# 检查数据库
python check_db.py

# 如果数据库为空，重建
python build_vector_db.py
```

### 问题 5: 前端无法连接后端

**解决方案：**
- 确认所有 4 个服务都在运行
- 检查浏览器控制台的错误信息（按 F12）
- 确认防火墙没有阻止端口

---

## 📞 需要帮助？

查看详细文档：
- **RAG 部署指南**: `RAG_SETUP_GUIDE.md`
- **项目说明**: `README.md`
- **RAG 后端说明**: `rag_backend/README.md`

---

**祝你使用愉快！** 🎓✨

