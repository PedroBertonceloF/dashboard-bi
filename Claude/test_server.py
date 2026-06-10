import asyncio
import httpx
import uvicorn
from multiprocessing import Process
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

def run_server():
    from backend.main import app
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

def run_test():
    with open("adocao_ia_DIRTY.csv", "rb") as f:
        files = {"file": ("test.csv", f, "text/csv")}
        with httpx.Client(base_url="http://127.0.0.1:8001") as client:
            res = client.post("/api/auth/register", json={"email": "teste3@teste.com", "password": "password123"})
            res = client.post("/api/auth/login", json={"email": "teste3@teste.com", "password": "password123"})
            token = res.json()["access_token"]
            upload_res = client.post("/api/datasets/upload", headers={"Authorization": f"Bearer {token}"}, files=files)
            print("Upload status:", upload_res.status_code)
            print("Upload response:", upload_res.text)

if __name__ == "__main__":
    p = Process(target=run_server)
    p.start()
    time.sleep(2) # let server start
    try:
        run_test()
    finally:
        p.terminate()
        p.join()
