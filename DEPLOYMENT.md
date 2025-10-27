# 🚀 Deployment Guide - Git + Vercel

## Prerequisites

1. **GitHub Account** - For code repository
2. **Vercel Account** - For hosting (free tier available)
3. **OpenAI API Key** - For embeddings and chat
4. **ChromaDB Service** - For vector storage

## Step-by-Step Deployment

### 1. Push Code to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit - Policy Chat Bot"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/policy-chatbot.git
git branch -M main
git push -u origin main
```

### 2. Set Up ChromaDB Service

You need a ChromaDB service for vector storage. Options:

#### Option A: Railway (Recommended)
1. Go to [Railway.app](https://railway.app)
2. Create new project
3. Add ChromaDB service:
   ```bash
   # In Railway dashboard, add service
   Service: ChromaDB
   Port: 8000
   ```
4. Note the public URL (e.g., `https://chromadb-production.up.railway.app`)

#### Option B: Render
1. Go to [Render.com](https://render.com)
2. Create new Web Service
3. Use Docker with ChromaDB image
4. Note the public URL

#### Option C: Self-hosted VPS
```bash
# On your VPS
docker run -d -p 8000:8000 \
  --name chromadb \
  --restart unless-stopped \
  chromadb/chroma:latest
```

### 3. Deploy to Vercel

1. **Connect GitHub to Vercel:**
   - Go to [Vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"
   - Import your repository

2. **Configure Environment Variables:**
   ```bash
   OPENAI_API_KEY=sk-your-openai-key-here
   CHROMA_DB_HOST=your-chromadb-host.com
   CHROMA_DB_PORT=8000
   API_BASE_URL=https://your-app.vercel.app/api
   ```

3. **Deploy Settings:**
   - Framework Preset: Other
   - Build Command: `pip install -r requirements-vercel.txt`
   - Output Directory: `./`
   - Install Command: `pip install -r requirements-vercel.txt`

### 4. Upload Documents

After deployment:

1. Go to your deployed app: `https://your-app.vercel.app`
2. Use the sidebar to upload policy documents
3. Documents will be processed and stored in ChromaDB

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vercel        │    │   ChromaDB      │    │   OpenAI        │
│   (Frontend +   │◄──►│   (Vector DB)   │◄──►│   (Embeddings   │
│   Backend API)  │    │   Railway/Render│    │   + Chat)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Cost Breakdown

### Vercel (Free Tier)
- ✅ Unlimited personal projects
- ✅ 100GB bandwidth/month
- ✅ Serverless functions
- ✅ Custom domains

### ChromaDB Service
- **Railway**: $5/month
- **Render**: $7/month  
- **VPS**: $5-10/month

### OpenAI API
- **Embeddings**: ~$0.0001 per 1K tokens
- **Chat**: ~$0.002 per 1K tokens
- **Estimated**: $5-20/month for typical usage

**Total Monthly Cost: $10-30**

## Troubleshooting

### Common Issues

1. **ChromaDB Connection Error**
   - Check environment variables
   - Verify ChromaDB service is running
   - Check firewall/network access

2. **Upload Fails**
   - Check file size limits
   - Verify file types are supported
   - Check ChromaDB storage capacity

3. **Slow Responses**
   - ChromaDB might be cold (Railway/Render sleep after inactivity)
   - Consider upgrading to always-on plan
   - Check OpenAI API rate limits

### Performance Optimization

1. **Enable ChromaDB Persistence:**
   ```bash
   # Add volume to ChromaDB container
   docker run -v chroma_data:/chroma/chroma chromadb/chroma
   ```

2. **Use CDN for Static Assets:**
   - Vercel automatically provides CDN
   - No additional setup needed

3. **Monitor Usage:**
   - Vercel dashboard shows function usage
   - ChromaDB service shows connection stats
   - OpenAI dashboard shows API usage

## Security Considerations

1. **Environment Variables:**
   - Never commit API keys to git
   - Use Vercel's environment variable system
   - Rotate keys regularly

2. **CORS Settings:**
   - Update `vercel.json` to restrict origins
   - Only allow your domain

3. **File Upload Limits:**
   - Set appropriate file size limits
   - Validate file types server-side
   - Scan uploaded files for malware

## Scaling

As your usage grows:

1. **Upgrade ChromaDB:**
   - Railway Pro: $20/month
   - Render Pro: $25/month
   - Better performance, more storage

2. **Add Monitoring:**
   - Vercel Analytics
   - ChromaDB metrics
   - Error tracking (Sentry)

3. **Implement Caching:**
   - Redis for query caching
   - CDN for static assets
   - Browser caching

## Support

- **Vercel Docs**: https://vercel.com/docs
- **ChromaDB Docs**: https://docs.trychroma.com
- **Railway Docs**: https://docs.railway.app
