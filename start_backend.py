#!/usr/bin/env python3
"""
Start the backend with proper environment variables
"""

import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set environment variables with defaults
os.environ["CHROMA_DB_PATH"] = os.getenv("CHROMA_DB_PATH", "./chroma_db")
os.environ["UPLOAD_DIRECTORY"] = os.getenv("UPLOAD_DIRECTORY", "./uploads")

if __name__ == "__main__":
    print("Starting Policy Chat Bot Backend...")
    print("API will be available at: http://localhost:8001")
    print("API docs at: http://localhost:8001/docs")
    print()
    
    # Import and run the FastAPI app
    from main import app
    uvicorn.run(app, host="0.0.0.0", port=8001)
