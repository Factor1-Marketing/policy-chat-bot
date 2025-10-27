# Policy Chat Bot

A RAG-based chatbot that allows users to search through policy documents and get answers with source references.

## Features

- 📚 **Document Upload**: Upload PDF, TXT, MD, and DOCX files
- 🔍 **RAG Search**: Retrieve relevant information using vector similarity search
- 💬 **Chat Interface**: Interactive chat with streaming responses
- 📖 **Source References**: Get specific references to document sections
- 🗄️ **Vector Database**: Persistent storage using ChromaDB
- 🚀 **FastAPI Backend**: RESTful API with streaming support
- 🎨 **Streamlit Frontend**: Modern web interface

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   ChromaDB      │
│   Frontend      │◄──►│   Backend       │◄──►│   Vector Store  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │   (Embeddings   │
                       │   & Chat)       │
                       └─────────────────┘
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd policy-chat-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   CHROMA_DB_PATH=./chroma_db
   UPLOAD_DIRECTORY=./uploads
   MAX_FILE_SIZE=10485760
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   ```

## Usage

### 1. Start the Backend API

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 2. Start the Frontend Interface

In a new terminal:

```bash
streamlit run chat_interface.py
```

The web interface will be available at `http://localhost:8501`

### 3. Upload Documents

1. Open the web interface
2. Use the sidebar to upload policy documents
3. Wait for processing to complete

### 4. Start Chatting

1. Type your questions in the chat input
2. Get answers with source references
3. View document sections in the expandable sources

## API Endpoints

### Chat
- `POST /chat` - Send a message and get a response
- `POST /chat/stream` - Stream response chunks

### Documents
- `POST /upload` - Upload a document
- `GET /documents` - List all documents
- `GET /documents/{file_name}` - Get document info
- `DELETE /documents/{file_name}` - Delete a document
- `POST /clear` - Clear all documents

### Search
- `POST /search` - Search documents without generating response

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | OpenAI API key for embeddings and chat |
| `CHROMA_DB_PATH` | `./chroma_db` | Path to ChromaDB storage |
| `UPLOAD_DIRECTORY` | `./uploads` | Directory for uploaded files |
| `MAX_FILE_SIZE` | `10485760` | Maximum file size in bytes (10MB) |
| `CHUNK_SIZE` | `1000` | Text chunk size for processing |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |

### Customization

You can modify the system behavior by editing:

- `config.py` - Configuration settings
- `document_processor.py` - Document processing logic
- `rag_system.py` - RAG pipeline and prompts
- `vector_store.py` - Vector database operations

## How It Works

### 1. Document Processing
- Documents are uploaded and stored locally
- Text is extracted (PDF, TXT, MD, DOCX support)
- Text is split into chunks with metadata
- Chunks include reference information for source linking

### 2. Vector Storage
- Chunks are embedded using OpenAI embeddings
- Stored in ChromaDB with metadata
- Metadata includes file info, sections, and reference links

### 3. Retrieval
- User questions are embedded
- Similarity search finds relevant chunks
- Chunks are ranked by relevance score

### 4. Generation
- Relevant chunks are formatted with source info
- Prompt includes context and question
- OpenAI generates response with citations

### 5. Reference Links
- Each chunk includes source document info
- Section headers are identified
- Preview text is provided
- Relevance scores are shown

## Development

### Project Structure

```
policy-chat-bot/
├── main.py                 # FastAPI backend
├── chat_interface.py       # Streamlit frontend
├── rag_system.py          # RAG pipeline
├── document_processor.py  # Document processing
├── vector_store.py        # Vector database management
├── config.py             # Configuration
├── requirements.txt      # Dependencies
└── README.md            # This file
```

### Adding New Features

1. **New Document Types**: Extend `DocumentProcessor.extract_text_from_*` methods
2. **Custom Embeddings**: Modify `VectorStoreManager` to use different embedding models
3. **Enhanced Chunking**: Customize `RecursiveCharacterTextSplitter` parameters
4. **UI Improvements**: Modify Streamlit interface in `chat_interface.py`

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is set in the `.env` file
   - Check that you have sufficient API credits

2. **Document Upload Fails**
   - Check file size limits
   - Ensure file format is supported
   - Verify upload directory permissions

3. **No Search Results**
   - Ensure documents are properly processed
   - Check ChromaDB storage directory
   - Verify embeddings are generated

4. **Performance Issues**
   - Reduce chunk size for faster processing
   - Limit number of search results
   - Use smaller embedding models

### Logs

- Backend logs: Check terminal output when running `python main.py`
- Frontend logs: Check Streamlit interface for error messages
- Vector store: ChromaDB logs are stored in the configured directory

## Security Considerations

- Configure CORS properly for production
- Validate file uploads thoroughly
- Secure API endpoints with authentication
- Encrypt sensitive data in ChromaDB
- Implement rate limiting

## License

This project is licensed under the MIT License.
