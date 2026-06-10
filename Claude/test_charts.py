import httpx
try:
    with httpx.Client(base_url="http://127.0.0.1:8000") as client:
        res = client.get("/api/datasets/12/charts/timeseries")
        print("Status:", res.status_code)
        print("Body:", repr(res.text))
except Exception as e:
    print(e)
