#!/usr/bin/env python3
"""
Manual SharePoint document setup - no Azure registration required
"""

import os
import shutil
from pathlib import Path
import zipfile

def setup_manual_sharepoint():
    """Instructions for manual SharePoint document setup"""
    
    print("📋 Manual SharePoint Document Setup")
    print("=" * 50)
    print()
    print("Step 1: Download Documents from SharePoint")
    print("- Go to your SharePoint policy folder")
    print("- Select all documents (Ctrl+A)")
    print("- Click 'Download' to get a ZIP file")
    print("- Extract the ZIP to a temporary folder")
    print()
    print("Step 2: Copy to Uploads Folder")
    print("- Copy all extracted documents to: uploads/")
    print("- Supported formats: PDF, DOCX, TXT, MD")
    print()
    print("Step 3: Process Documents")
    print("- Run: python process_all_documents.py")
    print("- This will vectorize all documents")
    print()
    print("Step 4: Deploy to Production")
    print("- Push to GitHub")
    print("- Deploy to Vercel")
    print("- Upload documents via web interface")
    print()
    print("Step 5: Update Process (When Documents Change)")
    print("- Download updated documents from SharePoint")
    print("- Upload new versions via web interface")
    print("- System will update automatically")
    print()

def extract_sharepoint_zip(zip_path: str, extract_to: str = "uploads"):
    """Extract SharePoint download ZIP to uploads folder"""
    
    if not os.path.exists(zip_path):
        print(f"❌ ZIP file not found: {zip_path}")
        return False
    
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs(extract_to, exist_ok=True)
        
        # Extract ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        print(f"✅ Extracted SharePoint documents to {extract_to}/")
        
        # Count extracted files
        extracted_files = list(Path(extract_to).glob("*"))
        supported_extensions = ['.pdf', '.docx', '.txt', '.md']
        
        supported_files = [
            f for f in extracted_files 
            if f.suffix.lower() in supported_extensions
        ]
        
        print(f"📁 Found {len(supported_files)} supported documents:")
        for file in supported_files:
            print(f"  - {file.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error extracting ZIP: {str(e)}")
        return False

def organize_sharepoint_documents(uploads_dir: str = "uploads"):
    """Organize extracted SharePoint documents"""
    
    uploads_path = Path(uploads_dir)
    if not uploads_path.exists():
        print(f"❌ Uploads directory not found: {uploads_dir}")
        return
    
    # Find all documents
    all_files = list(uploads_path.rglob("*"))
    supported_extensions = ['.pdf', '.docx', '.txt', '.md']
    
    documents = [f for f in all_files if f.is_file() and f.suffix.lower() in supported_extensions]
    
    print(f"📁 Found {len(documents)} documents to organize")
    
    # Move documents to root of uploads directory (flatten structure)
    moved_count = 0
    for doc in documents:
        if doc.parent != uploads_path:
            # Move to uploads root
            new_path = uploads_path / doc.name
            
            # Handle name conflicts
            counter = 1
            while new_path.exists():
                name_parts = doc.stem, counter, doc.suffix
                new_path = uploads_path / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                counter += 1
            
            shutil.move(str(doc), str(new_path))
            moved_count += 1
            print(f"📄 Moved: {doc.name}")
    
    print(f"✅ Organized {moved_count} documents")
    
    # Clean up empty directories
    for dir_path in uploads_path.rglob("*"):
        if dir_path.is_dir() and dir_path != uploads_path:
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"🗑️ Removed empty directory: {dir_path.name}")
            except:
                pass

if __name__ == "__main__":
    print("SharePoint Manual Setup Tool")
    print("=" * 30)
    print()
    print("Choose an option:")
    print("1. Show setup instructions")
    print("2. Extract SharePoint ZIP file")
    print("3. Organize extracted documents")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        setup_manual_sharepoint()
    elif choice == "2":
        zip_path = input("Enter path to SharePoint ZIP file: ").strip()
        extract_sharepoint_zip(zip_path)
    elif choice == "3":
        organize_sharepoint_documents()
    else:
        print("Invalid choice")



