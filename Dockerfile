# Use Python slim image
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages in stages
COPY backend/requirements-base.txt backend/requirements-ml.txt ./backend/

# Install base requirements first
RUN pip install --no-cache-dir -r backend/requirements-base.txt

# Install ML requirements with increased timeout
RUN pip install --no-cache-dir --timeout 300 -r backend/requirements-ml.txt

# Copy application code
COPY backend/ ./backend/
COPY math_docs/ ./math_docs/

# Set environment variables
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Run with 2 workers instead of 4 to reduce memory usage
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]