from python:3.7-alpine

RUN apk add python3-dev gcc musl-dev libxml2-dev libxslt-dev postgresql-dev\
    && pip3 install --upgrade pip\
    && pip3 install psycopg2