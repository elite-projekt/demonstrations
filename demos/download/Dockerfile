FROM python:3.8-alpine

# No Version Pining necessary
# hadolint ignore=DL3013
RUN pip3 install --upgrade --no-cache-dir pip

ENV APP_DIR /download/src

# app dir
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

#RUN apk update \
#    && apk add --virtual build-deps gcc python3-dev musl-dev \
#    && apk add jpeg-dev zlib-dev libjpeg\
#    && pip install Pillow

# open port
EXPOSE 5002

COPY . /download
COPY requirements.txt /download/requirements.txt
RUN pip3 install --no-cache-dir -r /download/requirements.txt
CMD [ "python", "./server.py" ]

