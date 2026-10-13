import sys
import os
from pathlib import Path

# Ensure backend directory is in path
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.append(str(CURRENT_DIR))

from app.database.session import SessionLocal, engine
from app.database.models import Base, Client, Assistant, BusinessUnit, KnowledgeChunk

try:
    from knowledge_base import COMPANY_DATA
except ImportError:
    from backend.knowledge_base import COMPANY_DATA

def seed_database():
    # Re-create tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if default client exists
        client = db.query(Client).filter(Client.name == "Swift Sign Group").first()
        if not client:
            print("Creating Client #001 (Swift Sign Group)...")
            client = Client(name="Swift Sign Group", status="active")
            db.add(client)
            db.flush()

        # Check or create Assistant
        assistant = db.query(Assistant).filter(Assistant.client_id == client.id).first()
        if not assistant:
            assistant = Assistant(
                client_id=client.id,
                name="Swift Sign AI",
                welcome_message="Hello! How can I assist you with Swift Sign services today?",
                tone="professional",
                system_prompt="You are a helpful assistant for Swift Sign Group. Only answer using approved knowledge."
            )
            db.add(assistant)
            db.flush()

        # Seed knowledge chunks from COMPANY_DATA
        print("Syncing multi-division knowledge chunks into database...")
        # Clear old minimal chunks to re-populate full suite
        db.query(KnowledgeChunk).filter(KnowledgeChunk.client_id == client.id).delete()

        chunks_to_add = []
        for key, text in COMPANY_DATA.items():
            category = "corporate" if "corporate" in key else "services"
            chunks_to_add.append(
                KnowledgeChunk(
                    client_id=client.id,
                    chunk_text=text.strip(),
                    category=category,
                    visibility="public",
                    status="approved",
                    version="2.0"
                )
            )

        db.add_all(chunks_to_add)
        db.commit()

        print("Seeding complete successfully!")
        print(f"Default Client ID: {client.id}")
        print(f"Total Knowledge Chunks Seeded: {len(chunks_to_add)}")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()