from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    client_id: str
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    client_id: str