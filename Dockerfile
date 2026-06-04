# ✅ Base image
FROM python:3.11-slim

# ✅ Set working directory
WORKDIR /app

# ✅ Prevent .pyc files & buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ✅ Install system deps (optional but safe)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy requirements first (better caching)
COPY requirements.txt .

# ✅ Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy project
COPY . .

# ✅ Collect static (if used)
RUN python manage.py collectstatic --noinput || true

# ✅ Run migrations
RUN python manage.py migrate

# ✅ Expose port
EXPOSE 8000

# ✅ Run server
CMD ["gunicorn", "aadukalam.wsgi:application", "--bind", "0.0.0.0:8000"]