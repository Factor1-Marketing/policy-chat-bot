#!/usr/bin/env python3
"""
Bulk upload script for policy documents
"""

import os
import requests
from pathlib import Path
import time

API_BASE_URL = "http://localhost:8000"

def upload_document(file_path):
    """Upload a single document"""
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (file_path.name, file, 'application/octet-stream')}
            response = requests.post(f"{API_BASE_URL}/upload", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS {file_path.name}: {result['chunks_created']} chunks created")
            return True
        else:
            print(f"ERROR {file_path.name}: {response.text}")
            return False
    except Exception as e:
        print(f"ERROR {file_path.name}: {str(e)}")
        return False

def bulk_upload(documents_folder="uploads"):
    """Upload all documents from a folder"""
    if not os.path.exists(documents_folder):
        print(f"ERROR: Folder '{documents_folder}' not found")
        return
    
    # Supported file types
    supported_extensions = ['.pdf', '.txt', '.md', '.docx']
    
    # Find all supported files
    files_to_upload = []
    for file_path in Path(documents_folder).iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            files_to_upload.append(file_path)
    
    if not files_to_upload:
        print(f"ERROR: No supported documents found in '{documents_folder}'")
        print(f"Supported formats: {', '.join(supported_extensions)}")
        return
    
    print(f"Found {len(files_to_upload)} documents to upload:")
    for file_path in files_to_upload:
        print(f"  - {file_path.name}")
    
    print("\nStarting upload process...")
    
    successful = 0
    failed = 0
    
    for file_path in files_to_upload:
        if upload_document(file_path):
            successful += 1
        else:
            failed += 1
        time.sleep(1)  # Small delay between uploads
    
    print(f"\nUpload Summary:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(files_to_upload)}")

if __name__ == "__main__":
    print("Policy Document Bulk Upload")
    print("Make sure the backend API is running on http://localhost:8000")
    print()
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("SUCCESS: Backend API is running")
        else:
            print("ERROR: Backend API is not responding properly")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend API")
        print("Please start the backend with: python run.py backend")
        exit(1)
    
    # Upload documents
    bulk_upload()
