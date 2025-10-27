#!/usr/bin/env python3
"""
Unified start script for Render deployment
Runs both backend and frontend services
"""

import os
import subprocess
import sys
import time
import signal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables with defaults
os.environ["CHROMA_DB_PATH"] = os.getenv("CHROMA_DB_PATH", "./chroma_db")
os.environ["UPLOAD_DIRECTORY"] = os.getenv("UPLOAD_DIRECTORY", "./uploads")
os.environ["API_BASE_URL"] = os.getenv("API_BASE_URL", "http://localhost:8001")

print("Starting Policy Chat Bot for Render...")
print(f"API_BASE_URL: {os.environ['API_BASE_URL']}")
print()

# Start backend in background
print("Starting backend API on port 8001...")
backend_process = subprocess.Popen(
    [sys.executable, "start_backend.py"],
    stdout=sys.stdout,
    stderr=sys.stderr
)

# Wait for backend to start
print("Waiting for backend to start...")
time.sleep(5)

# Start frontend
print("Starting frontend on port 8501...")
frontend_process = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "chat_interface.py", 
     "--server.port=8501", 
     "--server.address=0.0.0.0"],
    stdout=sys.stdout,
    stderr=sys.stderr
)

# Wait for both processes
def signal_handler(sig, frame):
    print("\nShutting down...")
    backend_process.terminate()
    frontend_process.terminate()
    backend_process.wait()
    frontend_process.wait()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Wait for processes to complete
backend_process.wait()
frontend_process.wait()

