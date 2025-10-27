#!/usr/bin/env python3
"""
Process all documents in the uploads folder
"""

import os
import sys
from pathlib import Path

# Set environment variables directly
os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
os.environ["CHROMA_DB_PATH"] = "./chroma_db"
os.environ["UPLOAD_DIRECTORY"] = "./uploads"

# Now import our modules
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager

def process_all_documents():
    """Process all documents in the uploads folder"""
    
    print("Policy Document Processor")
    print("Processing all documents from uploads folder...")
    print()
    
    # Initialize components
    processor = DocumentProcessor()
    vector_store = VectorStoreManager()
    
    # Check if uploads folder exists
    uploads_folder = Path("uploads")
    if not uploads_folder.exists():
        print("ERROR: uploads folder not found")
        return
    
    # Supported file types
    supported_extensions = ['.pdf', '.txt', '.md', '.docx']
    
    # Find all supported files
    files_to_process = []
    for file_path in uploads_folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            files_to_process.append(file_path)
    
    if not files_to_process:
        print("ERROR: No supported documents found in uploads folder")
        print(f"Supported formats: {', '.join(supported_extensions)}")
        return
    
    print(f"Found {len(files_to_process)} documents to process:")
    for file_path in files_to_process:
        print(f"  - {file_path.name}")
    
    print("\nStarting processing...")
    
    successful = 0
    failed = 0
    total_chunks = 0
    
    for file_path in files_to_process:
        try:
            print(f"\nProcessing: {file_path.name}")
            
            # Process the document
            documents = processor.process_document(str(file_path))
            
            # Add to vector store
            if vector_store.add_documents(documents):
                chunks_created = len(documents)
                total_chunks += chunks_created
                successful += 1
                print(f"SUCCESS: Created {chunks_created} chunks")
            else:
                failed += 1
                print(f"ERROR: Failed to add to vector store")
                
        except Exception as e:
            failed += 1
            print(f"ERROR: {str(e)}")
    
    print(f"\nProcessing Summary:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total chunks created: {total_chunks}")
    
    if successful > 0:
        print("\nAll documents are now ready for the chatbot!")
        print("You can now start the application with: python run.py both")
        
        # Show collection stats
        stats = vector_store.get_collection_stats()
        print(f"\nVector store contains:")
        print(f"  - {stats['total_documents']} total chunks")
        print(f"  - {stats['unique_files']} unique files")

if __name__ == "__main__":
    process_all_documents()
