#!/usr/bin/env python3
"""
Precision-focused RAG system
"""

import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

class PrecisionRAG:
    """RAG system focused on precision over recall"""
    
    def __init__(self, rag_system):
        self.rag = rag_system
        self.similarity_threshold = 0.4  # Only include high-quality matches
    
    def generate_precise_response(self, question: str) -> Dict[str, Any]:
        """Generate response focusing on precision"""
        
        # Get more results first
        all_results = self.rag.vector_store.get_relevant_documents_with_sources(question, k=20)
        
        # Filter by similarity threshold
        high_quality_results = [
            doc for doc in all_results 
            if doc["similarity_score"] >= self.similarity_threshold
        ]
        
        # If not enough high-quality results, lower threshold slightly
        if len(high_quality_results) < 3:
            self.similarity_threshold = 0.3
            high_quality_results = [
                doc for doc in all_results 
                if doc["similarity_score"] >= self.similarity_threshold
            ]
        
        # Keyword boost
        question_keywords = set(question.lower().split())
        boosted_results = []
        
        for doc in high_quality_results[:15]:  # Top 15 max
            content_lower = doc["content"].lower()
            keyword_matches = sum(1 for keyword in question_keywords if keyword in content_lower)
            
            if keyword_matches > 0:
                doc["similarity_score"] += (keyword_matches / len(question_keywords)) * 0.2
            
            boosted_results.append(doc)
        
        # Sort and take top 5
        boosted_results.sort(key=lambda x: x["similarity_score"], reverse=True)
        final_results = boosted_results[:5]
        
        # Generate response with focused results
        if not final_results:
            return {
                "answer": "I couldn't find relevant information in the policy documents to answer your question.",
                "sources": []
            }
        
        # Format context
        context = self._format_precise_context(final_results)
        
        # Create very focused prompt
        messages = [
            SystemMessage(content="""You are a precise policy assistant. Answer ONLY based on the provided context.
            
Rules:
1. Use ONLY information from the context provided
2. Be specific - quote exact amounts, approval processes, requirements
3. If the exact answer is in the context, provide it
4. If not enough information, say so clearly
5. Never make assumptions beyond what's in the context

Be concise and accurate."""),
            HumanMessage(content=f"""Context:
{context}

Question: {question}

Instructions: Answer the question using ONLY the specific information from the context above. If you find the exact answer, provide it with all details. If not, state clearly that the information is not available.""")
        ]
        
        response = self.rag.llm.invoke(messages)
        
        # Format sources
        sources = []
        for doc in final_results:
            source_info = doc["source_info"]
            content = doc["content"]
            
            sources.append({
                "file_name": source_info["file_name"],
                "relevance_score": doc["similarity_score"],
                "preview": content[:300] + "..." if len(content) > 300 else content,
                "full_content": content
            })
        
        return {
            "answer": response.content,
            "sources": sources
        }
    
    def _format_precise_context(self, results: List[Dict]) -> str:
        """Format context with emphasis on relevance"""
        parts = []
        
        for i, doc in enumerate(results, 1):
            source = doc["source_info"]["file_name"]
            score = doc["similarity_score"]
            content = doc["content"]
            
            parts.append(f"[RELEVANCE {i} ({score:.2f}): {source}]\n{content}\n")
        
        return "\n".join(parts)

# Test
if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
    
    from rag_system import RAGSystem
    rag = RAGSystem()
    precision = PrecisionRAG(rag)
    
    question = "how do i ask for a reimbursement for a meeting i conducted in a cafe with a client"
    result = precision.generate_precise_response(question)
    
    print("=" * 80)
    print("PRECISION RAG RESPONSE")
    print("=" * 80)
    print(result.get("answer"))
    print("\nSOURCES:")
    for i, source in enumerate(result.get("sources", [])[:5], 1):
        print(f"{i}. {source['file_name']} (Score: {source['relevance_score']:.3f})")
        if "Taking business clients out" in source.get("full_content", ""):
            print("   *** CLIENT MEETING POLICY FOUND! ***")
