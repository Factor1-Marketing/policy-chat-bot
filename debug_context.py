#!/usr/bin/env python3
"""
Debug script to see what context is being passed to the LLM
"""

import os
from rag_system import RAGSystem
from config import Config

def debug_context():
    # Set up environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize RAG system
    rag = RAGSystem()
    
    # Test query
    question = "how do i ask for a reimbursement for a meeting i conducted in a cafe with a client"
    
    print("=" * 80)
    print("DEBUGGING RAG CONTEXT")
    print("=" * 80)
    print(f"Question: {question}")
    print()
    
    # Get relevant documents
    relevant_docs = rag.search_documents(question, k=5)
    
    print(f"Found {len(relevant_docs)} relevant documents:")
    print()
    
    for i, doc in enumerate(relevant_docs, 1):
        source_info = doc["source_info"]
        content = doc["content"]
        score = doc["similarity_score"]
        
        print(f"--- DOCUMENT {i} ---")
        print(f"File: {source_info['file_name']}")
        print(f"Score: {score:.3f}")
        print(f"Content ({len(content)} chars):")
        print(content[:500] + "..." if len(content) > 500 else content)
        print()
    
    # Generate context
    context = rag.format_context_with_sources(relevant_docs)
    
    print("=" * 80)
    print("FORMATTED CONTEXT SENT TO LLM:")
    print("=" * 80)
    print(context)
    print("=" * 80)

if __name__ == "__main__":
    debug_context()
