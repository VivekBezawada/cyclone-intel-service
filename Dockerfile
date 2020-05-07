from python:3.7-alpine

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip