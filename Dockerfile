# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

WORKDIR /app
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

