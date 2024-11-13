# Use Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install only required system dependencies
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
COPY start.sh .
RUN chmod +x start.sh

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Health check with appropriate timing
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Run the application
CMD ["./start.sh"]

#test