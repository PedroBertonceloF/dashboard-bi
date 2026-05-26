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

def test_process_dataset(auth_token):
    # Upload a file first with some bad rows
    csv_content = b"Data,Setor,Faturamento\n2026-01-01,A,10\n2026-01-02,,20\ninvalid-date,C,30\n2026-01-04,D,not-a-number\n"
    files = {"file": ("test_clean.csv", csv_content, "text/csv")}
    upload_res = client.post(
        "/api/datasets/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
        files=files
    )
    dataset_id = upload_res.json()["dataset_id"]

    # Process and map columns
    mapping = {
        "date_col": "Data",
        "category_col": "Setor",
        "value_col": "Faturamento"
    }
    process_res = client.post(
        f"/api/datasets/{dataset_id}/process",
        headers={"Authorization": f"Bearer {auth_token}"},
        json=mapping
    )
    
    assert process_res.status_code == 200
    data = process_res.json()
    assert data["message"] == "Dataset processed successfully"
    assert data["original_rows"] == 4
    assert data["cleaned_rows"] == 1
    assert data["dropped_rows"] == 3

def test_process_dataset_not_found(auth_token):
    mapping = {"date_col": "Data", "category_col": "Setor", "value_col": "Faturamento"}
    process_res = client.post(
        "/api/datasets/999/process",
        headers={"Authorization": f"Bearer {auth_token}"},
        json=mapping
    )
    assert process_res.status_code == 404

def test_process_dataset_invalid_columns(auth_token):
    csv_content = b"Data,Setor,Faturamento\n2026-01-01,A,10\n"
    files = {"file": ("test_invalid_cols.csv", csv_content, "text/csv")}
    upload_res = client.post(
        "/api/datasets/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
        files=files
    )
    dataset_id = upload_res.json()["dataset_id"]

    mapping = {
        "date_col": "WrongDate",
        "category_col": "Setor",
        "value_col": "Faturamento"
    }
    process_res = client.post(
        f"/api/datasets/{dataset_id}/process",
        headers={"Authorization": f"Bearer {auth_token}"},
        json=mapping
    )
    assert process_res.status_code == 400
    assert "Missing mapped columns" in process_res.json()["detail"]

def test_get_kpis(auth_token):
    # 1. Upload
    csv_content = b"Data,Setor,Valor\n2026-01-01,A,10\n2026-01-02,A,20\n2026-01-03,B,30\n"
    files = {"file": ("test_kpi.csv", csv_content, "text/csv")}
    upload_res = client.post("/api/datasets/upload", headers={"Authorization": f"Bearer {auth_token}"}, files=files)
    dataset_id = upload_res.json()["dataset_id"]

    # 2. Process (Clean)
    mapping = {"date_col": "Data", "category_col": "Setor", "value_col": "Valor"}
    client.post(f"/api/datasets/{dataset_id}/process", headers={"Authorization": f"Bearer {auth_token}"}, json=mapping)

    # 3. Get KPIs
    kpi_res = client.get(f"/api/datasets/{dataset_id}/kpis", headers={"Authorization": f"Bearer {auth_token}"})
    
    assert kpi_res.status_code == 200
    data = kpi_res.json()
    assert data["total_sum"] == 60.0
    assert data["average"] == 20.0
    assert data["row_count"] == 3

def test_get_kpis_uncleaned(auth_token):
    csv_content = b"Data,Setor,Valor\n2026-01-01,A,10\n"
    files = {"file": ("test_kpi_unclean.csv", csv_content, "text/csv")}
    upload_res = client.post("/api/datasets/upload", headers={"Authorization": f"Bearer {auth_token}"}, files=files)
    dataset_id = upload_res.json()["dataset_id"]

    # Do not process it, directly ask for KPIs
    kpi_res = client.get(f"/api/datasets/{dataset_id}/kpis", headers={"Authorization": f"Bearer {auth_token}"})
    
    assert kpi_res.status_code == 400
    assert "must be cleaned" in kpi_res.json()["detail"]

def test_get_charts(auth_token):
    # Upload & Process
    csv_content = b"Data,Setor,Valor\n2026-01-01,A,10\n2026-01-01,A,20\n2026-01-02,B,30\n"
    files = {"file": ("test_charts.csv", csv_content, "text/csv")}
    upload_res = client.post("/api/datasets/upload", headers={"Authorization": f"Bearer {auth_token}"}, files=files)
    dataset_id = upload_res.json()["dataset_id"]
    
    mapping = {"date_col": "Data", "category_col": "Setor", "value_col": "Valor"}
    client.post(f"/api/datasets/{dataset_id}/process", headers={"Authorization": f"Bearer {auth_token}"}, json=mapping)

    # 1. Timeseries
    time_res = client.get(f"/api/datasets/{dataset_id}/charts/timeseries", headers={"Authorization": f"Bearer {auth_token}"})
    assert time_res.status_code == 200
    time_data = time_res.json()
    assert len(time_data) == 2
    assert time_data[0]["date"] == "2026-01-01"
    assert time_data[0]["value"] == 30.0  # 10 + 20
    assert time_data[1]["date"] == "2026-01-02"
    assert time_data[1]["value"] == 30.0

    # 2. Categories
    cat_res = client.get(f"/api/datasets/{dataset_id}/charts/categories", headers={"Authorization": f"Bearer {auth_token}"})
    assert cat_res.status_code == 200
    cat_data = cat_res.json()
    assert len(cat_data) == 2
    assert cat_data[0]["category"] == "A"
    assert cat_data[0]["value"] == 30.0
    assert cat_data[1]["category"] == "B"
    assert cat_data[1]["value"] == 30.0
