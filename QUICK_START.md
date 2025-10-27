# 🚀 Quick Start Guide - Policy Chat Bot

## Fresh Installation & Launch

### Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 2: Set Up Environment

```bash
# Run the setup script (creates directories and .env file)
python setup.py
```

### Step 3: Configure API Key

1. Get an OpenAI API key from: https://platform.openai.com/api-keys
2. Edit the `.env` file and replace `your_openai_api_key_here` with your actual API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 4: Launch the Application

**Option A: Run Both Services Together**
```bash
python run.py both
```

**Option B: Run Separately (Recommended for development)**
```bash
# Terminal 1 - Backend API
python run.py backend

# Terminal 2 - Frontend Interface  
python run.py frontend
```

### Step 5: Access the Interface

- **Web Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

## First-Time Usage

### 1. Upload Policy Documents

1. Open http://localhost:8501 in your browser
2. In the left sidebar, click "Choose a policy document"
3. Select PDF, TXT, MD, or DOCX files
4. Click "Upload Document"
5. Wait for processing to complete

### 2. Start Chatting

1. Type your question in the chat input at the bottom
2. Press Enter or click Send
3. Get answers with source references
4. Click on "📚 Sources" to see where the answer came from

### 3. Manage Documents

- View uploaded documents in the sidebar
- Delete documents using the 🗑️ button
- Clear all documents with "Clear All Documents"

## Example Questions to Try

- "What is the company's remote work policy?"
- "How many vacation days do employees get?"
- "What are the security requirements for data handling?"
- "What is the process for requesting time off?"

## Troubleshooting

### Common Issues

**❌ "OpenAI API Key Error"**
- Check your `.env` file has the correct API key
- Ensure you have OpenAI credits

**❌ "No documents found"**
- Upload documents first using the sidebar
- Check file formats are supported (PDF, TXT, MD, DOCX)

**❌ "Connection refused"**
- Make sure both services are running
- Check ports 8000 and 8501 are available

**❌ "File upload failed"**
- Check file size (max 10MB)
- Ensure file format is supported

### Getting Help

- Check the full README.md for detailed documentation
- View API docs at http://localhost:8000/docs
- Check terminal output for error messages

## Success! 🎉

You should now have a fully functional RAG-based policy chatbot that can:
- Answer questions about your policy documents
- Provide source references
- Handle multiple document types
- Give accurate, cited responses
