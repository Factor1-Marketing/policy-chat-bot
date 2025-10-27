# 🚀 Deploy Your Policy Chatbot Now

You have 3 main deployment options. **Option 1 (Docker on VPS)** is recommended for simplicity.

---

## Option 1: Docker on VPS (Recommended) ⭐

**Best for:** Full control, lowest cost, everything in one place

### Quick Start (15 minutes)

1. **Get a VPS** ($6/month on DigitalOcean)
   - Go to https://www.digitalocean.com/pricing
   - Create a $6/month Ubuntu 22.04 droplet
   - Note your server IP address

2. **Connect to your server:**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
   ```

4. **Upload your code:**
   
   **Option A: Using Git (recommended)**
   ```bash
   # On your server
   git clone https://github.com/yourusername/policy-chatbot.git
   cd policy-chatbot
   ```
   
   **Option B: Using SCP**
   ```bash
   # On your local machine (PowerShell)
   scp -r "G:\Web Apps\Policy Chat Bot\*" root@your-server-ip:/root/policy-chatbot/
   ```

5. **Create `.env` file:**
   ```bash
   # On your server
   cd policy-chatbot
   nano .env
   ```
   
   Add this content:
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   CHROMA_DB_PATH=./chroma_db
   UPLOAD_DIRECTORY=./uploads
   ```

6. **Deploy:**
   ```bash
   docker-compose up -d
   ```

7. **Access your app:**
   - Frontend: http://your-server-ip:8501
   - API: http://your-server-ip:8001

### Future Updates

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# View logs
docker-compose logs -f
```

---

## Option 2: Render.com (Easiest Cloud) ⭐

**Best for:** No server management, automatic deployments

### Quick Start

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/policy-chatbot.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign in with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository
   
3. **Configure:**
   - **Name:** policy-chatbot
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python start_backend.py & python start_frontend.py`
   - **Environment Variables:**
     - `OPENAI_API_KEY` = your key
     - `CHROMA_DB_PATH` = `./chroma_db`
     - `UPLOAD_DIRECTORY` = `./uploads`

4. **Add Persistent Disk:**
   - Click on your service
   - Go to "Settings" → "Disks"
   - Add disk for `/app/chroma_db` (2GB)
   - Add disk for `/app/uploads` (1GB)

5. **Access:** Your app will be live at `https://your-app.onrender.com`

**Cost:** Free tier available, $7/month for persistent disks

---

## Option 3: Railway.app (Modern Platform) 

**Best for:** Developer-friendly, great UI

### Quick Start

1. **Push to GitHub** (same as Option 2)

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure:**
   - Railway auto-detects Python
   - Add environment variables:
     - `OPENAI_API_KEY`
     - `CHROMA_DB_PATH` = `./chroma_db`
     - `UPLOAD_DIRECTORY` = `./uploads`

4. **Add Volume for Persistence:**
   - Click on your service
   - Go to "Volume"
   - Mount paths: `/app/chroma_db` and `/app/uploads`

5. **Access:** Your app will be live at your railway URL

**Cost:** $5/month for hobby plan

---

## Option 4: Replit (Fastest) 

**Best for:** Instant deployment, no setup

### Quick Start

1. Go to https://replit.com
2. Create account
3. Click "Import from GitHub"
4. Paste your repo URL
5. Add environment variables in "Secrets"
6. Click "Run"

**Access:** Your app will be live at `https://your-app.repl.co`

**Cost:** Free tier available, $7/month for better performance

---

## Which Should You Choose?

| Option | Cost | Difficulty | Best For |
|--------|------|------------|----------|
| **VPS + Docker** | $6/month | Medium | Production, full control |
| **Render.com** | Free-$7/month | Easy | Quick deployment |
| **Railway** | $5/month | Easy | Modern apps |
| **Replit** | Free-$7/month | Very Easy | Quick testing |

---

## Security Checklist

Before going live:

1. ✅ Remove hardcoded API keys (already fixed)
2. ⚠️ Set up firewall to allow only ports 80, 443, and 22
3. ⚠️ Add domain name and HTTPS (use Let's Encrypt)
4. ⚠️ Set up daily backups of `chroma_db` folder
5. ⚠️ Add rate limiting to prevent abuse
6. ⚠️ Monitor your OpenAI API usage

---

## Next Steps After Deployment

1. **Test with real questions**
2. **Share the URL with your testers**
3. **Monitor usage and costs**
4. **Get feedback and iterate**

---

## Need Help?

- Check `DEPLOYMENT_QUICK.md` for detailed VPS setup
- Check `DEPLOYMENT.md` for Vercel deployment
- View logs: `docker-compose logs -f` (Docker) or in your cloud dashboard

---

Your chatbot is ready to go live! 🚀

