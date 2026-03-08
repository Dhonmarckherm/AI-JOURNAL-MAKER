# AI Journal Maker - Railway Deployment

## 🚀 Deploy to Railway in 5 Minutes

### Prerequisites
- GitHub account
- Railway account (free tier available)
- OpenRouter API key (or Google Gemini)

---

## Step 1: Push to GitHub

```bash
# Initialize git repo (if not already)
git init
git add .
git commit -m "Initial commit - AI Journal Maker"

# Create repo on GitHub and push
git remote add origin https://github.com/yourusername/ai-journal-maker.git
git push -u origin main
```

---

## Step 2: Create Railway Account

1. Go to https://railway.app/
2. Click **"Login"** → Sign in with GitHub
3. You get $5 free credit (enough for hobby projects)

---

## Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your `ai-journal-maker` repository
4. Railway auto-detects Python/FastAPI

---

## Step 4: Add PostgreSQL Database

1. In your Railway project, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Wait for database to provision (~30 seconds)
3. Railway automatically sets `DATABASE_URL` environment variable

---

## Step 5: Add Cloudinary (Image Storage)

1. Go to https://cloudinary.com/
2. Sign up for free account
3. Copy your **Cloudinary URL** (from Dashboard)
   - Format: `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`
4. In Railway, go to your project → **Variables** → **Add Variable**
   - Key: `CLOUDINARY_URL`
   - Value: `cloudinary://your-key:your-secret@your-cloud`

---

## Step 6: Add API Keys

In Railway → Variables, add:

| Key | Value |
|-----|-------|
| `OPENROUTER_API_KEY` | `sk-or-v1-your-key-here` |
| `CLOUDINARY_URL` | `cloudinary://...` |

---

## Step 7: Deploy!

1. Railway automatically deploys on push
2. Go to **Settings** → **Domains**
3. Click **"Generate Domain"**
4. Your app is live at: `https://your-app.railway.app`

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ Auto-set by Railway | PostgreSQL connection |
| `CLOUDINARY_URL` | ✅ | Cloud image storage |
| `OPENROUTER_API_KEY` | ✅ | AI image analysis |
| `PORT` | Auto-set | Server port (default: 8000) |

---

## Testing

1. Open your Railway URL
2. Register a new account
3. Login
4. Upload an image
5. Generate AI report!

---

## Troubleshooting

### Build Fails
- Check build logs in Railway dashboard
- Ensure `requirements_journal.txt` is correct

### Database Errors
- Verify PostgreSQL is connected
- Check `DATABASE_URL` is set

### Image Upload Fails
- Verify `CLOUDINARY_URL` is correct
- Check Cloudinary dashboard for quota

### API Errors
- Verify `OPENROUTER_API_KEY` is valid
- Check OpenRouter dashboard for credits

---

## Pricing

**Railway Free Tier:**
- $5 credit/month
- ~500 hours of runtime
- 1GB database included

**Cloudinary FREE:**
- 25GB storage
- 25GB bandwidth/month
- Unlimited transformations

**OpenRouter:**
- Pay per request
- ~$0.01 per image analysis

---

## Custom Domain (Optional)

1. Buy domain (Namecheap, GoDaddy, etc.)
2. In Railway → Settings → Domains
3. Click **"Add Custom Domain"**
4. Update DNS records as instructed

---

## Updates

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push

# Railway auto-deploys on push!
```

---

## Support

- Railway Docs: https://docs.railway.app/
- Cloudinary Docs: https://cloudinary.com/documentation
- FastAPI Docs: https://fastapi.tiangolo.com/
