#!/usr/bin/env python3
"""
Policy Chat Bot - Main runner script
This script provides easy commands to run the application
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import fastapi
        import streamlit
        import langchain
        import chromadb
        import openai
        print("✅ All requirements are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in .env file")
        return False
    
    print("✅ Environment configuration is valid")
    return True

def run_backend():
    """Run the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed to start: {e}")

def run_frontend():
    """Run the Streamlit frontend"""
    print("🚀 Starting Streamlit frontend...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "chat_interface.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend failed to start: {e}")

def run_both():
    """Run both backend and frontend concurrently"""
    import threading
    import time
    
    print("🚀 Starting both backend and frontend...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    run_frontend()

def setup_project():
    """Set up the project for first-time use"""
    print("🔧 Setting up Policy Chat Bot...")
    
    # Create necessary directories
    directories = ["uploads", "chroma_db"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Create example .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_example = """OPENAI_API_KEY=your_openai_api_key_here
CHROMA_DB_PATH=./chroma_db
UPLOAD_DIRECTORY=./uploads
MAX_FILE_SIZE=10485760
CHUNK_SIZE=1000
CHUNK_OVERLAP=200"""
        
        with open(".env", "w") as f:
            f.write(env_example)
        print("✅ Created .env file - please add your OpenAI API key")
    else:
        print("✅ .env file already exists")
    
    print("\n🎉 Setup complete!")
    print("Next steps:")
    print("1. Add your OpenAI API key to the .env file")
    print("2. Run: python run.py backend")
    print("3. In another terminal, run: python run.py frontend")

def main():
    parser = argparse.ArgumentParser(description="Policy Chat Bot Runner")
    parser.add_argument(
        "command",
        choices=["backend", "frontend", "both", "setup", "check"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_project()
    elif args.command == "check":
        print("🔍 Checking Policy Chat Bot setup...")
        reqs_ok = check_requirements()
        env_ok = check_env_file()
        
        if reqs_ok and env_ok:
            print("\n🎉 Everything looks good! You can start the application.")
        else:
            print("\n❌ Setup issues found. Please fix them before running the application.")
    elif args.command == "backend":
        if not check_requirements() or not check_env_file():
            return
        run_backend()
    elif args.command == "frontend":
        if not check_requirements() or not check_env_file():
            return
        run_frontend()
    elif args.command == "both":
        if not check_requirements() or not check_env_file():
            return
        run_both()

if __name__ == "__main__":
    main()
