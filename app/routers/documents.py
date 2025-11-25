from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os, shutil
from app.db import SessionLocal
from app.crud import create_document, list_documents, get_document, update_document_parsed
from app.services.parsers import extract_text_from_pdf, extract_basic_fields

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload", summary="Upload a document file")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    storage_dir = os.getenv("DOCUMENT_STORAGE", "./data/documents")
    os.makedirs(storage_dir, exist_ok=True)
    filename = file.filename
    dest_path = os.path.join(storage_dir, filename)
    # save file
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    doc = create_document(db, filename=filename, storage_path=dest_path, source="upload")
    # parse immediately (sync)
    try:
        text = extract_text_from_pdf(dest_path)
        parsed = extract_basic_fields(text)
        update_document_parsed(db, doc.id, content=text, parsed=parsed, status="done")
    except Exception as e:
        update_document_parsed(db, doc.id, content=None, parsed={"error": str(e)}, status="error")
    return {"id": doc.id, "filename": filename}

@router.get("/", summary="List documents")
def docs(db: Session = Depends(get_db)):
    rows = list_documents(db)
    results = []
    for r in rows:
        parsed = r.parsed_json
        results.append({
            "id": r.id,
            "filename": r.filename,
            "source": r.source,
            "sender": r.sender,
            "received_at": r.received_at,
            "status": r.status,
            "parsed": parsed
        })
    return results

@router.get("/{doc_id}", summary="Get document")
def get_doc(doc_id: int, db: Session = Depends(get_db)):
    r = get_document(db, doc_id)
    if not r:
        raise HTTPException(404, "Not found")
    return {
        "id": r.id,
        "filename": r.filename,
        "storage_path": r.storage_path,
        "content": r.content,
        "parsed": r.parsed_json,
        "status": r.status
    }

@router.post("/{doc_id}/reparse")
def reparse(doc_id: int, db: Session = Depends(get_db)):
    doc = get_document(db, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    try:
        text = extract_text_from_pdf(doc.storage_path)
        parsed = extract_basic_fields(text)
        updated = update_document_parsed(db, doc_id, content=text, parsed=parsed, status="done")
        return {"success": True}
    except Exception as e:
        update_document_parsed(db, doc_id, content=None, parsed={"error": str(e)}, status="error")
        raise HTTPException(500, detail=str(e))
