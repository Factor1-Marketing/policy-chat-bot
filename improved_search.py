#!/usr/bin/env python3
"""
Improved search with reranking for better precision
"""

import os
from rag_system import RAGSystem
from typing import List, Dict, Any
import re

class Reranker:
    """Rerank search results based on keyword matching and relevance"""
    
    @staticmethod
    def rerank_results(query: str, results: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """Rerank results by boosting chunks that contain query keywords"""
        
        query_keywords = set(query.lower().split())
        
        for result in results:
            content_lower = result["content"].lower()
            
            # Count keyword matches in content
            keyword_matches = sum(1 for keyword in query_keywords if keyword in content_lower)
            
            # Boost score if keywords are found
            if keyword_matches > 0:
                result["similarity_score"] += (keyword_matches / len(query_keywords)) * 0.2
        
        # Sort by boosted score
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return results[:top_k]

class ImprovedSearchRAG:
    def __init__(self, rag_system: RAGSystem):
        self.rag = rag_system
        self.reranker = Reranker()
    
    def generate_response(self, question: str) -> Dict[str, Any]:
        """Generate response with improved retrieval"""
        
        # Step 1: Get initial results
        initial_results = self.rag.search_documents(question, k=20)  # Get more results
        
        # Step 2: Rerank by keyword relevance
        reranked_results = self.reranker.rerank_results(question, initial_results, top_k=10)
        
        # Step 3: Generate response with reranked results
        try:
            if not reranked_results:
                return {
                    "answer": "I couldn't find relevant information in the policy documents.",
                    "sources": []
                }
            
            # Format context
            context = self.rag.format_context_with_sources(reranked_results)
            
            # Create messages
            from langchain_core.messages import SystemMessage, HumanMessage
            messages = [
                SystemMessage(content="""You are a helpful assistant that answers questions based on policy documents. 
            Use the provided context to answer questions accurately and cite specific sources.
            
            Guidelines:
            1. Carefully read ALL the provided context - it contains relevant policy information
            2. Look for specific policies, procedures, amounts, and approval requirements
            3. Always cite the source document and section when possible
            4. Be specific about amounts, approval processes, and requirements
            5. If multiple sources are relevant, mention all of them
            6. If you find relevant information in the context, use it to provide a comprehensive answer
            
            Format your response with clear citations using the reference information provided."""),
                HumanMessage(content=f"""Context from policy documents:
            {context}
            
            Question: {question}
            
            IMPORTANT: Look carefully at the context above. If you find specific policies that directly relate to the question, use those policies to provide a detailed answer. Pay special attention to any budget amounts, approval requirements, and specific procedures mentioned in the context.
            
            Please provide a comprehensive answer based on the context above, including proper citations to the source documents.""")
            ]
            
            # Generate response
            response = self.rag.llm.invoke(messages)
            answer = response.content
            
            # Extract sources
            sources = []
            for doc_info in reranked_results:
                source_info = doc_info["source_info"]
                content = doc_info["content"]
                
                preview = content[:300]
                if len(content) > 300:
                    last_period = preview.rfind('.')
                    if last_period > 200:
                        preview = preview[:last_period + 1]
                    else:
                        preview += "..."
                
                sources.append({
                    "file_name": source_info["file_name"],
                    "file_path": source_info["file_path"],
                    "section_headers": source_info["section_headers"],
                    "chunk_index": source_info["chunk_index"],
                    "relevance_score": doc_info["similarity_score"],
                    "preview": preview,
                    "full_content": content
                })
            
            return {
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            return {"error": str(e)}

# Test the improved search
if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
    
    rag = RAGSystem()
    improved = ImprovedSearchRAG(rag)
    
    question = "how do i ask for a reimbursement for a meeting i conducted in a cafe with a client"
    
    result = improved.generate_response(question)
    
    print("=" * 80)
    print("IMPROVED RAG RESPONSE")
    print("=" * 80)
    print(result.get("answer", "No answer"))
    print("\nSOURCES:")
    for i, source in enumerate(result.get("sources", [])[:5], 1):
        print(f"{i}. {source['file_name']} (Score: {source['relevance_score']:.3f})")
        if "Taking business clients out" in source.get("full_content", ""):
            print("   *** FOUND CLIENT MEETING POLICY! ***")
