#!/usr/bin/env python3
"""
Test the enhanced source display functionality
"""

import os

# Set environment variables
os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
os.environ["CHROMA_DB_PATH"] = "./chroma_db"
os.environ["UPLOAD_DIRECTORY"] = "./uploads"

from rag_system import RAGSystem

def test_enhanced_sources():
    """Test the enhanced source functionality"""
    
    rag = RAGSystem()
    
    question = "how do i request a salary increase"
    
    print(f"Testing enhanced sources for question: {question}")
    print("=" * 60)
    
    # Get response with enhanced sources
    response = rag.generate_response(question)
    
    print("Answer:")
    print(response['answer'][:200] + "...")
    print("\n" + "=" * 60)
    
    print("Enhanced Sources:")
    for i, source in enumerate(response['sources'], 1):
        print(f"\n{i}. {source['file_name']}")
        print(f"   Relevance: {source['relevance_score']:.3f}")
        print(f"   Chunk: {source['chunk_index']}")
        print(f"   Preview: {source['preview'][:100]}...")
        print(f"   Full content length: {len(source['full_content'])} characters")
        print(f"   File path: {source['file_path']}")

if __name__ == "__main__":
    test_enhanced_sources()
