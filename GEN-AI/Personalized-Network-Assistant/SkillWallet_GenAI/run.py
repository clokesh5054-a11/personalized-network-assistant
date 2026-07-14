import subprocess
import sys
import time

def main():
    print("=================================================================")
    print("Starting Personalized Networking Assistant Local Servers...")
    print("- FastAPI Backend will run at: http://127.0.0.1:8000")
    print("- Streamlit Frontend will run at: http://127.0.0.1:8501")
    print("Press Ctrl+C in this terminal to stop both servers.")
    print("=================================================================")
    
    # 1. Start FastAPI Backend (Port 8000)
    backend_cmd = [
        sys.executable, "-m", "uvicorn", "app.main:app", 
        "--host", "127.0.0.1", "--port", "8000"
    ]
    backend_proc = subprocess.Popen(backend_cmd)
    
    # Brief pause to let backend server initialize port binding
    time.sleep(2.0)
    
    # 2. Start Streamlit Frontend (Port 8501)
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run", "frontend/main.py", 
        "--server.port", "8501", "--server.address", "127.0.0.1"
    ]
    frontend_proc = subprocess.Popen(frontend_cmd)
    
    try:
        # Keep monitoring subprocesses
        while True:
            if backend_proc.poll() is not None:
                print("Backend server stopped unexpectedly. Exiting...")
                break
            if frontend_proc.poll() is not None:
                print("Frontend server stopped unexpectedly. Exiting...")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down both servers gracefully...")
    finally:
        # Terminate subprocesses
        backend_proc.terminate()
        frontend_proc.terminate()
        
        # Await clean process exits
        backend_proc.wait()
        frontend_proc.wait()
        print("Both servers stopped successfully.")

if __name__ == "__main__":
    main()
