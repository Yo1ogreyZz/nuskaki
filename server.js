const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 3000;

// 中间件
app.use(cors());
app.use(express.json());

// RAG 服务 API 配置
const RAG_SERVICE_API = 'http://localhost:8000/api/rag_query';
const MODEL_NAME = 'llama3.2:3b';

// 聊天接口（使用 RAG 增强）
app.post('/api/chat', async (req, res) => {
  try {
    const { prompt, question_type = 'factual', top_k = 5 } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: '消息不能为空' });
    }

    console.log('收到用户消息:', prompt);
    console.log('问题类型:', question_type);

    // 调用 RAG 服务 API
    const response = await axios.post(RAG_SERVICE_API, {
      question: prompt,
      model: MODEL_NAME,
      question_type: question_type,
      top_k: top_k
    }, {
      timeout: 120000  // 2分钟超时
    });

    console.log('RAG 服务响应成功');
    console.log('检索到的文档数:', response.data.retrieved_docs?.length || 0);

    // 返回给前端
    res.json({
      success: response.data.success,
      response: response.data.answer,
      retrieved_docs: response.data.retrieved_docs,
      model: response.data.model,
      question_type: response.data.question_type
    });

  } catch (error) {
    console.error('RAG 服务错误:', error.message);

    if (error.code === 'ECONNREFUSED') {
      res.status(503).json({
        error: 'RAG 服务未启动',
        details: '请确保 RAG 服务正在运行 (python rag_service.py)'
      });
    } else if (error.response) {
      res.status(error.response.status).json({
        error: 'RAG 服务返回错误',
        details: error.response.data
      });
    } else {
      res.status(500).json({
        error: '服务器错误',
        details: error.message
      });
    }
  }
});

// 健康检查接口
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: '服务器运行正常' });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`=================================`);
  console.log(`🚀 后端服务器已启动!`);
  console.log(`📍 运行地址: http://localhost:${PORT}`);
  console.log(`🤖 使用模型: ${MODEL_NAME} (RAG 增强)`);
  console.log(`🔗 RAG 服务: ${RAG_SERVICE_API}`);
  console.log(`=================================`);
  console.log(`⚠️  请确保以下服务正在运行:`);
  console.log(`   1. Ollama 服务 (ollama serve)`);
  console.log(`   2. RAG 服务 (python rag_service.py)`);
  console.log(`=================================`);
});

