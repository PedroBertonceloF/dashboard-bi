import httpx
try:
    res = httpx.get("http://127.0.0.1:8000/docs", timeout=5.0)
    print("Backend Status:", res.status_code)
except Exception as e:
    print("Backend Error:", type(e).__name__, str(e))
