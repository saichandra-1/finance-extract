# Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# copy requirements
COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git wget curl libsndfile1 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# install a small spacy model
RUN python -m spacy download en_core_web_sm

# copy app
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
