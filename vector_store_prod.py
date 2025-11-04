import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import Config

class ProductionVectorStoreManager:
    def __init__(self):
        self.config = Config()
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.config.OPENAI_API_KEY)
        
        # Production ChromaDB setup
        chroma_host = os.getenv("CHROMA_DB_HOST", "localhost")
        chroma_port = os.getenv("CHROMA_DB_PORT", "8000")
        
        # Initialize ChromaDB HTTP client for production
        self.chroma_client = chromadb.HttpClient(
            host=chroma_host,
            port=int(chroma_port),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Collection name for policy documents
        self.collection_name = "policy_documents"
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize or load existing vectorstore"""
        try:
            # Try to get existing collection
            collection = self.chroma_client.get_collection(name=self.collection_name)
            self.vectorstore = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
            print(f"✅ Loaded existing vectorstore with {collection.count()} documents")
        except Exception:
            # Create new collection if it doesn't exist
            self.vectorstore = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
            print("✅ Created new vectorstore")
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to the vectorstore"""
        try:
            if not documents:
                return False
            
            # Add documents to vectorstore
            self.vectorstore.add_documents(documents)
            print(f"✅ Added {len(documents)} documents to vectorstore")
            return True
        except Exception as e:
            print(f"❌ Error adding documents to vectorstore: {str(e)}")
            return False
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Perform similarity search and return relevant documents"""
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"❌ Error performing similarity search: {str(e)}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Perform similarity search with scores"""
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"❌ Error performing similarity search with score: {str(e)}")
            return []
    
    def get_relevant_documents_with_sources(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Get relevant documents with enhanced source information"""
        try:
            # Get similarity search results with scores
            results = self.similarity_search_with_score(query, k=k)
            
            enhanced_results = []
            for doc, score in results:
                result_info = {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": float(score),
                    "source_info": self._format_source_info(doc.metadata)
                }
                enhanced_results.append(result_info)
            
            return enhanced_results
        except Exception as e:
            print(f"❌ Error getting relevant documents with sources: {str(e)}")
            return []
    
    def _format_source_info(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Format source information for display"""
        reference_file = metadata.get("reference_file", metadata.get("filename", "Unknown"))
        reference_path = metadata.get("reference_path", metadata.get("source", "Unknown"))
        section_headers = metadata.get("section_headers", "")
        
        # Convert section_headers from string back to list if needed
        if isinstance(section_headers, str) and section_headers:
            section_headers = [s.strip() for s in section_headers.split(",") if s.strip()]
        elif not section_headers:
            section_headers = []
        
        source_info = {
            "file_name": reference_file,
            "file_path": reference_path,
            "section_headers": section_headers,
            "chunk_index": metadata.get("chunk_index", 0),
            "total_chunks": metadata.get("total_chunks", 1),
            "preview": metadata.get("preview", "")[:200] + "..." if len(metadata.get("preview", "")) > 200 else metadata.get("preview", "")
        }
        
        return source_info
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vectorstore"""
        try:
            collection = self.chroma_client.get_collection(name=self.collection_name)
            count = collection.count()
            
            # Get unique files
            results = collection.get()
            unique_files = set()
            for metadata in results.get("metadatas", []):
                if metadata and ("filename" in metadata or "reference_file" in metadata):
                    file_name = metadata.get("filename") or metadata.get("reference_file")
                    unique_files.add(file_name)
            
            return {
                "total_documents": count,
                "unique_files": len(unique_files),
                "files": list(unique_files)
            }
        except Exception as e:
            print(f"❌ Error getting collection stats: {str(e)}")
            return {"total_documents": 0, "unique_files": 0, "files": []}
    
    def delete_documents_by_file(self, file_path: str) -> bool:
        """Delete all documents from a specific file"""
        try:
            collection = self.chroma_client.get_collection(name=self.collection_name)
            
            # Get all document IDs for this file
            results = collection.get(where={"source": file_path})
            if results["ids"]:
                collection.delete(ids=results["ids"])
                print(f"✅ Deleted {len(results['ids'])} documents for file: {file_path}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting documents for file {file_path}: {str(e)}")
            return False
    
    def clear_all_documents(self) -> bool:
        """Clear all documents from the vectorstore"""
        try:
            collection = self.chroma_client.get_collection(name=self.collection_name)
            collection.delete()
            print("✅ Cleared all documents from vectorstore")
            return True
        except Exception as e:
            print(f"❌ Error clearing vectorstore: {str(e)}")
            return False



