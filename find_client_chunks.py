#!/usr/bin/env python3
"""
Find all chunks that contain "Taking business clients out"
"""

import os
from vector_store import VectorStoreManager

def find_client_chunks():
    # Set up environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize vector store
    vector_store = VectorStoreManager()
    
    # Search for "Taking business clients out" specifically
    query = "Taking business clients out"
    results = vector_store.similarity_search(query, k=20)  # Get more results
    
    print(f"Searching for: '{query}'")
    print(f"Found {len(results)} results:")
    print()
    
    found_client_chunk = False
    for i, doc in enumerate(results, 1):
        content = doc.page_content
        if "Taking business clients out" in content:
            print(f"*** FOUND THE CLIENT MEETING CHUNK! ***")
            print(f"Chunk {i}: {doc.metadata.get('chunk_index', 'unknown')}")
            print(f"File: {doc.metadata.get('reference_file', 'unknown')}")
            print(f"Content: {content}")
            print("-" * 60)
            found_client_chunk = True
        elif "client" in content.lower() and "Budgets & Reimbursements.pdf" in doc.metadata.get("reference_file", ""):
            print(f"Chunk {i}: {doc.metadata.get('chunk_index', 'unknown')} - Contains 'client'")
            print(f"Content: {content[:100]}...")
            print()
    
    if not found_client_chunk:
        print("*** CLIENT MEETING CHUNK NOT FOUND IN TOP 20 RESULTS ***")
        print("This suggests the embedding similarity is not matching well.")
        print()
        print("Let me search for all chunks from Budgets & Reimbursements.pdf...")
        
        # Get all chunks from the document
        all_results = vector_store.similarity_search("budgets reimbursements", k=50)
        budget_chunks = [doc for doc in all_results if "Budgets & Reimbursements.pdf" in doc.metadata.get("reference_file", "")]
        
        print(f"Found {len(budget_chunks)} chunks from Budgets & Reimbursements.pdf:")
        for i, doc in enumerate(budget_chunks, 1):
            content = doc.page_content
            if "Taking business clients out" in content:
                print(f"*** FOUND IT! Chunk {i} (Index: {doc.metadata.get('chunk_index', 'unknown')}) ***")
                print(f"Content: {content}")
                print("-" * 60)
            elif "client" in content.lower():
                print(f"Chunk {i} (Index: {doc.metadata.get('chunk_index', 'unknown')}) - Contains 'client'")
                print(f"Content: {content[:150]}...")
                print()

if __name__ == "__main__":
    find_client_chunks()
