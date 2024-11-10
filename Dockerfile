# Use an official Node.js runtime as the base image
FROM node:18 as frontend

# Set working directory for frontend
WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build frontend
RUN npm run build

# Use Python image for the backend
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p math_docs math_tutor_db

# Copy Python requirements
COPY backend/requirements.txt ./backend/

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install -r backend/requirements.txt

# Copy backend source and math docs
COPY backend/ ./backend/
COPY math_docs/. ./math_docs/

# Copy built frontend from previous stage
COPY --from=frontend /app/.next ./frontend/.next

# Set environment variables
ENV PORT=8000
ENV PYTHONPATH=/app/backend

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "cd backend && uvicorn api:app --host 0.0.0.0 --port $PORT"]