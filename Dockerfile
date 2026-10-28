# ==========================================
# STAGE 1: The Builder Environment
# ==========================================
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system build dependencies required for compiling certain Python wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into a localized virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ==========================================
# STAGE 2: The Final Runtime Environment
# ==========================================
FROM python:3.11-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Make sure the final container uses the virtual environment's binaries
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy the pre-compiled virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the actual application source code
COPY . .

# Create a non-privileged user for security compliance
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
