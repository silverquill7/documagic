import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_empty():
    response = client.post("/api/documents/upload", files={"file": ("test.txt", b"hello world")})
    assert response.status_code == 200
    body = response.json()
    assert "id" in body

