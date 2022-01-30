FROM python:3.8-alpine

RUN pip3 install --upgrade pip

ENV APP_DIR /password/src

# app dir
RUN mkdir -p ${APP_DIR}


RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg\
    && pip install Pillow

COPY requirements.txt /password
RUN pip3 install -r /password/requirements.txt

