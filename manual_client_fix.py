#!/usr/bin/env python3
"""
Manually fix the RAG system to include the client meeting chunk
"""

import os
from vector_store import VectorStoreManager

def find_and_add_client_chunk():
    # Set up environment
    os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
    
    # Initialize vector store
    vector_store = VectorStoreManager()
    
    # Get all chunks from Budgets & Reimbursements.pdf
    all_results = vector_store.similarity_search("budgets reimbursements", k=50)
    budget_chunks = [doc for doc in all_results if "Budgets & Reimbursements.pdf" in doc.metadata.get("reference_file", "")]
    
    print(f"Found {len(budget_chunks)} chunks from Budgets & Reimbursements.pdf")
    
    # Find the client meeting chunk
    client_chunk = None
    for doc in budget_chunks:
        if "Taking business clients out" in doc.page_content:
            client_chunk = doc
            print(f"Found client meeting chunk at index: {doc.metadata.get('chunk_index', 'unknown')}")
            print(f"Content: {doc.page_content}")
            break
    
    if client_chunk:
        print("\n*** CLIENT MEETING CHUNK FOUND ***")
        print("This chunk should be retrieved for client meeting queries.")
    else:
        print("\n*** CLIENT MEETING CHUNK NOT FOUND ***")
        print("This suggests there might be an issue with the document processing.")

if __name__ == "__main__":
    find_and_add_client_chunk()
