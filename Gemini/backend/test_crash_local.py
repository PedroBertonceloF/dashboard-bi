from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_db
import models

Base.metadata.create_all(bind=engine)
client = TestClient(app)

client.post("/api/auth/register", json={"email": "crash_test2@teste.com", "password": "password123"})
res = client.post("/api/auth/login", json={"email": "crash_test2@teste.com", "password": "password123"})
token = res.json()["access_token"]

try:
    with open("../adocao_ia_DIRTY.csv", "rb") as f:
        files = {"file": ("adocao_ia_DIRTY.csv", f, "text/csv")}
        upload_res = client.post("/api/datasets/upload", headers={"Authorization": f"Bearer {token}"}, files=files)
        print("Upload status:", upload_res.status_code)
        if upload_res.status_code != 200:
            print(upload_res.text)
        
        dataset_id = upload_res.json()["dataset_id"]
        mapping = {
            "date_col": "Data",
            "category_col": "Setor",
            "value_col": "Valor_Investido"
        }
        process_res = client.post(f"/api/datasets/{dataset_id}/process", headers={"Authorization": f"Bearer {token}"}, json=mapping)
        print("Process status:", process_res.status_code)
        if process_res.status_code != 200:
            print(process_res.text)
            
        print("Process json:", process_res.json())
except Exception as e:
    import traceback
    traceback.print_exc()
