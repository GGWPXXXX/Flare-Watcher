

#Use Alpine Linux-based image
FROM python:3.9-alpine as builder

WORKDIR /app

COPY requirements.txt .
RUN /opt/venv/bin/pip install -r requirements.txt

FROM python:3.9-alpine

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY . .

ARG ENV_FILE=./.env
ENV $(cat $ENV_FILE | xargs)
ENV DJANGO_SUPERUSER_PASSWORD=$MY_DJANGO_SUPERUSER_PASSWORD
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn flare_watcher.wsgi:application --bind 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-allow-from='*' && python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL"]
