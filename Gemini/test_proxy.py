import httpx
try:
    res = httpx.post("http://localhost:5173/api/auth/login", json={"email": "a", "password": "b"})
    print("Status:", res.status_code)
    print("Body:", repr(res.text))
except Exception as e:
    print(e)
