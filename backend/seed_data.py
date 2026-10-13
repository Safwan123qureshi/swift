import sys
import os

# Windows consoles default to cp1252 which cannot print emoji (e.g. the check
# mark). Reconfigure stdout to UTF-8 so seeding output never crashes.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Parent directory ko Python path mein add karna
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal, engine
from app.database.models import Base, Client, Assistant, KnowledgeChunk

# Database tables ensure karna
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    try:
        # Check agar pehle se client majood hai
        existing_client = db.query(Client).filter(Client.name == "Swift Sign Group").first()
        if existing_client:
            print("Database already seeded!")
            print(f"✅ Existing Client ID: {existing_client.id}")
            return

        # 1. Test Client create karna
        client = Client(name="Swift Sign Group", status="active")
        db.add(client)
        db.commit()
        db.refresh(client)

        # 2. Test Assistant Settings create karna
        assistant = Assistant(
            client_id=client.id,
            name="Swift Sign AI",
            welcome_message="Hello! How can I help you today?",
            tone="professional",
            system_prompt="You are a polite AI assistant for Swift Sign Group. Provide concise and helpful info."
        )
        db.add(assistant)

        # 3. Test Knowledge Chunks create karna
        chunks = [
            KnowledgeChunk(
                client_id=client.id,
                chunk_text="Swift Sign IT Solutions located at Pakland City Center, Islamabad provides Web Development, Cyber Security Audits, and Mobile App Development."
            ),
            KnowledgeChunk(
                client_id=client.id,
                chunk_text="Swift Sign Business Management handles UAE Company Formation, Commercial Licensing, and Financial Advisory. Contact: info@swiftsignbm.com."
            )
        ]
        db.add_all(chunks)
        db.commit()

        print(f"✅ Success! Seeded Client ID: {client.id}")
        print("Is Client ID ko copy kar lein, hum test request mein yeh ID bhejenge.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()