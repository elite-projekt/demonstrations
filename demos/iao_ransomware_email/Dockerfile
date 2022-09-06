FROM python:3.10-alpine

# No Version Pining necessary
# hadolint ignore=DL3013
RUN pip3 install --upgrade --no-cache-dir pip

ENV APP_DIR /iao_ransomware_email/src

# app dir
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# expose web server port
EXPOSE 443

COPY . /iao_ransomware_email
COPY requirements.txt /iao_ransomware_email/requirements.txt

RUN pip3 install --no-cache-dir -r /iao_ransomware_email/requirements.txt

# exectute start up script
ENTRYPOINT ["gunicorn", "--certfile=/iao_ransomware_email/src/server.crt", "--keyfile=/iao_ransomware_email/src/server.key", "app:app", "-b", "0.0.0.0:443", "--workers=1"]
