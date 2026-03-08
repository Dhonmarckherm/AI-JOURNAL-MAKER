# 🚀 Deploy AI Journal Maker to Railway

Complete step-by-step guide for deploying to Railway.

---

## 📋 Prerequisites

- Railway account (free tier available at https://railway.app)
- OpenRouter API key (you already have one)
- Git installed (optional but recommended)

---

## 🚀 Quick Deploy (4 Steps)

### Step 1: Login to Railway

```bash
cd "C:\Users\Lenovo\Downloads\AI JOURNAL\AI-JOURNAL-MAKER"
railway login
```

This will open your browser. Click "Authorize" to login.

### Step 2: Create New Project

```bash
railway init
```

- Select "Create new project"
- Name it: `ai-journal-maker`
- Choose your team (if applicable)

### Step 3: Add PostgreSQL Database

```bash
railway add postgres
```

This creates a managed PostgreSQL database for your app.

### Step 4: Deploy

```bash
railway up
```

This will:
- Upload your code
- Install dependencies
- Start your application

---

## ⚙️ Environment Variables

After deployment, add your API key:

### Option A: Via CLI
```bash
railway variables set OPENROUTER_API_KEY=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
```

### Option B: Via Dashboard
1. Go to https://railway.app
2. Select your project
3. Click "Variables" tab
4. Add `OPENROUTER_API_KEY` with your key value

---

## 🌐 Get Your URL

After deployment completes:

```bash
railway domain
```

Your app will be available at: `https://your-app.up.railway.app`

---

## 📊 View Logs

```bash
# Real-time logs
railway logs

# View deployment status
railway status
```

---

## 🔧 Troubleshooting

### App won't start
```bash
# Check logs for errors
railway logs

# View build logs
railway logs --build
```

### Database connection issues
Railway automatically sets `DATABASE_URL`. Make sure it's in your variables.

### Port issues
Railway automatically sets the `PORT` variable. The app will use it.

---

## 💰 Railway Pricing

- **Free tier**: $5 credit/month (enough for hobby projects)
- **Paid tier**: $5/month + usage

---

## 📝 Project Structure for Railway

```
AI-JOURNAL-MAKER/
├── journal_maker/
│   ├── journal_app.py      # Main FastAPI app
│   ├── journal_ai.py       # AI analysis
│   ├── journal_db.py       # Database (PostgreSQL/SQLite)
│   └── requirements_journal.txt
├── journal_templates/
│   ├── index.html
│   ├── login.html
│   └── app.js
├── railway.json            # Railway config
├── nixpacks.toml          # Build configuration
└── .env.example
```

---

## 🔄 Update Deployment

After making changes:

```bash
# Push changes
git add .
git commit -m "Your changes"
git push

# Redeploy
railway up
```

---

## ✅ Post-Deployment Checklist

- [ ] App is accessible via URL
- [ ] User registration works
- [ ] User login works
- [ ] Image upload works
- [ ] AI analysis generates reports
- [ ] Journals save correctly
- [ ] Edit functionality works
- [ ] Word export works
- [ ] Delete functionality works

---

**Need Help?**
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
