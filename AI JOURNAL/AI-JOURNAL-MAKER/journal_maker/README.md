# AI Journal Maker

An AI-powered journal creation system that analyzes uploaded images and generates detailed journal reports.

## Features

- 📸 **Image Upload**: Upload one or multiple images
- 📝 **Metadata Input**: Add Date/Time and Title for each journal entry
- 🤖 **AI Analysis**: AI-powered image analysis generates detailed reports
- 📖 **Journal History**: View and manage past journal entries
- 🎨 **Modern UI**: Clean, responsive interface

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements_journal.txt
```

### Set API Key

```bash
# Set your OpenRouter API key
export OPENROUTER_API_KEY=your-api-key-here
# On Windows: set OPENROUTER_API_KEY=your-api-key-here
```

### Run the Application

```bash
python journal_app.py
```

Open your browser and navigate to `http://localhost:8000`

## Usage

1. **Upload Image**: Click or drag images to the upload area
2. **Add Metadata**: Fill in Date/Time and Title
3. **Generate Report**: Click "Analyze with AI" to generate the journal report
4. **View History**: Browse past journal entries

## Project Structure

```
.
├── journal_app.py              # Main FastAPI application
├── journal_ai.py               # AI analysis logic
├── journal_db.py               # Database operations
├── requirements_journal.txt    # Python dependencies
├── journal_config.json         # Configuration file
├── journal_data/               # Data storage
│   ├── images/                 # Uploaded images
│   └── journals.db             # SQLite database
└── journal_templates/
    └── index.html              # Frontend UI
```

## Configuration

Edit `journal_config.json` to customize:

```json
{
  "llm_provider": "openrouter",
  "model": "openai/gpt-4o",
  "temperature": 0.7,
  "max_tokens": 2048,
  "api_key_env": "OPENROUTER_API_KEY"
}
```

## API Endpoints

- `GET /` - Main UI
- `POST /api/upload` - Upload image
- `POST /api/analyze` - Analyze image with AI
- `GET /api/journals` - Get all journal entries
- `GET /api/journals/{id}` - Get specific journal entry
- `DELETE /api/journals/{id}` - Delete journal entry

## Deployment

See [DEPLOYMENT.md](../DEPLOYMENT.md) in the root directory for Railway deployment instructions.
