#!/usr/bin/env python3
"""
Quick setup script for Policy Chat Bot
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 Setting up Policy Chat Bot...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Install requirements
    print("📦 Installing requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Create directories
    print("📁 Creating directories...")
    directories = ["uploads", "chroma_db"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# OpenAI API Key - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Database and file paths
CHROMA_DB_PATH=./chroma_db
UPLOAD_DIRECTORY=./uploads

# File processing settings
MAX_FILE_SIZE=10485760
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
"""
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("⚠️  Please add your OpenAI API key to the .env file")
    else:
        print("✅ .env file already exists")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Add your OpenAI API key to the .env file")
    print("2. Start the backend: python run.py backend")
    print("3. Start the frontend: python run.py frontend")
    print("4. Or run both: python run.py both")
    print("\n📚 Read README.md for detailed instructions")

if __name__ == "__main__":
    main()
