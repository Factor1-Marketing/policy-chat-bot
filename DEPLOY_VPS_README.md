# Deployment Instructions

## For VPS Deployment

1. Copy this entire folder to your server (or use git)
2. Create a `.env` file from `.env.template`:
   ```bash
   cp .env.template .env
   nano .env  # Edit with your API key
   ```
3. Run deployment:
   ```bash
   docker-compose up -d
   ```

## Environment Variables Required

- `OPENAI_API_KEY` - Your OpenAI API key (required)

## Volumes (Data Persistence)

The following folders will persist data:
- `chroma_db/` - Vector database
- `uploads/` - Uploaded documents

## Accessing Your App

- Frontend: http://your-server-ip:8501
- API: http://your-server-ip:8001
- API Docs: http://your-server-ip:8001/docs

## Managing the Deployment

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build

# Backup database
docker exec policy-chatbot tar czf /app/backup.tar.gz /app/chroma_db
docker cp policy-chatbot:/app/backup.tar.gz ./backup.tar.gz
```

## Security

Before going live:
1. Set up a firewall (UFW)
2. Add domain name and HTTPS
3. Change default ports if needed
4. Monitor API usage
