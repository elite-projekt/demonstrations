FROM python:3.10-alpine

# No Version Pining necessary
# hadolint ignore=DL3013
RUN pip3 install --upgrade --no-cache-dir pip

ENV APP_DIR /fokusrnware/src

# app dir
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# Temporary security fix see #131
RUN apk add --no-cache --upgrade libretls=3.3.4-r3

# expose web server port
EXPOSE 443

COPY . /fokusrnware
COPY requirements.txt /fokusrnware/requirements.txt

RUN pip3 install --no-cache-dir -r /fokusrnware/requirements.txt

# exectute start up script
ENTRYPOINT ["gunicorn", "--certfile=/fokusrnware/src/server.crt", "--keyfile=/fokusrnware/src/server.key", "app:app", "-b", "0.0.0.0:443", "--workers=1"]
