"""
RAG FastAPI 服务
用于提供 HTTP API 接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from rag_core import RAGSystem

# 请求模型
class QueryRequest(BaseModel):
    question: str
    model: str = "llama3.2:3b"
    question_type: str = "factual"
    top_k: int = 5

app = FastAPI(title="NUS RAG Service")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 RAG 系统
print("正在初始化 RAG 系统...")
rag = RAGSystem(db_path="./data/vector_db")
print("✅ RAG 系统初始化完成")

@app.get("/")
def root():
    return {"message": "NUS RAG Service is running", "status": "ok"}

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "RAG Service"}

@app.post("/api/rag_query")
def rag_query(req: QueryRequest):
    """RAG 查询接口"""
    if not req.question:
        raise HTTPException(status_code=400, detail="question cannot be empty")

    try:
        result = rag.query(
            req.question,
            model=req.model,
            question_type=req.question_type,
            top_k=req.top_k
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("=================================")
    print("🚀 启动 RAG 服务")
    print("📍 运行地址: http://localhost:8000")
    print("📚 数据库路径: ./data/vector_db")
    print("=================================")
    uvicorn.run("rag_service:app", host="0.0.0.0", port=8000, reload=False)

