# AI Journal Maker - Usage Guide

## Quick Start Guide

### Local Development

```bash
# Install dependencies
pip install -r journal_maker/requirements_journal.txt

# Copy environment file
copy journal_maker\.env.example journal_maker\.env

# Edit .env and add your API keys:
# - OPENROUTER_API_KEY or GOOGLE_API_KEY
# - CLOUDINARY_URL (for production)

# Run the app
cd journal_maker
python journal_app.py
```

Open **http://localhost:8000**

---

## User Guide

### 1. Register Account

1. Go to the app URL
2. Click **Register**
3. Enter username, email, password
4. Click **Register**

### 2. Login

1. Enter your credentials
2. Click **Login**

### 3. Upload Images & Generate Journal

1. Click **Upload Images**
2. Select one or multiple images
3. (Optional) Add notes about your day
4. Click **Analyze & Generate Journal**
5. Wait for AI analysis (10-30 seconds)
6. Review and save your journal entry

### 4. View Journal History

1. Go to **Dashboard**
2. Browse all your journal entries
3. Search by date or keywords
4. Delete entries if needed

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register new user |
| POST | `/api/login` | Login |
| POST | `/api/logout` | Logout |
| GET | `/api/me` | Get current user |

### Journals

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyze` | Upload & analyze images |
| GET | `/api/journals` | Get all journals |
| GET | `/api/journals/{id}` | Get specific journal |
| POST | `/api/journals` | Save journal |
| DELETE | `/api/journals/{id}` | Delete journal |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |

---

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ (Production) |
| `CLOUDINARY_URL` | Cloudinary URL for image storage | ✅ (Production) |
| `OPENROUTER_API_KEY` | OpenRouter API key for AI | ✅ |
| `GOOGLE_API_KEY` | Google Gemini API key (alternative) | Optional |
| `PORT` | Server port | Auto |

### journal_config.json

```json
{
  "llm_provider": "openrouter",
  "model": "google/gemini-2.0-flash-exp:free",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

**Models:**
- `openrouter` - Access to 100+ models (default)
- `google` - Direct Google Gemini API
- `openai` - OpenAI GPT-4 Vision

---

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment guide.

### Quick Deploy

```bash
# Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push

# Deploy on Railway
# 1. Go to railway.app
# 2. New Project → Deploy from GitHub
# 3. Add PostgreSQL database
# 4. Add environment variables
# 5. Auto-deploy!
```

---

## Troubleshooting

### App won't start
```bash
# Check dependencies
pip install -r journal_maker/requirements_journal.txt

# Check environment file
cat journal_maker/.env
```

### Database errors
- Ensure `DATABASE_URL` is set correctly
- For local: uses SQLite by default
- For production: Railway provides PostgreSQL

### Image upload fails
- Check `CLOUDINARY_URL` is set
- Verify Cloudinary quota

### AI analysis fails
- Verify `OPENROUTER_API_KEY` is valid
- Check API credits balance

---

## Tips

1. **Free Models**: Use `google/gemini-2.0-flash-exp:free` on OpenRouter for free AI analysis
2. **Batch Upload**: Upload multiple images at once for comprehensive journal entries
3. **Search**: Use the search feature to find old entries by keywords
4. **Backup**: Export important journals regularly

---

**Happy Journaling! 📝**
