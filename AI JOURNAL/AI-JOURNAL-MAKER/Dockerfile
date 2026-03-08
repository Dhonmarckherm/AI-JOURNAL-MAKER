# Dockerfile for AI Journal Maker
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY journal_maker/requirements_journal.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_journal.txt

# Copy application code
COPY journal_maker/ ./

# Copy templates if needed
COPY journal_templates/ ./journal_templates/

# Create data directory
RUN mkdir -p /app/journal_data/images

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "start.py"]
