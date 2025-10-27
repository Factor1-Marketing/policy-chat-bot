#!/usr/bin/env python3
"""
Test the improved RAG system with the reimbursement question
"""

import os
from rag_system import RAGSystem

def test_improved_rag():
    # Set up environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize RAG system
    rag = RAGSystem()
    
    # Test query
    question = "how do i ask for a reimbursement for a meeting i conducted in a cafe with a client"
    
    print("=" * 80)
    print("TESTING IMPROVED RAG SYSTEM")
    print("=" * 80)
    print(f"Question: {question}")
    print()
    
    # Get response
    result = rag.generate_response(question)
    
    print("RESPONSE:")
    print("-" * 40)
    print(result.get("answer", "No answer generated"))
    print()
    
    print("SOURCES:")
    print("-" * 40)
    sources = result.get("sources", [])
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source.get('file_name', 'Unknown')} (Score: {source.get('relevance_score', 0):.3f})")
        if "Taking business clients out" in source.get("full_content", ""):
            print(f"   *** FOUND CLIENT MEETING POLICY! ***")
        print()

if __name__ == "__main__":
    test_improved_rag()
