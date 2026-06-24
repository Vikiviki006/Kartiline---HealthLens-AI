# ── Build stage ────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt


# ── Runtime stage ──────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL maintainer="HealthLens AI Team"
LABEL version="1.0.0"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r healthlens && useradd -r -g healthlens healthlens

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/healthlens/.local

# Copy application code
COPY . .

# Ensure uploads directory exists and is writable
RUN mkdir -p uploads logs && \
    chown -R healthlens:healthlens /app

USER healthlens

ENV PATH="/home/healthlens/.local/bin:$PATH"
ENV PYTHONPATH="/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/api/v1/health/ping').raise_for_status()"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
