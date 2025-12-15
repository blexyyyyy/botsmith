import requests
import json
import time
import os
from pathlib import Path

# Config
API_URL = "http://localhost:8000"
PROJECT_NAME = "e2e_test_bot"
PROMPT = "Create a simple calculator bot that adds two numbers."

def test_generation():
    print(f"🚀 Starting E2E Generation for '{PROJECT_NAME}'...")
    
    url = f"{API_URL}/bot/stream"
    params = {"prompt": PROMPT, "project_name": PROJECT_NAME}
    
    try:
        with requests.get(url, params=params, stream=True, timeout=300) as r:
            if r.status_code != 200:
                print(f"❌ Failed to connect: {r.status_code}")
                print(r.text)
                return False
            
            print("✅ Connected to stream. Listening for events...")
            for line in r.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data: "):
                        data_str = decoded[6:]
                        try:
                            data = json.loads(data_str)
                            event_type = data.get("type")
                            
                            if event_type == "log":
                                print(f"📝 [LOG] {data['data']['message']}")
                            elif event_type == "step_start":
                                print(f"⚡ [STEP] {data['data']['step']}")
                            elif event_type == "file_complete":
                                print(f"📄 [FILE] {data['data']['filename']}")
                            elif event_type == "done":
                                status = data['data'].get("status")
                                if status == "success":
                                    print("✅ Generation Complete!")
                                    return True
                                else:
                                    print("❌ Generation Failed!")
                                    return False
                            elif event_type == "error":
                                print(f"❌ [ERROR] {data['data']['message']}")
                                
                        except json.JSONDecodeError:
                            pass
                            
    except Exception as e:
        print(f"❌ Exception during stream: {e}")
        return False

def verify_artifacts():
    print("\n🔍 Verifying Artifacts...")
    
    workspace = Path("workspace") / PROJECT_NAME
    if not workspace.exists():
        print(f"❌ Project directory not found: {workspace}")
        return False
        
    required_files = ["bot.py", "README.md", "requirements.txt"]
    all_exist = True
    
    for f in required_files:
        path = workspace / f
        if path.exists():
            print(f"✅ Found {f}")
            if f == "bot.py":
                content = path.read_text()
                if "def main" in content or "if __name__" in content:
                    print("   - Content looks valid.")
                else:
                    print("   - ⚠️ Content might be empty or invalid.")
        else:
            print(f"❌ Missing {f}")
            all_exist = False
            
    return all_exist

if __name__ == "__main__":
    # Ensure previous run is clean
    # (Optional: Could delete workspace/e2e_test_bot here)
    
    success = test_generation()
    if success:
        artifacts_ok = verify_artifacts()
        if artifacts_ok:
            print("\n🎉 E2E TEST PASSED!")
            exit(0)
        else:
            print("\n⚠️ Generation succeeded but artifacts are missing.")
            exit(1)
    else:
        print("\n❌ E2E TEST FAILED.")
        exit(1)
