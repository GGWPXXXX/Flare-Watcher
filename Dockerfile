FROM python:3.9

WORKDIR /app

COPY . /app

RUN python -m venv /opt/venv
RUN . /opt/venv/bin/activate
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y ffmpeg libsm6 libxext6 libxrender-dev libgl1 libgl1-mesa-glx libgl1-mesa-dev libglib2.0-0
RUN pip install -r requirements.txt
CMD ["/bin/bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn flare_watcher.wsgi"]