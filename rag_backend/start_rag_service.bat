@echo off
echo ================================
echo 启动 RAG 服务
echo ================================
cd /d "%~dp0"
python rag_service.py
pause

