FROM python:3.9.1-buster

ENV PYTHONBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
