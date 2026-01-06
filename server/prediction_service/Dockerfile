FROM python:3.10.8-slim
# FROM python:3.8.12-slim


RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
    apt-get install ffmpeg -y && \
    rm -rf /var/lib/apt/lists/*

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
CMD ["gunicorn", "--workers=1", "--threads=4", "--log-level", "debug", "--bind", "0.0.0.0:8000", "--timeout", "600", "prediction_service_backend.wsgi"]
