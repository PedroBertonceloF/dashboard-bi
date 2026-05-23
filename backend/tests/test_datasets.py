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

@pytest.fixture
def auth_token():
    client.post(
        "/api/auth/register",
        json={"email": "testupload@example.com", "password": "password123"}
    )
    res = client.post(
        "/api/auth/login",
        json={"email": "testupload@example.com", "password": "password123"}
    )
    return res.json()["access_token"]

def test_upload_csv(auth_token):
    # Create a mock CSV file content
    csv_content = b"Date,Category,Value\n2026-01-01,A,10\n2026-01-02,B,20\n"
    
    # Simulate file upload using python-multipart
    files = {"file": ("test.csv", csv_content, "text/csv")}
    
    response = client.post(
        "/api/datasets/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
        files=files
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "dataset_id" in data
    assert data["columns"] == ["Date", "Category", "Value"]
    assert len(data["preview"]) == 2
    assert data["preview"][0]["Date"] == "2026-01-01"

def test_upload_unauthenticated():
    csv_content = b"Date,Category,Value\n2026-01-01,A,10"
    files = {"file": ("test.csv", csv_content, "text/csv")}
    
    response = client.post(
        "/api/datasets/upload",
        files=files
    )
    assert response.status_code == 401

def test_upload_invalid_extension(auth_token):
    txt_content = b"This is a text file, not a CSV"
    files = {"file": ("test.txt", txt_content, "text/plain")}
    
    response = client.post(
        "/api/datasets/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
        files=files
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only CSV files are allowed"
