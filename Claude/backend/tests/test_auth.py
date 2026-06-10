import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_user_can_register():
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data

def test_user_cannot_register_existing_email():
    client.post(
        "/api/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/register",
        json={"email": "duplicate@example.com", "password": "password456"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_user_can_login():
    client.post(
        "/api/auth/register",
        json={"email": "login@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_user_cannot_login_invalid_credentials():
    client.post(
        "/api/auth/register",
        json={"email": "wronglogin@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "wronglogin@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    
    response2 = client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"}
    )
    assert response2.status_code == 401

def test_protected_route():
    client.post(
        "/api/auth/register",
        json={"email": "protected@example.com", "password": "password123"}
    )
    login_res = client.post(
        "/api/auth/login",
        json={"email": "protected@example.com", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "protected@example.com"
    
    response2 = client.get(
        "/api/users/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response2.status_code == 401
