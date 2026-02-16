import requests
import time

print("Testing chatbot endpoint...")
start = time.time()

try:
    response = requests.post(
        "http://localhost:8001/api/chatbot/message",
        json={"message": "hello"},
        timeout=8
    )
    elapsed = time.time() - start
    print(f"SUCCESS in {elapsed:.2f}s")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except requests.exceptions.Timeout:
    elapsed = time.time() - start
    print(f"TIMEOUT after {elapsed:.2f}s")
except Exception as e:
    elapsed = time.time() - start
    print(f"ERROR after {elapsed:.2f}s: {type(e).__name__}: {e}")
