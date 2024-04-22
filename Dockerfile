# Build stage
FROM python:3.9 as build-stage

WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies (including development dependencies)
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY . .

# Build the application artifacts (if applicable)
RUN ./build.sh

# Production stage
FROM python:3.9-slim as production-stage

WORKDIR /app

# Copy the application artifacts from the build stage
COPY --from=build-stage /app/dist /app/dist
COPY --from=build-stage /app/requirements.txt .

# Install only the runtime dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy any other necessary files
COPY . .

# Set the environment variables and start the application
ENV DJANGO_SUPERUSER_PASSWORD=$MY_DJANGO_SUPERUSER_PASSWORD
CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn flare_watcher.wsgi:application --bind 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-allow-from='*' && python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL"]
# Use Alpine Linux-based image
# FROM python:3.9-alpine as builder

# WORKDIR /app

# RUN apk update && \
#     apk add --no-cache git gcc musl-dev libffi-dev && \
#     apk add --no-cache ffmpeg libsm6 libxext6 libxrender-dev && \
#     python -m venv /opt/venv && \
#     /opt/venv/bin/pip install --upgrade pip


# COPY requirements.txt .
# RUN /opt/venv/bin/pip install -r requirements.txt

# FROM python:3.9-alpine

# WORKDIR /app

# COPY --from=builder /opt/venv /opt/venv
# COPY . .

# ARG ENV_FILE=./.env
# ENV $(cat $ENV_FILE | xargs)
# ENV DJANGO_SUPERUSER_PASSWORD=$MY_DJANGO_SUPERUSER_PASSWORD
# ENV PATH="/opt/venv/bin:$PATH"

# EXPOSE 8000

# CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn flare_watcher.wsgi:application --bind 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-allow-from='*' && python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL"]
