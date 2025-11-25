from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    source = Column(String(128), nullable=True)  # e.g., "email", "upload"
    sender = Column(String(255), nullable=True)
    received_at = Column(DateTime, server_default=func.now())
    storage_path = Column(String(1024), nullable=False)
    content = Column(Text, nullable=True)       # full extracted text
    parsed_json = Column(Text, nullable=True)   # JSON string with structured fields
    status = Column(String(50), default="pending")  # pending/processing/done/error
