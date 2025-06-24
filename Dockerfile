# Use Debian-based Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build tools and xmlsec dependencies
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    pkg-config \
    python3-dev \
    gcc \
    libxml2 \
    libxmlsec1 \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip \
 && pip install --no-cache-dir lxml==4.9.3 \
 && pip install --no-cache-dir xmlsec \
 && pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]


