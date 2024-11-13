#!/bin/bash

# Make script exit on first error
set -e

echo "Starting FastAPI application..."

# Give the application time to fully start
sleep 5

# Start the FastAPI application
exec uvicorn backend.api:app --host 0.0.0.0 --port ${PORT:-8000} 