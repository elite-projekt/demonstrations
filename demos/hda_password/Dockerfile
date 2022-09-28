FROM python:3.10-alpine

RUN apk --no-cache update && apk --no-cache upgrade

# No Version Pining necessary
# hadolint ignore=DL3013
RUN pip3 install --upgrade --no-cache-dir pip

ENV APP_DIR /password/src

ARG ELITE_LANG

RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# No Version Pining necessary
# hadolint ignore=DL3013,DL3018
RUN apk --no-cache update\
    && apk --no-cache add --virtual build-deps gcc python3-dev musl-dev \
    && apk --no-cache add jpeg-dev zlib-dev libjpeg\
    && pip install --no-cache-dir Pillow

COPY . /password
COPY requirements.txt /password/requirements.txt
RUN pip3 install --no-cache-dir -r /password/requirements.txt
CMD [ "sh", "-c", "python ./server.py ${ELITE_LANG:-de}"]
