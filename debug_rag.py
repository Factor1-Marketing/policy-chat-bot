#!/usr/bin/env python3
"""
Debug the RAG system
"""

import os

# Set environment variables
os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
os.environ["CHROMA_DB_PATH"] = "./chroma_db"
os.environ["UPLOAD_DIRECTORY"] = "./uploads"

from vector_store import VectorStoreManager

def debug_search():
    """Debug the search functionality"""
    
    vector_store = VectorStoreManager()
    
    query = "what do i have to do to request a salary increase"
    
    print(f"Searching for: {query}")
    print()
    
    # Get relevant documents
    results = vector_store.get_relevant_documents_with_sources(query, k=5)
    
    print(f"Found {len(results)} results:")
    print()
    
    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"  Content: {result['content'][:200]}...")
        print(f"  Score: {result['similarity_score']}")
        print(f"  Source: {result['source_info']['file_name']}")
        print(f"  Section: {result['source_info']['section_headers']}")
        print()

if __name__ == "__main__":
    debug_search()
