#!/usr/bin/env python3
"""
Debug script to see all chunks from a specific document
"""

import os
from vector_store import VectorStoreManager
from config import Config
from dotenv import load_dotenv

def debug_document():
    # Set up environment
    load_dotenv()
    
    # Initialize vector store
    vector_store = VectorStoreManager()
    
    # Search for all chunks from Budgets & Reimbursements.pdf
    query = "Budgets Reimbursements"
    results = vector_store.similarity_search(query, k=20)  # Get more results
    
    print("=" * 80)
    print("ALL CHUNKS FROM BUDGETS & REIMBURSEMENTS.PDF")
    print("=" * 80)
    
    budget_chunks = []
    for doc in results:
        if "Budgets & Reimbursements.pdf" in doc.metadata.get("reference_file", ""):
            budget_chunks.append(doc)
    
    print(f"Found {len(budget_chunks)} chunks from Budgets & Reimbursements.pdf:")
    print()
    
    for i, doc in enumerate(budget_chunks, 1):
        chunk_index = doc.metadata.get("chunk_index", "unknown")
        content = doc.page_content
        print(f"--- CHUNK {i} (Index: {chunk_index}) ---")
        print(f"Content ({len(content)} chars):")
        print(content)
        print("-" * 60)
        print()

if __name__ == "__main__":
    debug_document()
