FROM python:3.9.12-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
COPY . /app
WORKDIR /app

VOLUME /app/app_env
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y
RUN apt-get install -y tzdata

ENTRYPOINT python main.py