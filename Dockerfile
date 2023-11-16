# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code


COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

EXPOSE 8000

CMD ["python","manage.py","runserver"]

