import streamlit as st
import requests
import json
import time
from typing import List, Dict, Any

# Configure Streamlit page
st.set_page_config(
    page_title="Policy Chat Bot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8001"

class PolicyChatBot:
    def __init__(self):
        self.api_base = API_BASE_URL
    
    def upload_document(self, file) -> Dict[str, Any]:
        """Upload a document to the API"""
        try:
            files = {"file": file}
            response = requests.post(f"{self.api_base}/upload", files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def send_message(self, message: str, stream: bool = True) -> Dict[str, Any]:
        """Send a message to the chat API"""
        try:
            data = {"message": message, "stream": stream}
            response = requests.post(f"{self.api_base}/chat", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_documents(self) -> Dict[str, Any]:
        """Get list of uploaded documents"""
        try:
            response = requests.get(f"{self.api_base}/documents")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def delete_document(self, file_name: str) -> bool:
        """Delete a document"""
        try:
            response = requests.delete(f"{self.api_base}/documents/{file_name}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Error deleting document: {str(e)}")
            return False

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
                else:
                    st.markdown("*No preview available*")
            
            with col2:
                # Relevance score with color coding
                if relevance_score > 0.4:
                    st.success(f"🎯 Relevance: {relevance_score:.3f}")
                elif relevance_score > 0.3:
                    st.warning(f"📊 Relevance: {relevance_score:.3f}")
                else:
                    st.info(f"📈 Relevance: {relevance_score:.3f}")
                
                # Chunk information
                chunk_index = source.get('chunk_index', 0)
                st.caption(f"Chunk {chunk_index}")
                
                # Add download button for the source file
                file_path = source.get('file_path', '')
                if file_path and st.button("📥 Download", key=f"download_{i}_{time.time()}"):
                    try:
                        with open(file_path, 'rb') as file:
                            file_data = file.read()
                            st.download_button(
                                label="Download File",
                                data=file_data,
                                file_name=file_name,
                                mime="application/octet-stream",
                                key=f"dl_{i}_{time.time()}"
                            )
                    except Exception as e:
                        st.error(f"Could not download file: {str(e)}")
            
            # Add separator between sources
            if i < len(sources):
                st.divider()

def main():
    st.title("📚 Policy Chat Bot")
    st.markdown("Ask questions about your policy documents and get answers with source references!")
    
    # Initialize chat bot
    if 'chat_bot' not in st.session_state:
        st.session_state.chat_bot = PolicyChatBot()
    
    # Sidebar for document management
    with st.sidebar:
        st.header("📁 Document Management")
        
        # Upload section
        st.subheader("Upload Documents")
        uploaded_file = st.file_uploader(
            "Choose a policy document",
            type=['pdf', 'txt', 'md', 'docx'],
            help="Upload PDF, TXT, MD, or DOCX files"
        )
        
        if uploaded_file is not None:
            if st.button("Upload Document"):
                with st.spinner("Processing document..."):
                    result = st.session_state.chat_bot.upload_document(uploaded_file)
                    
                if result.get('success'):
                    st.success(f"✅ {result['message']}")
                    st.info(f"Created {result['chunks_created']} chunks")
                    # Clear the file uploader
                    st.rerun()
                else:
                    st.error(f"❌ Upload failed: {result.get('error', 'Unknown error')}")
        
        st.divider()
        
        # Document list
        st.subheader("Uploaded Documents")
        docs_result = st.session_state.chat_bot.get_documents()
        
        if 'error' in docs_result:
            st.error(f"Error loading documents: {docs_result['error']}")
        else:
            if docs_result['total_documents'] == 0:
                st.info("No documents uploaded yet")
            else:
                st.info(f"Total: {docs_result['total_documents']} chunks from {docs_result['unique_files']} files")
                
                for file_name in docs_result['files']:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(file_name)
                    with col2:
                        if st.button("🗑️", key=f"delete_{file_name}", help="Delete document"):
                            if st.session_state.chat_bot.delete_document(file_name):
                                st.success(f"Deleted {file_name}")
                                st.rerun()
        
        st.divider()
        
        # Clear all button
        if st.button("🗑️ Clear All Documents", type="secondary"):
            if st.session_state.get('confirm_clear', False):
                try:
                    response = requests.post(f"{API_BASE_URL}/clear")
                    response.raise_for_status()
                    st.success("All documents cleared!")
                    st.session_state.confirm_clear = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing documents: {str(e)}")
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm clearing all documents")
    
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
                response = st.session_state.chat_bot.send_message(prompt, stream=False)
            
            if "error" in response:
                st.error(f"Error: {response['error']}")
            else:
                # Display the answer
                st.markdown(response['answer'])
                
                # Display sources
                if response.get('sources'):
                    display_sources(response['sources'])
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response['answer'],
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
