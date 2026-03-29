# Mitra AI — Complete Setup Guide
## Zero Cost Stack: Groq + Railway + GitHub Pages

---

## STEP 1: Get Free Groq API Key (2 minutes)
1. Go to: https://console.groq.com
2. Sign up with Google
3. Click API Keys → Create API Key
4. Copy your key (starts with gsk_...)

---

## STEP 2: Setup on your Windows PC

Open Command Prompt (Win+R → type cmd → Enter):

```
# Install Python if not installed: https://python.org/downloads
# Then run:

cd Desktop
git clone https://github.com/YOUR_USERNAME/mitra-ai.git
cd mitra-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Create your .env file
copy backend\.env.example backend\.env
# Now open backend/.env in Notepad and paste your Groq key
```

---

## STEP 3: Run locally to test

```
# In the mitra-ai folder with venv activated:
uvicorn backend.main:app --reload

# Open new browser tab: http://localhost:8000
# Open frontend/index.html in browser
# Test it — talk to Mitra!
```

---

## STEP 4: Deploy backend FREE on Railway

1. Go to: https://railway.app
2. Sign up with GitHub (free)
3. New Project → Deploy from GitHub repo
4. Select your mitra-ai repo
5. Add environment variable: GROQ_API_KEY = your_key
6. Deploy! Railway gives you a free URL like: https://mitra-ai.railway.app

---

## STEP 5: Deploy frontend FREE on GitHub Pages

1. In your repo, go to Settings → Pages
2. Source: Deploy from branch → main → /frontend folder
3. Save — your app is live at: https://YOUR_USERNAME.github.io/mitra-ai

---

## STEP 6: Connect frontend to backend

Open frontend/index.html
Find this line:
  const API_URL = ... 'https://YOUR-RAILWAY-URL.railway.app'
Replace with your actual Railway URL from Step 4.
Commit and push to GitHub.

---

## Total Monthly Cost: ₹0

- Groq API: FREE (rate limited but enough for MVP)
- Railway: FREE tier (500 hours/month)  
- GitHub Pages: FREE forever
- Domain: FREE (.github.io) or buy .in for ₹700/year later

---

## Free tier limits (Groq):
- 30 requests/minute
- 14,400 requests/day
- Perfect for 100-500 early users

---

## What to build next (Week 3-4):
- Add Supabase for persistent chat history (free tier)
- Add voice input using Web Speech API (browser built-in, free)
- Add more languages in the system prompt
- Create WhatsApp bot using Meta's free Cloud API

