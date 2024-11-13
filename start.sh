#!/bin/bash

# Make script exit on first error
set -e

echo "Starting FastAPI application..."

# Start the FastAPI application
if [ "$RAILWAY_ENVIRONMENT" = "production" ]; then
    # Production mode
    exec uvicorn backend.api:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4
else
    # Development mode
    exec uvicorn backend.api:app --host 0.0.0.0 --port ${PORT:-8000} --reload
fi 