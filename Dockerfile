FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y git-lfs && \
    rm -rf /var/lib/apt/lists/*


RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 libxrender-dev libgl1 libgl1-mesa-glx libgl1-mesa-dev libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ARG ENV_FILE=./.env
ENV $(cat $ENV_FILE | xargs)
ENV DJANGO_SUPERUSER_PASSWORD=$MY_DJANGO_SUPERUSER_PASSWORD

CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn flare_watcher.wsgi:application --bind 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-allow-from='*' && python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL"]