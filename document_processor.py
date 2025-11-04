import os
import hashlib
from typing import List, Dict, Any
from pathlib import Path
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import Config

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text
        except Exception as e:
            print(f"Error reading PDF {file_path}: {str(e)}")
        return text
    
    def create_document_chunks(self, text: str, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """Split text into chunks and create Document objects with metadata"""
        if metadata is None:
            metadata = {}
        
        # Add file-specific metadata
        file_name = Path(file_path).name
        file_hash = self._calculate_file_hash(file_path)
        
        base_metadata = {
            "source": file_path,
            "filename": file_name,
            "file_hash": file_hash,
            **metadata
        }
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create Document objects with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = {
                **base_metadata,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            
            # Add reference link information (simplified for ChromaDB)
            ref_info = self._generate_reference_link(file_path, chunk, i, chunks)
            chunk_metadata["reference_file"] = ref_info["file_name"]
            chunk_metadata["reference_path"] = ref_info["file_path"]
            chunk_metadata["section_headers"] = ", ".join(ref_info["section_headers"]) if ref_info["section_headers"] else ""
            chunk_metadata["preview"] = ref_info["preview"][:200]  # Limit preview length
            
            doc = Document(page_content=chunk, metadata=chunk_metadata)
            documents.append(doc)
        
        return documents
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate hash of file for tracking changes"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return "unknown"
    
    def _generate_reference_link(self, file_path: str, chunk: str, chunk_index: int, all_chunks: List[str]) -> Dict[str, Any]:
        """Generate reference information for the chunk"""
        file_name = Path(file_path).name
        
        # Try to identify section headers in the chunk
        lines = chunk.split('\n')
        potential_sections = []
        
        for line in lines[:5]:  # Check first 5 lines for section headers
            line = line.strip()
            if line and (line.isupper() or line.endswith(':') or 
                        any(keyword in line.lower() for keyword in ['section', 'chapter', 'policy', 'procedure'])):
                potential_sections.append(line)
        
        reference_info = {
            "file_name": file_name,
            "file_path": file_path,
            "chunk_index": chunk_index,
            "section_headers": potential_sections[:2],  # Top 2 potential sections
            "preview": chunk[:200] + "..." if len(chunk) > 200 else chunk
        }
        
        return reference_info
    
    def process_document(self, file_path: str) -> List[Document]:
        """Process a single document and return chunks"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        else:
            # For other file types, read as text
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text = file.read()
        
        if not text.strip():
            raise ValueError(f"No text content found in file: {file_path}")
        
        return self.create_document_chunks(text, file_path)
    
    def process_multiple_documents(self, file_paths: List[str]) -> List[Document]:
        """Process multiple documents and return all chunks"""
        all_documents = []
        
        for file_path in file_paths:
            try:
                documents = self.process_document(file_path)
                all_documents.extend(documents)
                print(f"Processed {file_path}: {len(documents)} chunks")
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
        
        return all_documents
