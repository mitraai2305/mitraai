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
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY", "placeholder"))
conversations = {}

SYSTEM_PROMPT = """You are Mitra, an AI life co-pilot built specifically for Indians.

Your core abilities:
- You understand Indian documents: Aadhaar, PAN, Voter ID, Ration Card, Passports, ITR forms, land records
- You explain government schemes simply: PM Kisan, Ayushman Bharat, Ujjwala Yojana, PMAY
- You help fill government forms in simple language
- You answer in the SAME language the user writes in: Hindi, Gujarati, Tamil, Telugu, Marathi, Bengali, etc.
- You understand Indian financial context: UPI, EPF, PPF, NPS, ITR filing, GST for small businesses

Rules:
1. Always reply in the same language the user used
2. Be warm, use "aap" in Hindi, appropriate respect in other languages
3. When someone shares a document description, extract key info and explain it simply
4. For government schemes, mention eligibility, benefits, and how to apply
5. Never give medical or legal advice - refer to professionals
6. Keep responses concise - most users are on mobile with slow internet

You are NOT ChatGPT. You are Mitra - India ka apna AI dost."""

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

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if req.user_id not in conversations:
        conversations[req.user_id] = []
    history = conversations[req.user_id]
    history.append({"role": "user", "content": req.message})
    recent_history = history[-10:]
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *recent_history],
            max_tokens=1024,
            temperature=0.7,
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        conversations[req.user_id] = history
        return ChatResponse(reply=reply, user_id=req.user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat/{user_id}")
def clear_chat(user_id: str):
    conversations.pop(user_id, None)
    return {"status": "cleared"}

@app.get("/health")
def health():
    return {"status": "ok"}
