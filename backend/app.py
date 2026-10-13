#.\venv\Scripts\python.exe run.py
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

try:
    from backend.knowledge_base import KNOWLEDGE_BASE
except ImportError:
    try:
        from knowledge_base import KNOWLEDGE_BASE
    except ImportError:
        KNOWLEDGE_BASE = "Swift Sign Group official services and corporate details."

from typing import Optional, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    brand: Optional[str] = None
    message: Optional[str] = None
    question: Optional[str] = None
    client_id: Optional[str] = None

MODEL_CANDIDATES: List[str] = [
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-flash-latest"
]

import re

ROMAN_URDU_GREETINGS = [
    "salam", "slm", "salaam", "asalam", "assalam", "aslam",
    "asalamoaliom", "aslamoalikum", "asalamoalikum", "asalamoalaikum",
    "assalam o alaikum", "asalam o alaikum", "assalam-o-alaikum",
    "assalam u alaikum", "asalamu alaikum", "assalamu alaikum",
    "assalam alaikum", "asalam alaikum", "salam alaikum",
    "kese ho", "kaise ho", "kese hain", "kaise hain",
    "kya haal hai", "kia hal ha", "kia haal hai", "kia hal", "kya haal",
    "kese ho aap", "kaise ho aap", "theek ho", "thik ho", "adaab", "aadab"
]

ENGLISH_GREETINGS = [
    "hi", "hello", "hey", "how are you", "how are you doing",
    "how r u", "how do you do", "good morning", "good afternoon",
    "good evening", "hi there", "hello there", "greetings"
]

def normalize_text(text: str) -> str:
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    return " ".join(cleaned.split())

def detect_greeting(text: str) -> Optional[str]:
    norm = normalize_text(text)
    if not norm:
        return "english"
    words = norm.split()
    for g in ROMAN_URDU_GREETINGS:
        pattern = r"\b" + re.escape(g) + r"\b"
        if norm == g or (len(words) <= 4 and re.search(pattern, norm)):
            return "urdu"
    for g in ENGLISH_GREETINGS:
        pattern = r"\b" + re.escape(g) + r"\b"
        if norm == g or (len(words) <= 4 and re.search(pattern, norm)):
            return "english"
    return None

@app.get("/")
@app.get("/status")
@app.get("/api/status")
def status():
    return {"status": "Active", "message": "Swift Sign Group AI Server is running."}

@app.post("/chat")
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        user_query = (request.question or request.message or "").strip()
        if not user_query:
            eng_default = "Hello! I am the official AI assistant for Swift Sign Group. How can I help you today?"
            return {"response": eng_default, "answer": eng_default, "message": eng_default, "status": "success"}

        greeting_type = detect_greeting(user_query)
        if greeting_type == "urdu":
            urdu_reply = "Walaikum Assalam! Main Swift Sign Group ka official AI assistant hoon. Main aapki kya madad kar sakta hoon?"
            return {"response": urdu_reply, "answer": urdu_reply, "message": urdu_reply, "status": "success"}
        elif greeting_type == "english":
            eng_reply = "Hello! I am the official AI assistant for Swift Sign Group. How can I help you today?"
            return {"response": eng_reply, "answer": eng_reply, "message": eng_reply, "status": "success"}

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"response": "⚠️ GEMINI_API_KEY environment variable missing."}

        client = genai.Client(api_key=api_key)

        try:
            from backend.knowledge_base import COMPANY_DATA
            full_knowledge = "\n".join(COMPANY_DATA.values())
        except ImportError:
            try:
                from knowledge_base import COMPANY_DATA
                full_knowledge = "\n".join(COMPANY_DATA.values())
            except ImportError:
                full_knowledge = KNOWLEDGE_BASE

        system_instruction = f"""
You are the official AI representative for Swift Sign Group of Companies.
Use the following complete knowledge base to answer any questions accurately:
{full_knowledge}

RULES:
1. Respond in English or Roman Urdu (Urdu written in Latin script) depending on user input. DO NOT respond in Devanagari/Hindi script.
2. If the user asks about office locations, services, organic food, Laila Hijab, or any division, provide the exact details from the knowledge base above.
3. Keep answers concise, polite, and professional.
"""

        reply_text = None
        last_err = None
        for model_name in MODEL_CANDIDATES:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_query,
                    config={"system_instruction": system_instruction}
                )
                if response and response.text:
                    reply_text = response.text.strip()
                    break
            except Exception as m_err:
                last_err = m_err
                continue

        if not reply_text:
            if last_err:
                raise last_err
            reply_text = "Thank you for contacting Swift Sign Group."

        return {
            "response": reply_text,
            "answer": reply_text,
            "message": reply_text,
            "status": "success"
        }

    except Exception as e:
        return {"response": f"⚠️ Runtime Error: {str(e)}", "status": "error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
