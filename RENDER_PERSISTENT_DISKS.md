# 📦 How to Add Persistent Disks on Render

Persistent disks ensure your ChromaDB data and uploaded files survive app restarts and deployments.

## Step-by-Step Instructions

### Step 1: Create Your Web Service First
- Deploy your service to Render (follow RENDER_DEPLOY_STEPS.md)
- Wait for initial deployment to complete

### Step 2: Navigate to Your Service
1. Go to https://dashboard.render.com
2. Find your `policy-chat-bot` service
3. Click on it to open the service page

### Step 3: Access Disk Settings
1. In the left sidebar, click **"Disks"** (or go to Settings → Disks)
2. Click the **"+ Add New Disk"** button

### Step 4: Add ChromaDB Disk (Data Storage)
Configure as follows:

```
Name: chromadb-data
Mount Path: /app/chroma_db
Size: 2 GB
```

- **Name:** Any name you prefer (e.g., `chromadb-data`, `vector-db`)
- **Mount Path:** `/app/chroma_db` - This is where your ChromaDB database files will be stored
- **Size:** Start with `2 GB` (you can increase later if needed)
- **Region:** Same region as your service

Click **"Add Disk"**

### Step 5: Add Uploads Disk (File Storage)
Add a second disk for uploaded documents:

```
Name: uploads-data
Mount Path: /app/uploads  
Size: 1 GB
```

- **Name:** Any name you prefer (e.g., `uploads-data`, `documents`)
- **Mount Path:** `/app/uploads` - Where PDF documents are stored
- **Size:** Start with `1 GB` (increase if you expect many documents)

Click **"Add Disk"**

### Step 6: Redeploy (if needed)
- If you added disks after initial deployment, Render may ask you to redeploy
- Go to **"Manual Deploy"** in the left sidebar
- Click **"Deploy latest commit"**

---

## ⚠️ Important Notes

### Storage Locations in Your App

Your app looks for files in:
- `./chroma_db/` → Now mounted at `/app/chroma_db` on the persistent disk
- `./uploads/` → Now mounted at `/app/uploads` on the persistent disk

This means:
- ✅ Data persists across deployments
- ✅ Data survives container restarts
- ✅ Data persists even if you update your code
- ❌ Data is **NOT** deleted when you delete the service

### Disk Management

**View Disk Usage:**
- Go to your service → Disks
- See how much space is being used

**Increase Disk Size:**
- If you run out of space, you can increase disk size
- Go to Disks → Edit → Increase size
- **Warning:** You cannot decrease disk size after creation

**Remove Disk:**
- Go to Disks → Delete disk
- **Warning:** This will permanently delete all data on that disk

### Backup Your Data

Even though data is on persistent disks, always backup:

```bash
# Download database backup (if you have SSH access)
# Or use Render's snapshot feature if available
```

---

## ✅ Verification

After adding disks, verify they're mounted:

1. **Check Render Logs:**
   - Go to your service → Logs
   - Look for startup messages
   - Should see paths like `/app/chroma_db` and `/app/uploads`

2. **Upload a Test Document:**
   - Go to your live app URL
   - Upload a test PDF
   - Check logs to confirm it's stored in `/app/uploads`

3. **Restart the Service:**
   - Go to Manual Deploy → Deploy
   - Your data should still be there after restart

---

## 🎯 Quick Reference

| Disk | Mount Path | Purpose | Size |
|------|-----------|---------|------|
| `chromadb-data` | `/app/chroma_db` | Vector database files | 2 GB |
| `uploads-data` | `/app/uploads` | PDF documents | 1 GB |

---

## 🆘 Troubleshooting

### "Disk mount failed"
- Check that mount paths match: `/app/chroma_db` and `/app/uploads`
- Ensure no typos in paths

### "Out of space"
- Increase disk size in Render dashboard
- Or delete old documents

### "Data still disappearing"
- Verify disks are actually mounted:
  - Go to service → Disks
  - Should see "Mounted" status
- Check mount paths in code match disk mount paths

---

## 💡 Best Practices

1. **Monitor Usage:** Check disk usage regularly
2. **Set Alerts:** Set up alerts when disk usage exceeds 80%
3. **Regular Backups:** Export important data periodically
4. **Plan Ahead:** Start with larger disks if you expect lots of data
5. **Use Different Disks:** Don't put everything on one disk

---

**Your persistent disks are now configured!** Your data will persist across all deployments and restarts. 🎉

