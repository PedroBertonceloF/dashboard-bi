import httpx
try:
    with httpx.Client(base_url="http://127.0.0.1:8000") as client:
        res = client.get("/openapi.json")
        if res.status_code == 200:
            openapi = res.json()
            paths = list(openapi.get("paths", {}).keys())
            print("Registered paths:")
            for p in paths:
                print(p)
        else:
            print("Failed to fetch openapi.json:", res.status_code)
except Exception as e:
    print(e)
