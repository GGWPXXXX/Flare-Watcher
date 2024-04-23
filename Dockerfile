FROM python:3.9-slim

#VOLUME /root/.cache/pip

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 libxrender-dev libgl1&& \
    rm -rf /var/lib/apt/lists/* && \
    python -m venv /opt/venv
    
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
    #pip install --cache-dir=/root/.cache/pip -r requirements.txt

ARG ENV_FILE=./.env
ENV $(cat $ENV_FILE | xargs)
ENV DJANGO_SUPERUSER_PASSWORD=$MY_DJANGO_SUPERUSER_PASSWORD

CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn flare_watcher.wsgi:application --bind 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-allow-from='*' && python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL"]