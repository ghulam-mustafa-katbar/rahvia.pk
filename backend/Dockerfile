# Multi-stage production Dockerfile for Rahvia Django Backend
FROM python:3.13-slim as builder

WORKDIR /app

# Install system build dependencies for Pillow and psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final minimal runner stage
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed site-packages and binaries directly to system path
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=rahvia_project.settings

EXPOSE 8000

# Shell form permits dynamic resolution of $PORT on Render (default 10000) or local (8000)
# Automatically runs pending migrations and idempotent seed data before starting Gunicorn
CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && python manage.py seed_data && gunicorn rahvia_project.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120"]
