# Main content from https://www.docker.com/blog/how-to-dockerize-django-app/
# "Official python runtime image"
FROM python:3.12-slim

# Make workdir
RUN mkdir /app
WORKDIR /app

# Pre-sanity checks
RUN python3 --version

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy all into workdir
COPY . /app/

# Expose port and define startup command
# NOTE: The CMD launches a DEV SERVER, so unsuitable for production
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
