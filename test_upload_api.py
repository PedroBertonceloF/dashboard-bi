import httpx

with open("adocao_ia_DIRTY.csv", "rb") as f:
    files = {"file": ("test.csv", f, "text/csv")}
    # First login
    res = httpx.post("http://127.0.0.1:8000/api/auth/login", json={"email": "teste@teste.com", "password": "password123"})
    if res.status_code != 200:
        # try register
        httpx.post("http://127.0.0.1:8000/api/auth/register", json={"email": "teste@teste.com", "password": "password123"})
        res = httpx.post("http://127.0.0.1:8000/api/auth/login", json={"email": "teste@teste.com", "password": "password123"})
    
    token = res.json()["access_token"]
    
    # Upload
    upload_res = httpx.post("http://127.0.0.1:8000/api/datasets/upload", headers={"Authorization": f"Bearer {token}"}, files=files)
    print("Upload status:", upload_res.status_code)
    print("Upload response:", upload_res.text)
