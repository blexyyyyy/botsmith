import subprocess
import time
import os
import sys
import threading
from pathlib import Path

def stream_process_output(process, prefix, color_code):
    """Reads stdout from a process and prints it with a colored prefix."""
    if process.stdout is None:
        return
        
    for line in iter(process.stdout.readline, b''):
        try:
            line_str = line.decode().strip()
            if line_str:
                print(f"\033[{color_code}m[{prefix}] {line_str}\033[0m")
        except:
            pass

def main():
    root_dir = Path(__file__).parent.resolve()
    ui_dir = root_dir / "botsmith-ui"
    
    print("\033[1;36mStarting BotSmith System...\033[0m")

    # 1. Start Backend
    print("🚀 Launching Backend API...")
    # Using python -m uvicorn ensures we use the same python environment
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "botsmith.api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(root_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # Thread to print backend output
    threading.Thread(target=stream_process_output, args=(backend_process, "API", "36"), daemon=True).start()

    # 2. Start Frontend
    print("🎨 Launching Frontend UI...")
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    
    frontend_process = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=str(ui_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # Thread to print frontend output
    threading.Thread(target=stream_process_output, args=(frontend_process, "UI", "35"), daemon=True).start()

    print("\n\033[1;32m✅ System Running!\033[0m")
    print(f"   API: http://localhost:8000")
    print(f"   UI:  http://localhost:5173")
    print("\nPress Ctrl+C to stop.\n")

    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
            
            # Check if processes died
            if backend_process.poll() is not None:
                print("\n❌ Backend died unexpectedly.")
                break
            if frontend_process.poll() is not None:
                print("\n❌ Frontend died unexpectedly.")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        if backend_process.poll() is None:
            backend_process.terminate()
        if frontend_process.poll() is None:
            # npm usually spawns subprocesses, terminate might not kill everything on Windows
            # but it's a best effort for a dev script.
            try:
                if os.name == 'nt':
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(frontend_process.pid)])
                else:
                    frontend_process.terminate()
            except:
                pass
                
    sys.exit(0)

if __name__ == "__main__":
    main()
