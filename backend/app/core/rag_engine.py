import os
import sys
from pathlib import Path
from google import genai
from sqlalchemy.orm import Session
from app.config import settings
from app.database.models import KnowledgeChunk, Assistant, Client

# Import full knowledge base as comprehensive context
try:
    from knowledge_base import KNOWLEDGE_BASE, get_company_context
except ImportError:
    try:
        from backend.knowledge_base import KNOWLEDGE_BASE, get_company_context
    except ImportError:
        KNOWLEDGE_BASE = "Swift Sign Group official services and corporate details."
        get_company_context = lambda b=None: KNOWLEDGE_BASE

class RAGEngine:
    def __init__(self, db: Session):
        self.db = db
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None

    def query(self, client_id: str, question: str) -> str:
        # 1. Prompt Injection & Security Filter
        forbidden_phrases = [
            "ignore previous instructions", 
            "show system prompt", 
            "give me the api key", 
            "act as administrator",
            "show all documents"
        ]
        q_lower = question.lower()
        if any(phrase in q_lower for phrase in forbidden_phrases):
            return "Security Notice: Your request contains unauthorized system instructions and has been blocked."

        # 2. Fetch Client & Assistant Context
        client = self.db.query(Client).filter(Client.id == client_id, Client.status == "active").first()
        if not client:
            return "Invalid or inactive Client ID."

        assistant = self.db.query(Assistant).filter(Assistant.client_id == client_id).first()
        system_prompt = assistant.system_prompt if assistant else "You are a helpful customer service assistant for Swift Sign Group."

        # 3. Retrieve Approved Knowledge Chunks
        chunks = self.db.query(KnowledgeChunk).filter(
            KnowledgeChunk.client_id == client_id,
            KnowledgeChunk.status == "approved",
            KnowledgeChunk.visibility == "public"
        ).all()

        if chunks:
            db_context = "\n\n".join([f"- {c.chunk_text}" for c in chunks])
            context = f"{db_context}\n\n[ADDITIONAL FULL SUBSIDIARY DETAILS]\n{KNOWLEDGE_BASE}"
        else:
            context = KNOWLEDGE_BASE

        # 4. Construct AI Prompt with Multi-Division Awareness
        full_prompt = f"""
{system_prompt}

You represent the Swift Sign Group of Companies and all its subsidiaries (IT & Cyber Solutions, Business Management, Shipping & General Trading, Laila Hijab, Organic Foods, and Corporate Offices).

COMPANY KNOWLEDGE BASE:
{context}

OPERATIONAL GUIDELINES:
- Warmly answer greetings (e.g., 'hi', 'hello', 'assalam o alaikum').
- Answer questions regarding ANY division, office location (Islamabad Pakland City Center, Dubai UAE), services, or contacts accurately using the company knowledge base above.
- Support both English and Roman Urdu based on the user's input. Do not reply in Devanagari/Hindi.
- If an inquiry is completely outside company operations, politely direct the user back to Swift Sign Group services.

User Question: {question}
Answer:
"""

        if not self.client:
            return "Gemini API Key is not configured."

        try:
            response = self.client.models.generate_content(
                model="gemini-flash-latest",
                contents=full_prompt,
            )
            return response.text.strip()
        except Exception as e:
            return f"Error generating AI response: {str(e)}"