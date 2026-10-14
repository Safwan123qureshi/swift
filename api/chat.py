import os
import re
from http.server import BaseHTTPRequestHandler
import json
from typing import Optional, Dict, List

try:
    from backend.knowledge_base import COMPANY_DATA
except ImportError:
    try:
        from knowledge_base import COMPANY_DATA
    except ImportError:
        COMPANY_DATA = {"info": "Swift Sign Group - IT Solutions and Business Management."}

# ── Greeting detection ─────────────────────────────────────────────────────────

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

# Ordered FASTEST / most-reliable first (verified live): the "-latest" and
# preview flash models frequently return 503 UNAVAILABLE under load, so we lead
# with gemini-3.5-flash-lite (sub-second, stable) then gemini-2.5-flash, keeping
# the rest purely as fallbacks.
MODEL_CANDIDATES: List[str] = [
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.8-flash",
]

def get_ai_reply(user_query: str, api_key: str) -> str:
    from google import genai

    full_knowledge = "\n".join(COMPANY_DATA.values())

    system_instruction = f"""
You are the official AI representative for Swift Sign Group of Companies.
Use the following complete knowledge base to answer any questions accurately:
{full_knowledge}

RULES:
1. Respond in English or Roman Urdu (Urdu written in Latin script) depending on user input. DO NOT respond in Devanagari/Hindi script.
2. If the user asks about office locations, services, organic food, Laila Hijab, or any division, provide the exact details from the knowledge base above.
3. Keep answers concise, polite, and professional.
"""

    client = genai.Client(api_key=api_key)
    last_err = None

    for model_name in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_query,
                config={"system_instruction": system_instruction}
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            last_err = e
            continue

    if last_err:
        raise last_err
    return "Thank you for contacting Swift Sign Group."


class handler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "Active",
            "message": "Swift Sign Group AI Server is running."
        }).encode())

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            user_query = (data.get("message") or data.get("question") or "").strip()

            if not user_query:
                reply = "Hello! I am the official AI assistant for Swift Sign Group. How can I help you today?"
                self._respond(200, {"response": reply, "message": reply, "status": "success"})
                return

            greeting_type = detect_greeting(user_query)
            if greeting_type == "urdu":
                reply = "Walaikum Assalam! Main Swift Sign Group ka official AI assistant hoon. Main aapki kya madad kar sakta hoon?"
                self._respond(200, {"response": reply, "message": reply, "status": "success"})
                return
            elif greeting_type == "english":
                reply = "Hello! I am the official AI assistant for Swift Sign Group. How can I help you today?"
                self._respond(200, {"response": reply, "message": reply, "status": "success"})
                return

            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                self._respond(500, {"response": "⚠️ Server configuration error: GEMINI_API_KEY not set.", "status": "error"})
                return

            reply = get_ai_reply(user_query, api_key)
            self._respond(200, {"response": reply, "message": reply, "status": "success"})

        except Exception as e:
            self._respond(500, {"response": f"⚠️ Server error: {str(e)}", "status": "error"})

    def _respond(self, status: int, payload: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
