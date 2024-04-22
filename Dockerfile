# Use Alpine Linux-based image
FROM python:3.9-alpine as builder

WORKDIR /app

# Install virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-alpine

WORKDIR /app

# Copy virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Set environment variables
ARG ENV_FILE=./.env
ENV $(cat $ENV_FILE | xargs)
ENV DJANGO_SUPERUSER_PASSWORD=$MY_DJANGO_SUPERUSER_PASSWORD

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn flare_watcher.wsgi:application --bind 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-allow-from='*' && python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL"]