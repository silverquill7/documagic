import pytest
from app import create_app

def test_register_user(client):
    response = client.post('/register', data={
        'email': 'test@example.com',
        'password': 'Password123'
    })
    assert response.status_code == 200

def test_login_success(client):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'Password123'
    })
    assert response.status_code == 200
