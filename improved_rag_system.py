#!/usr/bin/env python3
"""
Improved RAG system with better document retrieval
"""

import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from vector_store import VectorStoreManager

class ImprovedRAGSystem:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vector_store = VectorStoreManager()
    
    def search_documents_improved(self, query: str, k: int = 15) -> List[Dict[str, Any]]:
        """Improved document search with multiple strategies"""
        
        # Strategy 1: Original semantic search
        semantic_results = self.vector_store.get_relevant_documents_with_sources(query, k=k)
        
        # Strategy 2: Keyword-based search for specific terms
        keyword_queries = self._extract_keywords(query)
        keyword_results = []
        
        for keyword_query in keyword_queries:
            results = self.vector_store.get_relevant_documents_with_sources(keyword_query, k=10)
            keyword_results.extend(results)
        
        # Strategy 3: Search for specific document types
        doc_type_queries = self._get_doc_type_queries(query)
        doc_type_results = []
        
        for doc_query in doc_type_queries:
            results = self.vector_store.get_relevant_documents_with_sources(doc_query, k=5)
            doc_type_results.extend(results)
        
        # Combine and deduplicate results
        all_results = semantic_results + keyword_results + doc_type_results
        
        # Remove duplicates based on content
        seen_content = set()
        unique_results = []
        
        for result in all_results:
            content = result["content"]
            if content not in seen_content:
                seen_content.add(content)
                unique_results.append(result)
        
        # Sort by relevance score and return top k
        unique_results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return unique_results[:k]
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from the query"""
        keywords = []
        query_lower = query.lower()
        
        # Client meeting related keywords
        if any(word in query_lower for word in ["client", "meeting", "cafe", "restaurant"]):
            keywords.extend([
                "taking business clients out",
                "client budget",
                "business client expense",
                "client meeting",
                "managers only client"
            ])
        
        # Reimbursement related keywords
        if any(word in query_lower for word in ["reimbursement", "reimburse", "expense"]):
            keywords.extend([
                "reimbursement policy",
                "expense approval",
                "budget allowance",
                "receipt required"
            ])
        
        return keywords
    
    def _get_doc_type_queries(self, query: str) -> List[str]:
        """Get document type specific queries"""
        doc_queries = []
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["reimbursement", "expense", "budget"]):
            doc_queries.extend([
                "budgets reimbursements policy",
                "expense approval process",
                "budget allowance"
            ])
        
        if any(word in query_lower for word in ["client", "meeting"]):
            doc_queries.extend([
                "client policy",
                "business client",
                "client referral"
            ])
        
        return doc_queries
    
    def generate_response_improved(self, question: str) -> Dict[str, Any]:
        """Generate response with improved document retrieval"""
        try:
            # Get relevant documents with improved search
            relevant_docs = self.search_documents_improved(question, k=15)
            
            if not relevant_docs:
                return {
                    "answer": "I couldn't find any relevant information in the policy documents to answer your question.",
                    "sources": []
                }
            
            # Format context with sources
            context = self.format_context_with_sources(relevant_docs)
            
            # Create messages for the LLM
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
            
            Please provide a comprehensive answer based on the context above, including proper citations to the source documents.""")
            ]
            
            # Generate response
            response = self.llm.invoke(messages)
            answer = response.content
            
            # Extract sources for response
            sources = []
            for doc_info in relevant_docs:
                source_info = doc_info["source_info"]
                content = doc_info["content"]
                
                # Create a preview
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

# Test the improved system
if __name__ == "__main__":
    import os
    os.environ["OPENAI_API_KEY"] = "LOAD_FROM_ENV"
    
    rag = ImprovedRAGSystem()
    question = "how do i ask for a reimbursement for a meeting i conducted in a cafe with a client"
    
    print("=" * 80)
    print("TESTING IMPROVED RAG SYSTEM")
    print("=" * 80)
    print(f"Question: {question}")
    print()
    
    result = rag.generate_response_improved(question)
    
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
