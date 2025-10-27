import streamlit as st
import os
import json
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our RAG components
from rag_system import RAGSystem
from vector_store import VectorStoreManager
from document_processor import DocumentProcessor
from config import Config

# Configure Streamlit page
st.set_page_config(
    page_title="Policy Chat Bot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components (cached to persist across reruns)
@st.cache_resource
def initialize_components():
    """Initialize RAG system and other components"""
    try:
        config = Config()
        vector_store = VectorStoreManager()
        rag_system = RAGSystem()
        document_processor = DocumentProcessor()
        return {
            'config': config,
            'vector_store': vector_store,
            'rag_system': rag_system,
            'document_processor': document_processor
        }
    except Exception as e:
        st.error(f"Failed to initialize components: {str(e)}")
        return None

def format_source_info(source: Dict[str, Any]) -> str:
    """Format source information for display"""
    info = f"📄 **{source['file_name']}**"
    
    if source.get('section_headers'):
        info += f" - {', '.join(source['section_headers'])}"
    
    if source.get('relevance_score'):
        info += f" (Relevance: {source['relevance_score']:.3f})"
    
    return info

def display_sources(sources: List[Dict[str, Any]]):
    """Display source information with excerpts in an expandable section"""
    if not sources:
        return
    
    with st.expander(f"📚 Sources ({len(sources)})", expanded=True):
        for i, source in enumerate(sources, 1):
            # Create columns for better layout
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # File name and section headers
                file_name = source.get('file_name', 'Unknown Document')
                section_headers = source.get('section_headers', [])
                relevance_score = source.get('relevance_score', 0)
                
                # Display file info with better formatting
                file_path = source.get('file_path', '')
                if file_path:
                    # Create clickable file path
                    st.markdown(f"**{i}. 📄 [{file_name}](file:///{file_path.replace(chr(92), '/')})**")
                else:
                    st.markdown(f"**{i}. 📄 {file_name}**")
                
                if section_headers and len(section_headers) > 0:
                    st.markdown(f"*Sections: {', '.join(section_headers)}*")
                
                # Show excerpt/preview in a highlighted box
                preview_text = source.get('preview', '')
                if preview_text:
                    st.markdown("**📖 Excerpt:**")
                    
                    # Create expandable excerpt with full content option
                    with st.expander("View excerpt", expanded=True):
                        st.text(preview_text)
                        
                        # Add option to view full content
                        full_content = source.get('full_content', '')
                        if full_content and len(full_content) > len(preview_text):
                            with st.expander("📄 View full content"):
                                st.text(full_content)
            
            with col2:
                # Display relevance score as a badge
                if relevance_score > 0:
                    st.metric("Relevance", f"{relevance_score:.3f}")
                    
                    # Visual indicator
                    if relevance_score > 0.8:
                        st.success("Highly Relevant")
                    elif relevance_score > 0.5:
                        st.info("Moderately Relevant")
                    else:
                        st.warning("Somewhat Relevant")
                
                # File size info if available
                file_size = source.get('file_size')
                if file_size:
                    # Convert to human readable
                    if file_size < 1024:
                        size_str = f"{file_size}B"
                    elif file_size < 1024 * 1024:
                        size_str = f"{file_size / 1024:.1f}KB"
                    else:
                        size_str = f"{file_size / (1024 * 1024):.1f}MB"
                    st.caption(f"Size: {size_str}")

def main():
    """Main application entry point"""
    st.title("📚 Policy Chat Bot")
    st.markdown("Ask questions about your policy documents using AI-powered search.")
    
    # Initialize components
    components = initialize_components()
    if components is None:
        st.stop()
    
    # Store in session state
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = components['rag_system']
        st.session_state.vector_store = components['vector_store']
        st.session_state.document_processor = components['document_processor']
        st.session_state.config = components['config']
    
    # Sidebar for document management
    with st.sidebar:
        st.header("📂 Document Management")
        
        # Document upload
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a policy document",
            type=['pdf', 'txt', 'md', 'docx'],
            help="Upload PDF, TXT, MD, or DOCX files"
        )
        
        if uploaded_file is not None:
            if st.button("📤 Upload Document", use_container_width=True):
                with st.spinner("Processing document..."):
                    try:
                        # Save uploaded file
                        upload_dir = st.session_state.config.UPLOAD_DIRECTORY
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        file_path = os.path.join(upload_dir, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Process document
                        documents = st.session_state.document_processor.process_document(file_path)
                        
                        # Add to vector store
                        success = st.session_state.vector_store.add_documents(documents)
                        
                        if success:
                            st.success(f"✅ {uploaded_file.name} uploaded and processed!")
                            st.balloons()
                        else:
                            st.error("Failed to process document")
                            os.remove(file_path)
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        st.divider()
        
        # Document list
        st.subheader("📋 Uploaded Documents")
        
        try:
            stats = st.session_state.vector_store.get_collection_stats()
            if stats and 'document_count' in stats and stats['document_count'] > 0:
                st.info(f"Total documents: {stats.get('document_count', 0)}")
                st.info(f"Total chunks: {stats.get('chunk_count', 0)}")
                
                # List documents
                documents = os.listdir(st.session_state.config.UPLOAD_DIRECTORY)
                pdf_files = [f for f in documents if f.endswith(('.pdf', '.txt', '.md', '.docx'))]
                
                if pdf_files:
                    for file_name in pdf_files:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.text(file_name)
                        with col2:
                            if st.button("🗑️", key=f"delete_{file_name}", help="Delete document"):
                                file_path = os.path.join(st.session_state.config.UPLOAD_DIRECTORY, file_name)
                                try:
                                    # Remove from vector store
                                    st.session_state.vector_store.delete_document(file_name)
                                    # Remove file
                                    os.remove(file_path)
                                    st.success(f"Deleted {file_name}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
            else:
                st.info("No documents uploaded yet. Upload a document to get started!")
                
        except Exception as e:
            st.warning("Error loading documents. Upload a document to get started.")
        
        st.divider()
        
        # Clear all button
        if st.button("🗑️ Clear All Documents", type="secondary"):
            try:
                # Clear vector store
                st.session_state.vector_store.clear_all()
                # Clear upload directory
                for file in os.listdir(st.session_state.config.UPLOAD_DIRECTORY):
                    if file.endswith(('.pdf', '.txt', '.md', '.docx')):
                        os.remove(os.path.join(st.session_state.config.UPLOAD_DIRECTORY, file))
                st.success("All documents cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Main chat interface
    st.header("💬 Chat")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display sources if available
            if message["role"] == "assistant" and "sources" in message:
                display_sources(message["sources"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your policy documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating response..."):
                try:
                    # Call RAG system directly (no HTTP)
                    response = st.session_state.rag_system.generate_response(prompt, k=5)
                except Exception as e:
                    response = {
                        "answer": f"Error: {str(e)}",
                        "sources": []
                    }
            
            if "error" in response:
                st.error(f"Error: {response['error']}")
            else:
                # Display the answer
                st.markdown(response.get('answer', 'No answer generated'))
                
                # Display sources
                if response.get('sources'):
                    display_sources(response['sources'])
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.get('answer', ''),
                    "sources": response.get('sources', [])
                })
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.8em;'>
            Policy Chat Bot - Powered by RAG and OpenAI
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

