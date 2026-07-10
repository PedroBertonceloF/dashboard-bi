import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine

client = TestClient(app)

# Login
client.post("/api/auth/register", json={"email": "debug@teste.com", "password": "password123"})
res = client.post("/api/auth/login", json={"email": "debug@teste.com", "password": "password123"})
token = res.json()["access_token"]

try:
    with open("dados_teste_erros.csv", "rb") as f:
        files = {"file": ("dados_teste_erros.csv", f, "text/csv")}
        print("Uploading...")
        upload_res = client.post("/api/datasets/upload", headers={"Authorization": f"Bearer {token}"}, files=files)
        print("Upload status:", upload_res.status_code)
        if upload_res.status_code != 200:
            print(upload_res.text)
            sys.exit(1)
        
        dataset_id = upload_res.json()["dataset_id"]
        print("Dataset ID:", dataset_id)
        
        mapping = {
            "date_col": "data_cadastro",
            "category_col": "status",
            "value_col": "valor_gasto"
        }
        print("Processing...")
        process_res = client.post(f"/api/datasets/{dataset_id}/process", headers={"Authorization": f"Bearer {token}"}, json=mapping)
        print("Process status:", process_res.status_code)
        if process_res.status_code != 200:
            print(process_res.text)
        else:
            print("Process json:", process_res.json())
except Exception as e:
    import traceback
    traceback.print_exc()
