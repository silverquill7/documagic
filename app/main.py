from fastapi import FastAPI
from app.routers.documents import router as documents_router
from app.db import engine
from app import models
from app.security import add_security_headers

app = FastAPI(title="DocuMagic")

# create tables if not using alembic (in development only)
# models.Base.metadata.create_all(bind=engine)

app.include_router(documents_router, prefix="/api/documents")

# add simple middleware to add security headers
add_security_headers(app)
