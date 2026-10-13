from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import traceback

from app.database.session import get_db
from app.core.rag_engine import RAGEngine

router = APIRouter(prefix="/api", tags=["Chat"])

class ChatRequest(BaseModel):
    client_id: str
    question: str

@router.post("/chat")
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        rag = RAGEngine(db)
        answer = rag.query(client_id=request.client_id, question=request.question)
        return {"response": answer}
    except Exception as e:
        # Yeh line terminal par poora error print kar degi
        print("--- CHAT ERROR TRACEBACK ---")
        traceback.print_exc()
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))