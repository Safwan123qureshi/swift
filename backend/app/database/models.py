from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.session import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    status = Column(String, default="active")  # active, suspended
    created_at = Column(DateTime, default=datetime.utcnow)

    assistants = relationship("Assistant", back_populates="client")
    business_units = relationship("BusinessUnit", back_populates="client")
    knowledge_chunks = relationship("KnowledgeChunk", back_populates="client")

class Assistant(Base):
    __tablename__ = "assistants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    name = Column(String, nullable=False)
    welcome_message = Column(Text, default="Hello! How can I help you today?")
    tone = Column(String, default="professional")
    system_prompt = Column(Text, nullable=True)

    client = relationship("Client", back_populates="assistants")

class BusinessUnit(Base):
    __tablename__ = "business_units"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    name = Column(String, nullable=False)

    client = relationship("Client", back_populates="business_units")
    knowledge_chunks = relationship("KnowledgeChunk", back_populates="business_unit")

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    business_unit_id = Column(String, ForeignKey("business_units.id"), nullable=True)
    chunk_text = Column(Text, nullable=False)
    
    # Metadata fields as per PDF spec
    category = Column(String, default="general")
    visibility = Column(String, default="public")  # public, internal, confidential, secret
    status = Column(String, default="approved")    # draft, approved, archived
    version = Column(String, default="1.0")

    client = relationship("Client", back_populates="knowledge_chunks")
    business_unit = relationship("BusinessUnit", back_populates="knowledge_chunks")