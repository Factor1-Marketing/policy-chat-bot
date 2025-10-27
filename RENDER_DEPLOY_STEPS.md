# 🚀 Deploy to Render.com - Step by Step

Your code is now on GitHub at: https://github.com/Factor1-Marketing/policy-chat-bot

## Steps to Deploy:

### 1. Go to Render.com
   - Visit: https://render.com
   - Sign in (create account if needed)
   - Click **"Sign in with GitHub"** to connect your account

### 2. Create New Web Service
   - Click the **"+ New +"** button (top right)
   - Select **"Web Service"**

### 3. Connect Your GitHub Repository
   - You'll see a list of your repositories
   - Find and click: **Factor1-Marketing/policy-chat-bot**
   - Click **"Connect"**

### 4. Configure the Service

   **Basic Settings:**
   - **Name:** `policy-chat-bot` (or any name you like)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** `Python 3`

   **Build Settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python start_backend.py & python start_frontend.py`

### 5. Add Environment Variables
   
   Click **"Add Environment Variable"** and add these:

   | Variable Name | Value |
   |--------------|-------|
   | `OPENAI_API_KEY` | your-actual-openai-api-key-here |
   | `CHROMA_DB_PATH` | `./chroma_db` |
   | `UPLOAD_DIRECTORY` | `./uploads` |
   | `PYTHON_VERSION` | `3.9` |

   ⚠️ **Important:** Keep your API key secret! Don't share it publicly.

### 6. Add Persistent Storage (CRITICAL!)

   Without this, your database will be lost when the app restarts.

   **Steps:**
   1. After creating the service, go to **Settings** → **Disks**
   2. Click **"+ Add New Disk"**
   3. Add disk for ChromaDB:
      - **Name:** `chromadb-data`
      - **Mount Path:** `/app/chroma_db`
      - **Size:** `2 GB`
   4. Add another disk for uploads:
      - **Name:** `uploads-data`
      - **Mount Path:** `/app/uploads`
      - **Size:** `1 GB`

### 7. Deploy!

   - Click **"Create Web Service"**
   - Render will start building your app
   - This takes about 5-10 minutes
   - Watch the logs as it builds and starts

### 8. Access Your App

   Once deployed, your app will be live at:
   ```
   https://policy-chat-bot.onrender.com
   ```
   *(exact URL will be shown in the Render dashboard)*

---

## 🔧 After Deployment

### Upload Documents
- Go to your live URL
- Use the sidebar to upload policy documents
- Documents will be processed and stored in ChromaDB
- Share the URL with testers!

### Monitor Usage
- Check Render dashboard for usage stats
- Monitor OpenAI API costs at https://platform.openai.com/usage
- Check logs in Render dashboard for any issues

### Update Your App
- Push changes to GitHub
- Render auto-deploys from your `main` branch

---

## 💰 Cost Breakdown

**Render.com:**
- Free tier: Limited hours/month (spins down after inactivity)
- $7/month: Always-on (recommended for production)

**OpenAI API:**
- ~$5-20/month depending on usage

**Total: $12-27/month for always-on production**

---

## 📝 Quick Commands

```bash
# View logs
# (in Render dashboard → Logs)

# Check deployment status
# (in Render dashboard)
```

---

## 🆘 Troubleshooting

### App won't start?
- Check logs in Render dashboard
- Verify environment variables are set correctly
- Check that persistent disks are mounted

### Documents not saving?
- Verify persistent disks are added and mounted correctly
- Check disk sizes are adequate

### API errors?
- Verify OPENAI_API_KEY is set correctly
- Check OpenAI API credits

---

**Need help?** Check the Render documentation: https://render.com/docs

Your chatbot will be live in ~10 minutes! 🎉

