#!/usr/bin/env python3
"""
Migrate local ChromaDB data to production ChromaDB service
"""

import os
import json
from pathlib import Path

# Set environment variables for local and production
    from dotenv import load_dotenv
    load_dotenv()
os.environ["CHROMA_DB_PATH"] = "./chroma_db"
os.environ["UPLOAD_DIRECTORY"] = "./uploads"

from vector_store import VectorStoreManager
from vector_store_prod import ProductionVectorStoreManager
from document_processor import DocumentProcessor

def migrate_data():
    """Migrate data from local ChromaDB to production ChromaDB"""
    
    print("🚀 Starting data migration to production...")
    
    # Initialize local and production vector stores
    local_store = VectorStoreManager()
    prod_store = ProductionVectorStoreManager()
    
    # Get all documents from local store
    try:
        local_collection = local_store.chroma_client.get_collection(name="policy_documents")
        local_data = local_collection.get()
        
        print(f"📊 Found {len(local_data['documents'])} documents in local store")
        
        if not local_data['documents']:
            print("❌ No documents found in local store")
            return
        
        # Prepare documents for migration
        documents_to_migrate = []
        for i, (doc_content, metadata, doc_id) in enumerate(zip(
            local_data['documents'],
            local_data['metadatas'],
            local_data['ids']
        )):
            # Create Document object
            from langchain_core.documents import Document
            doc = Document(
                page_content=doc_content,
                metadata=metadata
            )
            documents_to_migrate.append(doc)
        
        print(f"📦 Prepared {len(documents_to_migrate)} documents for migration")
        
        # Migrate to production
        success = prod_store.add_documents(documents_to_migrate)
        
        if success:
            print("✅ Migration completed successfully!")
            
            # Verify migration
            prod_stats = prod_store.get_collection_stats()
            print(f"📈 Production store now has {prod_stats['total_documents']} documents")
            print(f"📁 From {prod_stats['unique_files']} unique files")
        else:
            print("❌ Migration failed")
            
    except Exception as e:
        print(f"❌ Migration error: {str(e)}")

def re_upload_documents():
    """Alternative: Re-process and upload documents from files"""
    
    print("🔄 Re-processing documents from files...")
    
    # Initialize production store
    prod_store = ProductionVectorStoreManager()
    processor = DocumentProcessor()
    
    # Process all files in uploads directory
    uploads_dir = Path("uploads")
    if not uploads_dir.exists():
        print("❌ Uploads directory not found")
        return
    
    supported_extensions = ['.pdf', '.txt', '.md', '.docx']
    files_to_process = []
    
    for file_path in uploads_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            files_to_process.append(file_path)
    
    print(f"📁 Found {len(files_to_process)} files to process")
    
    total_chunks = 0
    for file_path in files_to_process:
        try:
            print(f"🔄 Processing: {file_path.name}")
            documents = processor.process_document(str(file_path))
            
            success = prod_store.add_documents(documents)
            if success:
                total_chunks += len(documents)
                print(f"✅ Added {len(documents)} chunks from {file_path.name}")
            else:
                print(f"❌ Failed to add chunks from {file_path.name}")
                
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")
    
    print(f"🎉 Total chunks migrated: {total_chunks}")

if __name__ == "__main__":
    print("Choose migration method:")
    print("1. Migrate from local ChromaDB (faster)")
    print("2. Re-process from files (more reliable)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        migrate_data()
    elif choice == "2":
        re_upload_documents()
    else:
        print("Invalid choice")



