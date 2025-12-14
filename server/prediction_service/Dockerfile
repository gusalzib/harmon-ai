FROM python:3.9.6-slim
# FROM python:3.8.12-slim


RUN mkdir /app
WORKDIR /app

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
