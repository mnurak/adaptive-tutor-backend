# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Set environment variables using the modern key=value format
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Add Hugging Face cache directory to environment
ENV HF_HOME=/usr/src/app/huggingface_cache

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- PRE-DOWNLOAD THE ML MODEL ---
# This step caches the model inside the image for instant startup.
COPY download_model.py .
RUN python download_model.py

# Copy the application code into the container
COPY ./app /usr/src/app/app

# --- FINAL FIX ---
# Increase the worker timeout to 120 seconds to allow for AI processing.
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--timeout", "120", "-b", "0.0.0.0:8000", "app.main:app"]