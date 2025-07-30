FROM python:3.9-slim

# Update OS packages to latest patched versions
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY ../requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn server
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
