# Instruct what environment to install
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
COPY . code
WORKDIR /code

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# en_IN UTF-8/en_IN UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
ENV LANG en_IN.UTF-8
ENV LC_NUMERIC en_IN.UTF-8

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt