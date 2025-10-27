# 🚀 Quick Deployment Guide

## Deployment Method: VPS with Docker (Recommended - 15 minutes)

### Why This is the Quickest:
- ✅ No external services to set up
- ✅ Everything runs in one container
- ✅ ChromaDB and files persist on the server
- ✅ Simple updates by replacing the container
- ✅ Full control over the system

---

## 📋 Step-by-Step Deployment

### Step 1: Get a VPS (5 minutes)

**Options:**
- **DigitalOcean**: https://www.digitalocean.com/pricing
- **Linode**: https://www.linode.com/pricing/
- **Hetzner**: https://www.hetzner.com/cloud

**Recommended:** DigitalOcean Droplet ($6/month)
- Choose: Ubuntu 22.04
- Size: Basic $6/month (1GB RAM) is enough
- Location: Nearest to your users

---

### Step 2: Set Up Docker on Server (3 minutes)

**SSH into your server:**
```bash
ssh root@your-server-ip
```

**Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

**Verify:**
```bash
docker --version
docker-compose --version
```

---

### Step 3: Upload Your Code (3 minutes)

**On your local machine, create the deployment package:**

```bash
cd "H:\Policy Chat Bot"
git init
git add .
git commit -m "Initial deployment"
```

**Then on the server:**

```bash
# On your server
git clone https://github.com/yourusername/policy-chatbot.git
cd policy-chatbot
```

---

### Step 4: Configure and Deploy (2 minutes)

**Create `.env` file on server:**
```bash
nano .env
```

**Add:**
```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Build and run:**
```bash
docker-compose up -d
```

---

### Step 5: Test Your Deployment (2 minutes)

**Check if it's running:**
```bash
docker ps
```

**View logs:**
```bash
docker-compose logs -f
```

**Access your app:**
- Frontend: http://your-server-ip:8501
- Backend API: http://your-server-ip:8001

---

## 🔄 Managing Your Deployment

### Start Services:
```bash
docker-compose up -d
```

### Stop Services:
```bash
docker-compose down
```

### View Logs:
```bash
docker-compose logs -f
```

### Update Application:
```bash
git pull
docker-compose up -d --build
```

### Backup Database:
```bash
# Copy the chroma_db folder
docker exec policy-chatbot tar czf - /app/chroma_db > backup.tar.gz
```

### Restore Database:
```bash
docker cp backup.tar.gz policy-chatbot:/app/
docker exec policy-chatbot tar xzf /app/backup.tar.gz -C /app/
```

---

## 🔒 Production Considerations

### 1. Domain Name (Optional)
```bash
# Point your domain to server IP
# A record: @ -> your-server-ip
```

### 2. HTTPS (Optional but Recommended)
```bash
# Install nginx
apt install nginx

# Install certbot
apt install certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d yourdomain.com
```

### 3. Firewall
```bash
# Allow only necessary ports
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### 4. Auto-Restart on Reboot
Docker Compose already handles this with `restart: unless-stopped`

### 5. Monitoring (Optional)
```bash
# Install monitoring
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower
```

---

## 💰 Total Cost

| Item | Cost |
|------|------|
| **VPS** (DigitalOcean) | $6/month |
| **OpenAI API** | $5-20/month |
| **Domain** (optional) | $12/year |
| **Total** | **$11-26/month** |

---

## 🎯 Quick Summary

**Time to Deploy:** ~15 minutes

**Commands:**
```bash
# 1. Get VPS
# 2. SSH to server
ssh root@your-ip

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# 4. Clone your repo
git clone https://github.com/yourusername/policy-chatbot.git
cd policy-chatbot

# 5. Add your OpenAI key
echo "OPENAI_API_KEY=sk-your-key" > .env

# 6. Deploy
docker-compose up -d

# 7. Done! Visit http://your-ip:8501
```

**That's it!** Your policy chatbot is now live on the internet. 🎉

---

## 🔧 Troubleshooting

### Can't access the website?
```bash
# Check if Docker is running
docker ps

# Check firewall
ufw status
```

### Need to reset?
```bash
docker-compose down
rm -rf chroma_db/* uploads/*
docker-compose up -d
```

### Want to add new documents?
1. Upload via the web interface at port 8501
2. Or copy files to `./uploads/` folder and restart

---

## 📚 Next Steps

1. **Custom domain** - Point your domain to the server
2. **HTTPS** - Add SSL certificate
3. **Backups** - Set up automated backups
4. **Monitoring** - Add health checks
5. **Scaling** - Add more resources if needed

Your policy chatbot is ready for production! 🚀

