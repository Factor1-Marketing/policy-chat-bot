#!/usr/bin/env python3
"""
Test searching specifically for client meeting content
"""

import os
from vector_store import VectorStoreManager

def test_client_search():
    # Set up environment
    os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
    
    # Initialize vector store
    vector_store = VectorStoreManager()
    
    # Test different search queries
    queries = [
        "client meeting reimbursement cafe",
        "taking business clients out",
        "client budget manager",
        "business client expense",
        "client gift budget"
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"SEARCHING FOR: '{query}'")
        print('='*60)
        
        results = vector_store.similarity_search(query, k=5)
        
        for i, doc in enumerate(results, 1):
            if "Budgets & Reimbursements.pdf" in doc.metadata.get("reference_file", ""):
                content = doc.page_content
                if "client" in content.lower():
                    print(f"\n*** FOUND CLIENT-RELATED CONTENT ***")
                    print(f"Chunk {i}: {doc.metadata.get('chunk_index', 'unknown')}")
                    print(f"Content: {content[:200]}...")
                    print(f"Full content: {content}")
                    break
        else:
            print("No client-related content found in top 5 results")

if __name__ == "__main__":
    test_client_search()
