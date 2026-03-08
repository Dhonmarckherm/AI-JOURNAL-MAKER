# 🚀 AI Journal Maker

**AI-powered journal creation system with image analysis**

![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)

---

## ✨ Features

- 📸 **Image Upload** - Upload multiple images
- 🤖 **AI Analysis** - GPT-4 Vision / Google Gemini image analysis
- 📝 **Journal Reports** - Auto-generated detailed journal entries
- 🔐 **User Authentication** - Secure login/register system
- 💾 **PostgreSQL** - Production-ready database (Railway)
- 🎨 **Modern UI** - Responsive Bootstrap 5 design
- 📊 **User Dashboard** - View, search, manage journal history

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Login   │  │  Upload  │  │  Journal │              │
│  │  Register│  │  Images  │  │  History │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Backend (FastAPI)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │   Auth   │  │  Journal │  │   Image  │              │
│  │  System  │  │   CRUD   │  │ Analysis │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
       │                  │                    │
       ▼                  ▼                    ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ PostgreSQL  │  │  OpenRouter │  │  Cloudinary │
│  (Railway)  │  │  AI Vision  │  │  (Images)   │
└─────────────┘  └─────────────┘  └─────────────┘
```

---

## 🚀 Quick Start (Local Development)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/ai-journal-maker.git
cd ai-journal-maker

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r journal_maker/requirements_journal.txt

# Setup environment
copy journal_maker\.env.example journal_maker\.env
# Edit .env and add your API keys
```

### Run Locally

```bash
cd journal_maker
python journal_app.py
```

Open **http://localhost:8000**

---

## ☁️ Deploy to Railway (Recommended)

### Quick Deploy with Railway CLI:

```bash
# Navigate to project
cd AI-JOURNAL-MAKER

# Login to Railway
railway login

# Initialize project
railway init

# Add PostgreSQL database
railway add postgres

# Deploy
railway up

# Get your URL
railway domain
```

### Environment Variables Required:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | ✅ | AI image analysis API key |

Railway automatically provides `DATABASE_URL` when you add PostgreSQL.

📖 **Full guide:** [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)

---

## ▲ Deploy to Vercel

### Quick Deploy with Vercel CLI:

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to project
cd AI-JOURNAL-MAKER

# Login
vercel login

# Deploy to production
vercel --prod
```

### Environment Variables Required:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | ✅ | AI image analysis API key |
| `DATABASE_URL` | Optional | PostgreSQL for persistent data |

📖 **Full guide:** [README_VERCEL.md](README_VERCEL.md)

---

## 📁 Project Structure

```
.
├── api/
│   └── index.py              # Vercel serverless entry point
├── journal_maker/
│   ├── journal_app.py        # FastAPI backend (local/Railway)
│   ├── journal_ai.py         # AI analysis (OpenRouter/Gemini)
│   ├── journal_db.py         # Database (SQLite/PostgreSQL)
│   ├── journal_config.json   # Configuration
│   ├── requirements_journal.txt
│   └── .env.example
├── journal_templates/
│   ├── index.html            # Main UI
│   ├── login.html            # Login page
│   ├── register.html         # Register page
│   └── app.js                # Frontend JavaScript
├── vercel.json               # Vercel configuration
├── railway.json              # Railway config
├── render.yaml               # Render config
├── DEPLOYMENT.md             # Deployment guide
├── README_VERCEL.md          # Vercel deployment guide
└── README.md                 # This file
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ (Railway) | PostgreSQL connection |
| `CLOUDINARY_URL` | ✅ | Cloud image storage |
| `OPENROUTER_API_KEY` | ✅ | AI image analysis |
| `GOOGLE_API_KEY` | Optional | Alternative to OpenRouter |
| `PORT` | Auto | Server port (default: 8000) |

### journal_config.json

```json
{
  "llm_provider": "openrouter",
  "model": "google/gemini-2.0-flash-exp:free",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

---

## 🎯 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login
- `POST /api/logout` - Logout
- `GET /api/me` - Get current user

### Journals
- `POST /api/analyze` - Upload & analyze images
- `GET /api/journals` - Get all journals
- `GET /api/journals/{id}` - Get specific journal
- `POST /api/journals` - Save journal
- `DELETE /api/journals/{id}` - Delete journal

---

## 💰 Pricing

### Railway Free
- $5 credit/month (~500 hours)
- 1GB PostgreSQL database
- Sufficient for hobby projects

### Cloudinary (Free)
- 25GB storage
- 25GB bandwidth/month
- Unlimited transformations

### OpenRouter
- Pay-per-use
- ~$0.01 per image analysis
- Free tier models available

---

## 🛡️ Security

- ✅ Password hashing
- ✅ Session-based authentication
- ✅ HTTP-only cookies
- ✅ Protected API routes
- ✅ User-scoped data access
- ✅ CORS configuration

---

## 📊 Database Schema

### Users
```sql
- id (PK)
- username (unique)
- email (unique)
- password_hash
- created_at
```

### Journals
```sql
- id (PK)
- user_id (FK → users)
- title
- date, time
- notes
- report (AI-generated)
- image_paths (JSON)
- created_at
```

---

## 🧪 Testing

```bash
# Run locally
cd journal_maker
python journal_app.py

# Test endpoints
curl http://localhost:8000/api/health
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Better password hashing (bcrypt)
- [ ] Email verification
- [ ] Password reset
- [ ] Journal sharing
- [ ] Export to PDF
- [ ] Mobile app

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **Railway** - Easy cloud deployment
- **Cloudinary** - Cloud image management
- **OpenRouter** - Access to 100+ AI models
- **Bootstrap** - UI framework

---

**Built with ❤️ using FastAPI + PostgreSQL + AI**
