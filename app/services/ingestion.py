import os
import email
import time
import logging
from imap_tools import MailBox, AND
from app.config import settings
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.crud import create_document, update_document_parsed
from app.services.parsers import extract_text_from_pdf, extract_basic_fields

logger = logging.getLogger("ingestion")
logger.setLevel(logging.INFO)

def save_attachment(msg, att, storage_dir):
    filename = att.filename or "attachment"
    safe_name = filename.replace("/", "_").replace("\\", "_")
    path = os.path.join(storage_dir, safe_name)
    with open(path, "wb") as f:
        f.write(att.payload)
    return path

def process_attachment_file(db: Session, doc_id: int, file_path: str):
    try:
        text = extract_text_from_pdf(file_path)
        parsed = extract_basic_fields(text)
        update_document_parsed(db, doc_id, content=text, parsed=parsed, status="done")
        logger.info("Parsed and saved doc %s", doc_id)
    except Exception as e:
        logger.exception("Error parsing file %s: %s", file_path, e)
        update_document_parsed(db, doc_id, content=None, parsed={"error": str(e)}, status="error")

def poll_mailbox_once():
    storage = settings.DOCUMENT_STORAGE
    os.makedirs(storage, exist_ok=True)
    with MailBox(settings.IMAP_HOST, settings.IMAP_PORT).login(settings.IMAP_USER, settings.IMAP_PASS) as mailbox:
        # only unseen emails
        for msg in mailbox.fetch(AND(seen=False)):
            sender = msg.from_
            subject = msg.subject
            for att in msg.attachments:
                path = save_attachment(msg, att, storage)
                db = SessionLocal()
                doc = create_document(db, filename=os.path.basename(path), storage_path=path, source="email", sender=sender)
                # process attachment asynchronously / in same process for now
                process_attachment_file(db, doc.id, path)
                db.close()
            # mark seen
            mailbox.flag(msg.uid, MailBox.Flag.SEEN)

def run_loop():
    logger.info("Starting IMAP ingestion loop...")
    while True:
        try:
            poll_mailbox_once()
        except Exception as e:
            logger.exception("Error in ingestion loop: %s", e)
        time.sleep(settings.EMAIL_POLL_INTERVAL)

# a simple entrypoint for running this worker
if __name__ == "__main__":
    run_loop()
