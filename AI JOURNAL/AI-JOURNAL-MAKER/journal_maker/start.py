#!/usr/bin/env python3
"""
Startup script with error handling for Railway deployment
"""
import os
import sys

print("=== AI Journal Maker Starting ===", flush=True)
print(f"Python version: {sys.version}", flush=True)
print(f"Working directory: {os.getcwd()}", flush=True)

# Check required environment variables
required_vars = ["OPENROUTER_API_KEY"]
optional_vars = ["DATABASE_URL", "CLOUDINARY_URL"]

print("\n=== Environment Variables ===", flush=True)
for var in required_vars:
    value = os.getenv(var)
    status = "✓ SET" if value else "✗ MISSING"
    print(f"{var}: {status}", flush=True)

for var in optional_vars:
    value = os.getenv(var)
    status = f"✓ SET ({value[:20]}...)" if value else "✗ NOT SET (using local)"
    print(f"{var}: {status}", flush=True)

# Get port - Railway sets PORT env var
port = int(os.getenv("PORT", "8000"))
print(f"\n=== Starting Server on port {port} ===", flush=True)

import uvicorn

uvicorn.run(
    "journal_app:app",
    host="0.0.0.0",
    port=port,
    log_level="info"
)
