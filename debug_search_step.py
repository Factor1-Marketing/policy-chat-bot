#!/usr/bin/env python3
"""
Debug the search step by step
"""

import os
from rag_system import RAGSystem

def debug_search_step():
    # Set up environment
    os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
    
    # Initialize RAG system
    rag = RAGSystem()
    
    query = "how do i ask for a reimbursement for a meeting i conducted in a cafe with a client"
    
    print("Step 1: Check if query contains client keywords...")
    client_keywords = ["client", "meeting", "cafe", "restaurant"]
    has_client_keywords = any(word in query.lower() for word in client_keywords)
    print(f"Query contains client keywords: {has_client_keywords}")
    print(f"Keywords found: {[word for word in client_keywords if word in query.lower()]}")
    
    if has_client_keywords:
        print("\nStep 2: Getting all chunks from Budgets & Reimbursements.pdf...")
        all_results = rag.vector_store.similarity_search("budgets reimbursements", k=50)
        budget_chunks = [doc for doc in all_results if "Budgets & Reimbursements.pdf" in doc.metadata.get("reference_file", "")]
        print(f"Found {len(budget_chunks)} chunks from Budgets & Reimbursements.pdf")
        
        print("\nStep 3: Looking for client meeting chunk...")
        client_chunk_found = False
        for i, doc in enumerate(budget_chunks, 1):
            if "Taking business clients out" in doc.page_content:
                print(f"*** FOUND CLIENT MEETING CHUNK at position {i} ***")
                print(f"Chunk index: {doc.metadata.get('chunk_index', 'unknown')}")
                print(f"Content: {doc.page_content}")
                client_chunk_found = True
                break
        
        if not client_chunk_found:
            print("*** CLIENT MEETING CHUNK NOT FOUND ***")
            print("This suggests the chunk might not exist or the search is not working.")
    
    print("\nStep 4: Testing the search_documents method...")
    results = rag.search_documents(query, k=10)
    print(f"search_documents returned {len(results)} results")
    
    client_meeting_found = False
    for i, doc in enumerate(results, 1):
        if "Taking business clients out" in doc["content"]:
            print(f"*** CLIENT MEETING CHUNK FOUND in results at position {i} ***")
            print(f"Score: {doc['similarity_score']}")
            client_meeting_found = True
            break
    
    if not client_meeting_found:
        print("*** CLIENT MEETING CHUNK NOT FOUND in search results ***")
        print("Top 5 results:")
        for i, doc in enumerate(results[:5], 1):
            print(f"{i}. {doc['source_info']['file_name']} (Score: {doc['similarity_score']:.3f})")

if __name__ == "__main__":
    debug_search_step()
