#!/usr/bin/env python3
"""
Test document processing with direct API key
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

def test_processing():
    """Test processing one document"""
    
    print("Testing document processing...")
    print(f"API Key set: {bool(os.environ.get('OPENAI_API_KEY'))}")
    
    # Initialize components
    processor = DocumentProcessor()
    vector_store = VectorStoreManager()
    
    # Find first PDF file
    uploads_folder = Path("uploads")
    pdf_files = list(uploads_folder.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in uploads folder")
        return
    
    test_file = pdf_files[0]
    print(f"Testing with file: {test_file.name}")
    
    try:
        # Process the document
        documents = processor.process_document(str(test_file))
        print(f"Created {len(documents)} chunks")
        
        # Add to vector store
        success = vector_store.add_documents(documents)
        if success:
            print("SUCCESS: Document processed and added to vector store!")
        else:
            print("ERROR: Failed to add to vector store")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_processing()
