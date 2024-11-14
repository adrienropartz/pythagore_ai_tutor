# Use Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /app/db /app/math_docs

# Copy and install requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend ./backend
COPY math_docs math_docs/
COPY db db/

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Healthcheck configuration
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application directly (no need for start.sh)
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]

#test