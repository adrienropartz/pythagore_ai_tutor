#!/bin/bash

# Make script exit on first error
set -e

# Print commands before executing
set -x

# Check if we're running in production (Railway sets this)
if [ "$RAILWAY_ENVIRONMENT" = "production" ]; then
    echo "Starting application in production mode..."
    
    # Start the FastAPI application with multiple workers for production
    echo "Starting FastAPI application..."
    uvicorn backend.api:app --host 0.0.0.0 --port $PORT --workers 4

else
    echo "Starting application in development mode..."
    
    # Start the FastAPI application in development mode with hot reload
    echo "Starting FastAPI application in development mode..."
    uvicorn backend.api:app --host 0.0.0.0 --port ${PORT:-8000} --reload
fi 