from fastapi import FastAPI, File, UploadFile, HTTPException
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
from vector_store_prod import ProductionVectorStoreManager
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
vector_store = ProductionVectorStoreManager()

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    stream: bool = True

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence: float
    total_sources_found: int

@app.get("/")
async def root():
    return {"message": "Policy Chat Bot API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    try:
        stats = vector_store.get_collection_stats()
        return {
            "status": "healthy",
            "chromadb": "connected",
            "documents": stats["total_documents"],
            "files": stats["unique_files"]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "chromadb": "disconnected",
            "error": str(e)
        }

@app.post("/chat")
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

@app.post("/upload")
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
        
        # Save file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document
        documents = document_processor.process_document(temp_path)
        
        # Add to vector store
        success = vector_store.add_documents(documents)
        
        # Clean up temp file
        os.remove(temp_path)
        
        if success:
            return {
                "message": "Document uploaded and processed successfully",
                "file_name": file.filename,
                "chunks_created": len(documents),
                "success": True
            }
        else:
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

@app.post("/search")
async def search_documents(query: str, k: int = 10):
    """Search documents without generating a response"""
    try:
        results = rag_system.search_documents(query, k)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Handler for Vercel
handler = app



