import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. Load your API key from the .env file 
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app = FastAPI()

# 2. Allow your frontend (GitHub Pages) to talk to this backend 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your GitHub Pages URL
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# 3. Setting the "Bada Bhai" Personality
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are Mitra AI, a supportive 'Bada Bhai' (Big Brother) and mentor for Indian students and founders. "
        "Your tone is encouraging, witty, and relatable. Use simple English mixed with occasional Hinglish. "
        "If a user makes a grammar mistake, gently guide them. If they talk about startups, inspire them. "
        "Keep responses concise and helpful."
    )
}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Calling Groq API (within free tier limits: 30 requests/min) 
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[SYSTEM_PROMPT, {"role": "user", "content": request.message}],
            temperature=0.7,
            max_tokens=500,
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
