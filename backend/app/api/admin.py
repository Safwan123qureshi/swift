from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database.session import get_db
from app.database.models import KnowledgeChunk, Client

router = APIRouter()

class KnowledgeCreate(BaseModel):
    client_id: str
    chunk_text: str

class KnowledgeResponse(BaseModel):
    id: int
    client_id: str
    chunk_text: str

    class Config:
        from_attributes = True

# 1. Add new Knowledge Chunk
@router.post("/knowledge", response_model=KnowledgeResponse)
def add_knowledge(data: KnowledgeCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == data.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    chunk = KnowledgeChunk(client_id=data.client_id, chunk_text=data.chunk_text)
    db.add(chunk)
    db.commit()
    db.refresh(chunk)
    return chunk

# 2. Get all Knowledge Chunks for a Client
@router.get("/knowledge/{client_id}", response_model=List[KnowledgeResponse])
def get_knowledge_by_client(client_id: str, db: Session = Depends(get_db)):
    chunks = db.query(KnowledgeChunk).filter(KnowledgeChunk.client_id == client_id).all()
    return chunks

# 3. Delete a Knowledge Chunk
@router.delete("/knowledge/{chunk_id}")
def delete_knowledge(chunk_id: int, db: Session = Depends(get_db)):
    chunk = db.query(KnowledgeChunk).filter(KnowledgeChunk.id == chunk_id).first()
    if not chunk:
        raise HTTPException(status_code=404, detail="Knowledge Chunk not found")
    
    db.delete(chunk)
    db.commit()
    return {"message": f"Knowledge Chunk {chunk_id} deleted successfully"}