const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 3000;

// 中间件
app.use(cors());
app.use(express.json());

// Ollama API 配置
const OLLAMA_API = 'http://localhost:11434/api/generate';
const MODEL_NAME = 'llama3.2:3b';

// 聊天接口
app.post('/api/chat', async (req, res) => {
  try {
    const { prompt } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: '消息不能为空' });
    }

    console.log('收到用户消息:', prompt);

    // 调用 Ollama API
    const response = await axios.post(OLLAMA_API, {
      model: MODEL_NAME,
      prompt: prompt,
      stream: false
    });

    console.log('Ollama 响应:', response.data.response);

    res.json({
      success: true,
      response: response.data.response
    });

  } catch (error) {
    console.error('Ollama API 错误:', error.message);

    if (error.code === 'ECONNREFUSED') {
      res.status(503).json({
        error: 'Ollama 服务未启动，请确保 Ollama 正在运行',
        details: '请在终端运行: ollama serve'
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
  console.log(`🤖 使用模型: ${MODEL_NAME}`);
  console.log(`=================================`);
});

