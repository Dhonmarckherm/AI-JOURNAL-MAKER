# 🚀 Deploy AI Journal Maker to Vercel

Complete guide for deploying the AI Journal Maker to Vercel.

---

## ⚡ Quick Deploy

### Option 1: Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to project
cd "AI-JOURNAL-MAKER"

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Option 2: GitHub Integration

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Configure and deploy

---

## 📋 Pre-Deployment Checklist

### 1. Set Environment Variables

In Vercel Dashboard, go to **Settings → Environment Variables** and add:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | ✅ | AI image analysis (get from [openrouter.ai](https://openrouter.ai)) |
| `DATABASE_URL` | Optional | PostgreSQL URL (if using external DB) |

### 2. Update Configuration

Edit `journal_maker/journal_config.json` if needed:

```json
{
  "llm_provider": "openrouter",
  "model": "nvidia/nemotron-nano-12b-v2-vl:free",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

---

## 🏗️ Project Structure for Vercel

```
AI-JOURNAL-MAKER/
├── api/
│   └── index.py          # Vercel serverless entry point
├── journal_maker/
│   ├── journal_ai.py     # AI analysis module
│   ├── journal_db.py     # Database operations
│   └── journal_config.json
├── journal_templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── app.js
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
└── README_VERCEL.md      # This file
```

---

## 🔧 Deployment Steps

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login

```bash
vercel login
```

### Step 3: Link Project

```bash
vercel link
```

### Step 4: Add Environment Variables

```bash
vercel env add OPENROUTER_API_KEY
# Enter your API key when prompted
```

### Step 5: Deploy

```bash
# Development deployment
vercel

# Production deployment
vercel --prod
```

---

## 📊 Vercel Configuration

### vercel.json Explained

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "journal_templates/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "journal_templates/$1"
    },
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

---

## 💾 Data Storage

### Vercel Limitations
- Vercel serverless functions are **stateless**
- `/tmp` directory is available (512MB limit)
- Data in `/tmp` is **temporary** (cleared after function execution)

### Solutions for Persistent Data

#### Option 1: External Database (Recommended)
Use a cloud database service:
- [Neon](https://neon.tech) - Serverless PostgreSQL (free tier)
- [Supabase](https://supabase.com) - PostgreSQL + extras (free tier)
- [Railway](https://railway.app) - PostgreSQL ($5/month)

Update `DATABASE_URL` environment variable:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

#### Option 2: SQLite with Caveats
- Works for demo/testing
- Data may be lost between invocations
- Not recommended for production

---

## 🖼️ Image Storage

### Current Implementation
- Images stored in `/tmp/journal_data/images/`
- Temporary storage (cleared after function execution)

### Production Solutions

#### Option 1: Cloudinary (Recommended)
```bash
# Add to Vercel environment variables
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

#### Option 2: AWS S3
```bash
# Add to Vercel environment variables
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=your_bucket
```

---

## 🔍 Testing Locally

### Simulate Vercel Environment

```bash
# Install Vercel CLI
npm install -g vercel

# Run locally
vercel dev
```

### Test Endpoints

```bash
# Health check
curl https://your-app.vercel.app/api/health

# Login
curl -X POST https://your-app.vercel.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

---

## 🐛 Troubleshooting

### Issue: Module Not Found

```bash
# Make sure requirements.txt is in project root
# Check all dependencies are listed
pip install -r requirements.txt
```

### Issue: Environment Variables Not Working

1. Go to Vercel Dashboard → Project → Settings → Environment Variables
2. Ensure variables are added for correct environment (Production/Preview)
3. Redeploy after adding variables

### Issue: 500 Error on Image Upload

- Check file size (max 10MB)
- Verify image format (jpg, png, gif, webp)
- Check `/tmp` directory space

### Issue: Database Errors

- Verify `DATABASE_URL` format
- Ensure database allows connections from Vercel IPs
- Check database user permissions

---

## 📈 Vercel Limits

| Feature | Free Plan | Pro Plan |
|---------|-----------|----------|
| Serverless Function Duration | 10s | 60s |
| Function Size | 50MB | 250MB |
| /tmp Storage | 512MB | 1024MB |
| Bandwidth | 100GB/month | 1TB/month |

**Note:** AI image analysis may exceed 10s limit for large images. Consider upgrading to Pro plan.

---

## 🔐 Security Best Practices

1. **Never commit `.env` files** to Git
2. Use Vercel Environment Variables for secrets
3. Enable HTTPS (automatic on Vercel)
4. Set strong passwords for user accounts
5. Regularly rotate API keys

---

## 📝 Post-Deployment Checklist

- [ ] Test user registration
- [ ] Test user login
- [ ] Upload test images
- [ ] Verify AI analysis works
- [ ] Test journal save/edit/delete
- [ ] Test Word export
- [ ] Check error handling
- [ ] Monitor function logs in Vercel dashboard

---

## 🔗 Useful Links

- [Vercel Python Documentation](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenRouter API](https://openrouter.ai/docs)

---

## 🆘 Support

For issues or questions:
1. Check Vercel function logs
2. Review error messages in browser console
3. Verify environment variables are set correctly
4. Test locally with `vercel dev`

---

**Deployed with ❤️ on Vercel**
