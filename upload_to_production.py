#!/usr/bin/env python3
"""
Upload documents to production API
"""

import requests
import os
from pathlib import Path

def upload_documents_to_production():
    """Upload all documents from uploads folder to production"""
    
    # Production API URL (replace with your actual Vercel URL)
    PRODUCTION_API_URL = "https://your-app.vercel.app/api"
    
    uploads_dir = Path("uploads")
    if not uploads_dir.exists():
        print("❌ Uploads directory not found")
        return
    
    supported_extensions = ['.pdf', '.txt', '.md', '.docx']
    files_to_upload = []
    
    for file_path in uploads_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            files_to_upload.append(file_path)
    
    print(f"📁 Found {len(files_to_upload)} files to upload")
    
    for file_path in files_to_upload:
        try:
            print(f"🔄 Uploading: {file_path.name}")
            
            with open(file_path, 'rb') as file:
                files = {'file': (file_path.name, file, 'application/octet-stream')}
                response = requests.post(f"{PRODUCTION_API_URL}/upload", files=files)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {result['chunks_created']} chunks created")
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error uploading {file_path.name}: {str(e)}")

if __name__ == "__main__":
    upload_documents_to_production()



