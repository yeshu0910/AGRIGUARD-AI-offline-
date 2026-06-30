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
# Create required runtime folders (safe fallback)
# =========================
RUN mkdir -p /app/database /app/models /app/tmp

# =========================
# Environment settings
# =========================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# =========================
# Streamlit port
# =========================
EXPOSE 8501

# =========================
# Run Streamlit app
# (update path if needed)
# =========================
CMD ["streamlit", "run", "ml_pipeline/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
