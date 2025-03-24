# Dockerfile - AI Finance Assistant
FROM python:3.10-slim-buster AS builder

# ---- System Dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    awscli \
    && rm -rf /var/lib/apt/lists/*

# ---- Environment Setup ----
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /app

# ---- Dependency Installation ----
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Application Code ----
FROM python:3.10-slim-buster AS runtime
COPY --from=builder /opt/venv /opt/venv

# Runtime Environment
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    AWS_EC2_METADATA_DISABLED=true \
    PYTHONPATH=/app

# Security: Non-root user
RUN useradd -m -u 1001 appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app
USER appuser
WORKDIR /app

# Application Files
COPY --chown=appuser:appuser . .

# ---- Runtime Configuration ----
EXPOSE 5000  # For FastAPI/Flask apps
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:5000/health || exit 1

# Entrypoint (customize based on your app)
CMD ["python", "script/main.py"]
