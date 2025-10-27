#!/usr/bin/env python3
"""
Start the frontend with proper environment variables
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    print("Starting Policy Chat Bot Frontend...")
    print("Web interface will be available at: http://localhost:8501")
    print()
    
    # Run streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "chat_interface.py", "--server.port=8501", "--server.address=0.0.0.0"])
