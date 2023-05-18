FROM python:latest

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD 1

COPY ./src /app

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt