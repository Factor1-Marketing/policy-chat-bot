#!/usr/bin/env python3
"""
Test the direct search for client meeting policy
"""

import os
from rag_system import RAGSystem

def test_direct_search():
    # Set up environment
    os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
    
    # Initialize RAG system
    rag = RAGSystem()
    
    # Test the direct search for "taking business clients out"
    print("Testing direct search for 'taking business clients out'...")
    client_results = rag.vector_store.get_relevant_documents_with_sources("taking business clients out", k=5)
    
    print(f"Found {len(client_results)} results:")
    for i, doc in enumerate(client_results, 1):
        content = doc["content"]
        score = doc["similarity_score"]
        print(f"\nResult {i} (Score: {score:.3f}):")
        print(f"Content: {content[:200]}...")
        if "Taking business clients out" in content:
            print("*** FOUND THE CLIENT MEETING POLICY! ***")
            print(f"Full content: {content}")
    
    print("\n" + "="*60)
    print("Testing the improved search_documents method...")
    
    # Test the improved search method
    query = "how do i ask for a reimbursement for a meeting i conducted in a cafe with a client"
    results = rag.search_documents(query, k=10)
    
    print(f"Found {len(results)} results:")
    for i, doc in enumerate(results, 1):
        content = doc["content"]
        score = doc["similarity_score"]
        file_name = doc["source_info"]["file_name"]
        print(f"\nResult {i}: {file_name} (Score: {score:.3f})")
        if "Taking business clients out" in content:
            print("*** FOUND THE CLIENT MEETING POLICY! ***")
            print(f"Content: {content}")
        else:
            print(f"Content: {content[:100]}...")

if __name__ == "__main__":
    test_direct_search()
