FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-distutils python3-pip && pip install --no-cache-dir setuptools wheel && pip install --no-cache-dir -r requirements.txt


COPY . .

ENV DJANGO_SETTINGS_MODULE=threat_detection.settings

CMD ["sh", "start.sh"]