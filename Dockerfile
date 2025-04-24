FROM python:3.11-slim

# Install build tools
RUN apt-get update && apt-get install -y \
    gcc \
    libdbus-1-dev \
    libdbus-glib-1-dev \
    python3-dev \
    build-essential \
    && apt-get clean

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
