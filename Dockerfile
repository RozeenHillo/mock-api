# Use a small official Python base image (Linux)
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install minimal OS dependencies (keep image small)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Create a non-root user for better security
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy dependency file first (better Docker layer caching)
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY . /app

# Switch to non-root user
USER appuser

# Expose service port
EXPOSE 8000

# Start the API server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
