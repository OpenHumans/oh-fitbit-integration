FROM python:3.6-slim-buster

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=false \
    PIP_DISABLE_PIP_VERSION_CHECK=false

RUN apt update \
 && apt install --assume-yes --no-install-recommends \
    libpq-dev

RUN pip install --upgrade pipenv

WORKDIR /app

COPY ./Pipfile /app
COPY ./Pipfile.lock /app

RUN pipenv install --system

COPY . /app
