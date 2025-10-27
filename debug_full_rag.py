#!/usr/bin/env python3
"""
Debug the full RAG pipeline
"""

import os

# Set environment variables
os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
os.environ["CHROMA_DB_PATH"] = "./chroma_db"
os.environ["UPLOAD_DIRECTORY"] = "./uploads"

from rag_system import RAGSystem

def debug_full_rag():
    """Debug the complete RAG pipeline"""
    
    rag = RAGSystem()
    
    question = "how do i request a salary increase"
    
    print(f"Question: {question}")
    print("=" * 50)
    
    # Test the full pipeline
    response = rag.generate_response(question)
    
    print("Full Response:")
    print(response)
    print("=" * 50)
    
    # Test individual components
    print("\nTesting individual components:")
    
    # 1. Document retrieval
    print("\n1. Document Retrieval:")
    relevant_docs = rag.vector_store.get_relevant_documents_with_sources(question, k=5)
    print(f"Found {len(relevant_docs)} documents")
    
    # 2. Context formatting
    print("\n2. Context Formatting:")
    context = rag.format_context_with_sources(relevant_docs)
    print(f"Context length: {len(context)} characters")
    print(f"Context preview: {context[:500]}...")
    
    # 3. LLM call
    print("\n3. Testing LLM directly:")
    try:
        messages = rag.prompt_template.format_messages(
            context=context,
            question=question
        )
        
        print(f"Number of messages: {len(messages)}")
        print(f"System message: {messages[0].content[:200]}...")
        print(f"Human message length: {len(messages[1].content)}")
        print(f"Human message content: {messages[1].content}")
        
        # Test LLM response
        llm_response = rag.llm(messages)
        print(f"LLM Response: {llm_response.content}")
        
    except Exception as e:
        print(f"LLM Error: {e}")

if __name__ == "__main__":
    debug_full_rag()
