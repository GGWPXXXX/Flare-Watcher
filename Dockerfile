FROM python:3.9

WORKDIR /app
COPY . /app
COPY prediction/model/random_forest_model.pkl /app/prediction/model/
COPY prediction/model/yolo_object_detection.pt /app/prediction/model/

RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 libxrender-dev libgl1 libgl1-mesa-glx libgl1-mesa-dev libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Create a new superuser
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=changeme

RUN python manage.py migrate && \
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | python manage.py shell && \
    python manage.py collectstatic --noinput

CMD ["bash", "-c", "gunicorn flare_watcher.wsgi:application --bind 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-allow-from='*'"]