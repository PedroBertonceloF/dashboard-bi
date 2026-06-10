import httpx

with open("adocao_ia_DIRTY.csv", "rb") as f:
    files = {"file": ("test.csv", f, "text/csv")}
    
    with httpx.Client(base_url="http://127.0.0.1:8000") as client:
        res = client.post("/api/auth/login", json={"email": "teste2@teste.com", "password": "password123"})
        if res.status_code != 200:
            client.post("/api/auth/register", json={"email": "teste2@teste.com", "password": "password123"})
            res = client.post("/api/auth/login", json={"email": "teste2@teste.com", "password": "password123"})
        
        token = res.json()["access_token"]
        
        upload_res = client.post("/api/datasets/upload", headers={"Authorization": f"Bearer {token}"}, files=files)
        print("Upload status:", upload_res.status_code)
        print("Upload response:", upload_res.text)
        
        if upload_res.status_code == 200:
            dataset_id = upload_res.json()["dataset_id"]
            mapping = {
                "date_col": "Data",
                "category_col": "Setor",
                "value_col": "Valor_Investido"
            }
            process_res = client.post(f"/api/datasets/{dataset_id}/process", headers={"Authorization": f"Bearer {token}"}, json=mapping)
            print("Process status:", process_res.status_code)
            print("Process response:", process_res.text)
