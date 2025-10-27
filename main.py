from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import shutil
from pathlib import Path

from rag_system import RAGSystem
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from config import Config

app = FastAPI(title="Policy Chat Bot API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
config = Config()
rag_system = RAGSystem()
document_processor = DocumentProcessor()
vector_store = VectorStoreManager()

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    stream: bool = True

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence: float
    total_sources_found: int

class DocumentUploadResponse(BaseModel):
    message: str
    file_name: str
    chunks_created: int
    success: bool

class DocumentInfo(BaseModel):
    file_name: str
    file_path: str
    total_chunks: int
    sections: List[str]
    text_preview: str

@app.get("/")
async def root():
    return {"message": "Policy Chat Bot API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """Chat endpoint with RAG"""
    try:
        response = rag_system.generate_response(chat_message.message)
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(chat_message: ChatMessage):
    """Streaming chat endpoint"""
    async def generate():
        try:
            for chunk in rag_system.generate_streaming_response(chat_message.message):
                yield f"data: {json.dumps(chunk)}\n\n"
        except Exception as e:
            error_chunk = {
                "type": "error",
                "error": str(e),
                "answer": f"Error: {str(e)}",
                "sources": []
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a policy document"""
    try:
        # Validate file size
        if file.size > config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {config.MAX_FILE_SIZE} bytes"
            )
        
        # Validate file type
        allowed_extensions = ['.pdf', '.txt', '.md', '.docx']
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Save file
        file_path = os.path.join(config.UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document
        documents = document_processor.process_document(file_path)
        
        # Add to vector store
        success = vector_store.add_documents(documents)
        
        if success:
            return DocumentUploadResponse(
                message="Document uploaded and processed successfully",
                file_name=file.filename,
                chunks_created=len(documents),
                success=True
            )
        else:
            # Clean up file if processing failed
            os.remove(file_path)
            raise HTTPException(status_code=500, detail="Failed to process document")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    try:
        stats = vector_store.get_collection_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/{file_name}")
async def get_document_info(file_name: str):
    """Get information about a specific document"""
    try:
        # Find the file path
        file_path = None
        for file in os.listdir(config.UPLOAD_DIRECTORY):
            if file == file_name:
                file_path = os.path.join(config.UPLOAD_DIRECTORY, file)
                break
        
        if not file_path:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Get document summary
        summary = rag_system.get_document_summary(file_path)
        if "error" in summary:
            raise HTTPException(status_code=500, detail=summary["error"])
        
        return DocumentInfo(**summary)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents/{file_name}")
async def delete_document(file_name: str):
    """Delete a document and its chunks"""
    try:
        # Find and delete the file
        file_path = None
        for file in os.listdir(config.UPLOAD_DIRECTORY):
            if file == file_name:
                file_path = os.path.join(config.UPLOAD_DIRECTORY, file)
                break
        
        if not file_path:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete from vector store
        success = vector_store.delete_documents_by_file(file_path)
        
        # Delete file
        os.remove(file_path)
        
        if success:
            return {"message": f"Document {file_name} deleted successfully"}
        else:
            return {"message": f"File {file_name} deleted, but some chunks may remain in vector store"}
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_documents(query: str, k: int = 10):
    """Search documents without generating a response"""
    try:
        results = rag_system.search_documents(query, k)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_all_documents():
    """Clear all documents from the system"""
    try:
        # Clear vector store
        vector_store.clear_all_documents()
        
        # Clear upload directory
        for file in os.listdir(config.UPLOAD_DIRECTORY):
            file_path = os.path.join(config.UPLOAD_DIRECTORY, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        return {"message": "All documents cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
