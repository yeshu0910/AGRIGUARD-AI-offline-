# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

# =========================
# System dependencies
# =========================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Install Python dependencies
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =========================
# Copy entire project
# (safe for ML + Streamlit)
# =========================
COPY . .

# =========================
# Create required runtime folders
# =========================
RUN mkdir -p /app/AgriGuard/database /app/AgriGuard/models /app/AgriGuard/images /app/AgriGuard/tmp

# =========================
# Environment settings
# =========================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# =========================
# FastAPI port
# =========================
EXPOSE 8000

# =========================
# Run FastAPI app
# =========================
CMD ["uvicorn", "AgriGuard.backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
