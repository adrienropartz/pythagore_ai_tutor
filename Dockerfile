# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy Python requirements
COPY backend/requirements.txt ./backend/

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install -r backend/requirements.txt

# Copy backend source and math docs
COPY backend/ ./backend/
COPY math_docs/. ./math_docs/

# Keep WORKDIR as /app (not /app/backend)
# WORKDIR /app/backend  <- Remove or comment this line

# Set PYTHONPATH to include /app
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Make sure uvicorn is in PATH
ENV PATH="/usr/local/bin:${PATH}"

# Command to run the application
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]