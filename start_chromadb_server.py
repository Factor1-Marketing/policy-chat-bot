#!/usr/bin/env python3
"""
Start ChromaDB server for production
"""

import subprocess
import sys
import os
import time
import requests

def start_chromadb_server():
    """Start ChromaDB HTTP server"""
    
    print("🚀 Starting ChromaDB server for production...")
    
    # ChromaDB server command
    cmd = [
        sys.executable, "-m", "chromadb.cli",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--path", "./chroma_data"
    ]
    
    print(f"Command: {' '.join(cmd)}")
    print("ChromaDB server will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop")
    
    try:
        # Start the server
        process = subprocess.Popen(cmd)
        
        # Wait for server to start
        print("Waiting for server to start...")
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get("http://localhost:8000/api/v1/heartbeat", timeout=1)
                if response.status_code == 200:
                    print("✅ ChromaDB server is running!")
                    break
            except:
                pass
            time.sleep(1)
        else:
            print("❌ ChromaDB server failed to start")
            return False
        
        # Keep running
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping ChromaDB server...")
        process.terminate()
        process.wait()
        print("✅ ChromaDB server stopped")

if __name__ == "__main__":
    start_chromadb_server()



