FROM python:3.10-alpine

# No Version Pining necessary
# hadolint ignore=DL3013
RUN pip3 install --upgrade --no-cache-dir pip

ENV APP_DIR /ransomware/src

# app dir
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# expose web server port
EXPOSE 443

COPY . /ransomware
COPY requirements.txt /ransomware/requirements.txt

RUN pip3 install --no-cache-dir -r /ransomware/requirements.txt

# exectute start up script
ENTRYPOINT ["gunicorn", "--certfile=/ransomware/src/server.crt", "--keyfile=/ransomware/src/server.key", "app:app", "-b", "0.0.0.0:443", "--workers=1"]
