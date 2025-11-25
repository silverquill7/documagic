import json
from sqlalchemy.orm import Session
from app import models

def create_document(db: Session, filename: str, storage_path: str, source: str = "upload", sender: str | None = None):
    doc = models.Document(filename=filename, storage_path=storage_path, source=source, sender=sender, status="pending")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def update_document_parsed(db: Session, doc_id: int, content: str, parsed: dict, status: str = "done"):
    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not doc:
        return None
    doc.content = content
    doc.parsed_json = json.dumps(parsed, ensure_ascii=False)
    doc.status = status
    db.commit()
    db.refresh(doc)
    return doc

def list_documents(db: Session, limit=100):
    return db.query(models.Document).order_by(models.Document.received_at.desc()).limit(limit).all()

def get_document(db: Session, doc_id: int):
    return db.query(models.Document).filter(models.Document.id == doc_id).first()
