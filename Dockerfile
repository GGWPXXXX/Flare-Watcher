FROM python:3.9

WORKDIR /app

COPY . /app
COPY prediction/model/random_forest_model.pkl /app/prediction/model/
RUN wget https://media.githubusercontent.com/media/GGWPXXXX/Flare-Watcher/main/best.pt -O /app/prediction/model/yolo_object_detection.pt

RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 libxrender-dev libgl1 libgl1-mesa-glx libgl1-mesa-dev libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# load environment variables from .env file
ARG ENV_FILE=./.env
ENV $(cat $ENV_FILE | xargs)


CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn flare_watcher.wsgi:application --bind 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-allow-from='*' && python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL"]

