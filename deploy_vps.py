#!/usr/bin/env python3
"""
Helper script to prepare your code for VPS deployment
"""

import os
import shutil

def create_env_template():
    """Create a .env.template file for deployment"""
    template = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Paths
CHROMA_DB_PATH=./chroma_db
UPLOAD_DIRECTORY=./uploads

# File Upload Settings
MAX_FILE_SIZE=10485760
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8001
STREAMLIT_PORT=8501
"""
    
    if not os.path.exists('.env.template'):
        with open('.env.template', 'w') as f:
            f.write(template)
        print("[OK] Created .env.template file")
    else:
        print("[INFO] .env.template already exists")

def create_deployment_readme():
    """Create a deployment-specific README"""
    readme = """# Deployment Instructions

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
"""
    
    if not os.path.exists('DEPLOY_VPS_README.md'):
        with open('DEPLOY_VPS_README.md', 'w') as f:
            f.write(readme)
        print("[OK] Created DEPLOY_VPS_README.md")
    else:
        print("[INFO] DEPLOY_VPS_README.md already exists")

def main():
    print("Preparing your Policy Chatbot for deployment...\n")
    
    create_env_template()
    create_deployment_readme()
    
    print("\nDeployment preparation complete!")
    print("\nNext steps:")
    print("1. Copy this folder to your VPS (or use git)")
    print("2. Create .env file: cp .env.template .env")
    print("3. Edit .env with your API key")
    print("4. Run: docker-compose up -d")
    print("\nFor detailed instructions, see DEPLOY_NOW.md")

if __name__ == "__main__":
    main()

