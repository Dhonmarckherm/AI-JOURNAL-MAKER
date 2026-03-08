# 🚀 COMPLETE RAILWAY DEPLOYMENT GUIDE

## Option 1: Deploy via Railway Website (EASIEST - Recommended)

### Step 1: Go to Railway
Open your browser and visit: **https://railway.app**

### Step 2: Sign Up / Login
- Click **"Start a New Project"**
- Login with **GitHub** (recommended) or Email

### Step 3: Create New Project
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Connect your GitHub account if prompted
- Select repository: **`AI-JOURNAL-MAKER`**

### Step 4: Add PostgreSQL Database
1. In your Railway project dashboard
2. Click **"New"** → **"Database"** → **"PostgreSQL"**
3. Wait for database to provision (about 30 seconds)

### Step 5: Add Environment Variables
1. Click on your **service** (not the database)
2. Go to **"Variables"** tab
3. Click **"Add Variable"**
4. Add this variable:
   ```
   OPENROUTER_API_KEY=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
   ```
5. Click **"Save"**

### Step 6: Deploy!
- Railway will automatically start deploying
- Watch the **"Deployments"** tab for progress
- Wait until you see **"SUCCESS"**

### Step 7: Get Your URL
1. Go to **"Settings"** tab
2. Scroll to **"Domains"**
3. Click **"Generate Domain"**
4. Your app URL will be: `https://your-app.up.railway.app`

### Step 8: Test Your App!
- Open your URL in browser
- Register a new account
- Upload images and test all features!

---

## Option 2: Deploy via CLI (If you prefer command line)

### Step 1: Login with Browser
```bash
railway login
```
This will automatically open your browser. Click **"Authorize"**.

### Step 2: Initialize Project
```bash
cd "C:\Users\Lenovo\Downloads\AI JOURNAL\AI-JOURNAL-MAKER"
railway init
```
- Select **"Create new project"**
- Name: `ai-journal-maker`

### Step 3: Add Database
```bash
railway add postgres
```

### Step 4: Set Variables
```bash
railway variables set OPENROUTER_API_KEY=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
```

### Step 5: Deploy
```bash
railway up
```

### Step 6: Get Domain
```bash
railway domain
```

---

## ✅ Verify Deployment

After deployment, test these features:

1. **Register** - Create a new account
2. **Login** - Sign in with your credentials
3. **Upload Images** - Upload 1-5 images
4. **AI Analysis** - Wait for AI to generate report
5. **Save Journal** - Click "Save to Journal"
6. **Edit Journal** - Click "Edit" button, modify title/date/time/notes
7. **Export Word** - Click "Export as Word" to download .docx
8. **Delete Journal** - Click "Delete" to remove entry

---

## 🔧 Troubleshooting

### App won't start
1. Go to Railway dashboard
2. Click your project
3. Go to **"Deployments"** tab
4. Click latest deployment
5. Check **"Build Logs"** for errors

### Database error
Make sure you added PostgreSQL:
- Railway dashboard → Your Project → Should see "PostgreSQL" service

### API Key error
Verify environment variable:
- Railway dashboard → Service → Variables → Check `OPENROUTER_API_KEY` exists

### Port error
Railway auto-sets PORT. The app is configured to use it automatically.

---

## 💰 Railway Free Tier

- **$5 credit/month** (enough for ~500 hours)
- **1GB PostgreSQL** database included
- Perfect for hobby projects!

---

## 📞 Need Help?

- **Railway Docs**: https://docs.railway.app
- **Discord Support**: https://discord.gg/railway
- **Status Page**: https://status.railway.app

---

**Your app is ready to deploy! Follow Option 1 (website) for the easiest experience.**
