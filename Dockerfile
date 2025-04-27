FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    apt-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app/videoflix_api

CMD ["gunicorn", "videoflix_api.wsgi:application", "--bind", "0.0.0.0:8000"]
