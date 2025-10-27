# Quick Fix for Render 502 Error

## The Problem
Streamlit is trying to call `http://localhost:8001` which doesn't exist because we're not running the FastAPI backend separately.

## Temporary Fix (3 minutes)

Instead of the complex solution, let's just disable the parts that are failing:

1. Go to Render dashboard
2. Click your service → Settings  
3. Under **Environment Variables**, add:

```
DISABLE_API_CALLS=true
```

4. Update the file `chat_interface.py` line 17 to check this variable:

```python
# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")
DISABLE_API = os.getenv("DISABLE_API_CALLS", "false").lower() == "true"
```

Then modify the get_documents() method to return empty list when disabled.

## Better Solution

The REAL issue: **Render can't run two services.**

We need ONE of:
1. Deploy FastAPI as one service, Streamlit as another (separate services)
2. Make Streamlit self-contained (no FastAPI backend)

**Option 2 is simpler for Render.**

Would you like me to:
A) Make Streamlit call RAG directly (no backend needed)
B) Deploy as two separate services on Render
C) Use a different platform like Railway (better for multi-service apps)

