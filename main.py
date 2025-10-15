# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai.services import base_service

# 创建 FastAPI 应用
app = FastAPI(title="AI Gateway API")


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
async def root():
    return {"message": "AI API is running!"}


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        res = await base_service.chat(request.prompt)
        return {"response": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
