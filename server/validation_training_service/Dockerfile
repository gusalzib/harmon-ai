# Use an official Python runtime as a parent image
# Python 3.10 is generally stable for TensorFlow and TFMA
FROM python:3.10-slim


# Set work directory
WORKDIR /app

# Install system dependencies
# build-essential is often needed for compiling Python packages (like numpy/pandas extensions)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Add env
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/HarmonAi_storage.json

# Expose port 8000
EXPOSE 8000

CMD ["gunicorn", "--log-level", "debug", "--bind", "0.0.0.0:8000", "--timeout", "600", "validation_training_backend.wsgi"]
