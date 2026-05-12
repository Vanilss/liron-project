# Build stage
FROM python:3.11-slim as builder

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Optimize pip installation with cache mount
# This requires BuildKit (default in modern Docker)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy only the necessary files from the builder
COPY --from=builder /root/.local /root/.local
# Copy application code
COPY . .

# Update PATH to include user-installed binaries
ENV PATH=/root/.local/bin:$PATH

# Streamlit configurations
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8501

# Healthcheck using python's built-in urllib
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "main.py"]

