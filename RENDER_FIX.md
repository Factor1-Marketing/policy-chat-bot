# 🔧 Fix for Render Deployment - Connection Error

## The Problem

Your error:
```
Error loading documents: HTTPConnectionPool(host='localhost', port=8001): 
Connection refused
```

This happens because the frontend is trying to connect to `localhost:8001` but the backend isn't starting or accessible.

## The Solution

Update your Render service with these settings:

### Updated Start Command

Replace the start command in Render with:

```bash
python start_render.py
```

### Environment Variables (Add These)

In your Render service settings, add:

```
API_BASE_URL=http://localhost:8001
CHROMA_DB_PATH=./chroma_db
UPLOAD_DIRECTORY=./uploads
```

### Or Use Simpler Alternative

If that doesn't work, change the **Start Command** to just run Streamlit:

```bash
streamlit run chat_interface.py --server.port=$PORT --server.address=0.0.0.0
```

And run the backend separately using Render's background workers feature OR modify your code to use Streamlit's serverless functions.

---

## Quick Fix Steps

1. Go to your Render dashboard
2. Click on your `policy-chat-bot` service  
3. Go to **Settings**
4. Find **"Start Command"**
5. Replace with: `python start_render.py`
6. Add environment variable: `API_BASE_URL=http://localhost:8001`
7. Click **"Save Changes"** 
8. Go to **Manual Deploy** → **"Deploy latest commit"**

---

## If Still Not Working

The issue is that Render can only expose ONE port to the internet. You're trying to run two services (FastAPI on 8001 and Streamlit on 8501).

**Better solution:** Use Streamlit's built-in API integration, or deploy as two separate services on Render.

### Option A: Single Streamlit Service (Simpler)

Change start command to:
```bash
streamlit run chat_interface.py --server.port=$PORT --server.address=0.0.0.0
```

Then modify `chat_interface.py` to call OpenAI directly (no FastAPI backend).

### Option B: Two Separate Render Services (More Complex)

1. Deploy backend as separate "Web Service" 
2. Deploy frontend as separate "Static Site"
3. Configure CORS between them

Let me know which approach you want!

