from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
from typing import Optional

app = FastAPI(title="Mitra AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversations = {}

SYSTEM_PROMPT = """You are Mitra, an AI life co-pilot built specifically for Indians. Reply in the same language the user writes in. Be warm and helpful."""

class ChatRequest(BaseModel):
    user_id: str
    message: str
    language: Optional[str] = "auto"

class ChatResponse(BaseModel):
    reply: str
    user_id: str

@app.get("/")
def root():
    return {"status": "Mitra AI is running", "version": "0.1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")
    
    client = Groq(api_key=api_key)
    
    if req.user_id not in conversations:
        conversations[req.user_id] = []
    history = conversations[req.user_id]
    history.append({"role": "user", "content": req.message})
    
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history[-6:],
            max_tokens=512,
            temperature=0.7,
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        conversations[req.user_id] = history
        return ChatResponse(reply=reply, user_id=req.user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
