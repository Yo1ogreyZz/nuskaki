@echo off
echo ==========================================
echo   NUS Kaki - 一键启动所有服务
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查 Ollama 服务...
curl -s http://localhost:11434 >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama 服务未运行！
    echo 💡 请先在新终端运行: ollama serve
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Ollama 服务正常运行
)

echo.
echo [2/4] 启动 RAG 服务...
start "RAG Service" cmd /k "cd /d %~dp0rag_backend && python rag_service.py"
timeout /t 5 /nobreak >nul

echo.
echo [3/4] 启动 Node.js 后端...
start "Node Backend" cmd /k "cd /d %~dp0 && node server.js"
timeout /t 3 /nobreak >nul

echo.
echo [4/4] 启动 Vue 前端...
start "Vue Frontend" cmd /k "cd /d %~dp0 && npm run serve"

echo.
echo ==========================================
echo ✅ 所有服务启动中...
echo ==========================================
echo.
echo 服务地址:
echo   - 前端: http://localhost:8080
echo   - 后端: http://localhost:3000
echo   - RAG:  http://localhost:8000
echo.
echo 按任意键关闭此窗口（其他窗口将继续运行）
echo ==========================================
pause

