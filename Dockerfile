FROM python:3.12-slim AS builder

RUN apt-get update & apt-get install --fix-missing --no-install-recommends -y \
    build-essential \ 
    libpq-dev \ 
    default-libmysqlclient-dev \
    pkg-config \ 
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheel -r requirements.txt


