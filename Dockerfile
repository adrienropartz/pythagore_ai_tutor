# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
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

# Set the working directory to where your main application is
WORKDIR /app/backend

# Command to run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]