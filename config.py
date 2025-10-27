import os
from dotenv import load_dotenv

try:
    load_dotenv()
except UnicodeDecodeError:
    # Handle encoding issues with .env file
    pass

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY", "./uploads")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))  # Smaller chunks for better precision
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))  # Proportional overlap
    
    # Ensure directories exist
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
