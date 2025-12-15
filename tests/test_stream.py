import requests
import json

url = "http://localhost:8000/bot/stream"
params = {"prompt": "make a hello world bot", "project_name": "test_stream_bot"}

print(f"Connecting to {url}...")
try:
    with requests.get(url, params=params, stream=True) as r:
        print(f"Status Code: {r.status_code}")
        if r.status_code != 200:
            print("Failed to connect!")
            print(r.text)
            exit(1)
            
        print("Connected! Listening for events...")
        for line in r.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                print(f"Received: {decoded}")
                if "done" in decoded:
                    print("Stream completed.")
                    break
except Exception as e:
    print(f"Connection failed: {e}")
