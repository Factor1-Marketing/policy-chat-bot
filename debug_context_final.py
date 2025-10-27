#!/usr/bin/env python3
"""
Debug the final context sent to the LLM
"""

import os
from rag_system import RAGSystem

def debug_final_context():
    # Set up environment
    os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
    
    # Initialize RAG system
    rag = RAGSystem()
    
    query = "how do i ask for a reimbursement for a meeting i conducted in a cafe with a client"
    
    print("Getting relevant documents...")
    relevant_docs = rag.search_documents(query, k=10)
    
    print(f"Found {len(relevant_docs)} relevant documents")
    
    # Check if client meeting chunk is in the results
    client_meeting_found = False
    for i, doc in enumerate(relevant_docs, 1):
        if "Taking business clients out" in doc["content"]:
            print(f"*** CLIENT MEETING CHUNK FOUND at position {i} ***")
            print(f"Score: {doc['similarity_score']}")
            print(f"Content: {doc['content']}")
            client_meeting_found = True
            break
    
    if not client_meeting_found:
        print("*** CLIENT MEETING CHUNK NOT FOUND ***")
        return
    
    print("\n" + "="*80)
    print("FORMATTED CONTEXT SENT TO LLM:")
    print("="*80)
    
    # Format context with sources
    context = rag.format_context_with_sources(relevant_docs)
    print(context)
    
    print("\n" + "="*80)
    print("CHECKING IF CLIENT MEETING POLICY IS IN CONTEXT:")
    print("="*80)
    
    if "Taking business clients out" in context:
        print("*** CLIENT MEETING POLICY IS IN THE CONTEXT ***")
        # Find the specific line
        lines = context.split('\n')
        for i, line in enumerate(lines, 1):
            if "Taking business clients out" in line:
                print(f"Found at line {i}: {line}")
                # Show surrounding context
                start = max(0, i-3)
                end = min(len(lines), i+4)
                print("\nSurrounding context:")
                for j in range(start, end):
                    marker = ">>> " if j == i-1 else "    "
                    print(f"{marker}{lines[j]}")
                break
    else:
        print("*** CLIENT MEETING POLICY NOT FOUND IN CONTEXT ***")

if __name__ == "__main__":
    debug_final_context()
