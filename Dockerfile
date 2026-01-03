# UHIP - Unified Hybrid Intelligence Platform
# Production Dockerfile

FROM python:3.11-slim

LABEL maintainer="UHIP Development Team <dev@uhip.io>"
LABEL description="Unified Hybrid Intelligence Platform - Production-Ready System"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY uhip/ ./uhip/
COPY setup.py .
COPY README.md .
COPY LICENSE .

# Install UHIP
RUN pip install -e .

# Create logs directory
RUN mkdir -p /app/logs

# Set default environment variables
ENV UHIP_MAX_WORKERS=4 \
    UHIP_LOG_LEVEL=INFO \
    UHIP_AUTO_OPTIMIZE=true

# Expose port for future API extensions
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import uhip; print('OK')" || exit 1

# Default command
CMD ["uhip", "--demo"]
