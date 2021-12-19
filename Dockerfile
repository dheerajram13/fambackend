FROM python:3.8-slim-buster

COPY youtube/requirements.txt /app/

WORKDIR /app/

RUN pip3 install -r requirements.txt

COPY  youtube /app/

