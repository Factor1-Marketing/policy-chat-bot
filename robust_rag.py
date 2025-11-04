#!/usr/bin/env python3
"""
Robust RAG system with multiple improvements for accuracy
"""

import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from vector_store import VectorStoreManager

class RobustRAG:
    """More robust RAG system with better retrieval accuracy"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vector_store = VectorStoreManager()
        self.similarity_threshold = 0.35  # Minimum similarity score
    
    def search_with_expansion(self, query: str, k: int = 15) -> List[Dict[str, Any]]:
        """Search with query expansion and filtering"""
        
        # Original search
        results = self.vector_store.get_relevant_documents_with_sources(query, k=k * 2)
        
        # Filter by similarity threshold
        filtered_results = [
            doc for doc in results 
            if doc["similarity_score"] >= self.similarity_threshold
        ]
        
        # Apply keyword boost
        query_keywords = set(query.lower().split())
        
        boosted_results = []
        for doc in filtered_results:
            content_lower = doc["content"].lower()
            
            # Count keyword matches
            matches = sum(1 for keyword in query_keywords if keyword in content_lower)
            
            if matches > 0:
                # Boost score for keyword matches
                boost = (matches / len(query_keywords)) * 0.15
                doc["similarity_score"] = min(1.0, doc["similarity_score"] + boost)
            
            boosted_results.append(doc)
        
        # Sort by boosted score
        boosted_results.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        # Return top k
        return boosted_results[:k]
    
    def generate_response(self, question: str, k: int = 10) -> Dict[str, Any]:
        """Generate response with improved retrieval"""
        try:
            # Get relevant documents with improved search
            relevant_docs = self.search_with_expansion(question, k=k)
            
            if not relevant_docs:
                return {
                    "answer": "I couldn't find relevant information in the policy documents to answer your question.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Format context
            context = self.format_context_with_sources(relevant_docs)
            
            # Create messages
            messages = [
                SystemMessage(content="""You are a helpful assistant that answers questions based on policy documents. 
            Your answers must be accurate and based ONLY on the provided context.
            
            Critical Instructions:
            1. Read ALL context carefully before answering
            2. Find the MOST RELEVANT information for the specific question asked
            3. Provide SPECIFIC details (amounts, approval processes, requirements)
            4. If the context contains the answer, provide it with specific details
            5. Cite the exact source document when possible
            6. If you cannot find the answer in the context, clearly state that
            
            Be precise and cite sources accurately."""),
                HumanMessage(content=f"""Context from policy documents:
            {context}
            
            Question: {question}
            
            Instructions: Answer this question using ONLY the information from the context above. If you find relevant information in the context, provide a detailed answer with specific details. If not, clearly state that the information is not available in the provided documents.""")
            ]
            
            # Generate response
            response = self.llm.invoke(messages)
            answer = response.content
            
            # Extract sources
            sources = []
            for doc_info in relevant_docs:
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
            
            # Calculate confidence
            avg_confidence = sum(doc["similarity_score"] for doc in relevant_docs) / len(relevant_docs)
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": avg_confidence,
                "total_sources_found": len(relevant_docs)
            }
            
        except Exception as e:
            return {
                "answer": f"Error generating response: {str(e)}",
                "sources": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def format_context_with_sources(self, relevant_docs: List[Dict[str, Any]]) -> str:
        """Format context with source information"""
        context_parts = []
        
        for i, doc_info in enumerate(relevant_docs, 1):
            source_info = doc_info.get("source_info", {})
            content = doc_info.get("content", "")
            similarity_score = doc_info.get("similarity_score", 0)
            
            file_name = source_info.get("file_name", "Unknown Document")
            section_headers = source_info.get("section_headers", "")
            
            context_part = f"[Source {i}: {file_name}]"
            if section_headers:
                context_part += f" (Section: {section_headers})"
            context_part += f" (Relevance: {similarity_score:.3f})\n{content}\n"
            
            context_parts.append(context_part)
        
        return "\n".join(context_parts)

if __name__ == "__main__":
    # Test
    os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
    
    rag = RobustRAG()
    question = "how do i ask for a reimbursement for a meeting i conducted in a cafe with a client"
    
    result = rag.generate_response(question)
    
    print("=" * 80)
    print("ROBUST RAG RESPONSE")
    print("=" * 80)
    print(result.get("answer", "No answer"))
    print()
    print("SOURCES:")
    for i, source in enumerate(result.get("sources", [])[:5], 1):
        print(f"{i}. {source['file_name']} (Score: {source['relevance_score']:.3f})")
        if "Taking business clients out" in source.get("full_content", ""):
            print("   *** FOUND CLIENT MEETING POLICY! ***")
