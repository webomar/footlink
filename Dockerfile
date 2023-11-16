# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install "gunicorn==20.0.4"

COPY . .

WORKDIR /app
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

