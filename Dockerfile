# Use Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install only required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories first
RUN mkdir -p /app/db /app/math_docs

# Copy and install requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend ./backend

# Copy empty directories (without trying to handle missing files)
COPY math_docs math_docs/
COPY db db/

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Run the application
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]

#test