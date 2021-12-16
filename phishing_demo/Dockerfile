FROM python:3.10-alpine

RUN pip3 install --upgrade pip

ENV APP_DIR /phishing/app

# app dir
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# expose web server port
EXPOSE 443

COPY . /phishing
COPY requirements.txt /phishing/requirements.txt

RUN pip3 install -r /phishing/requirements.txt

# exectute start up script
ENTRYPOINT ["gunicorn", "--certfile=/phishing/app/server.crt", "--keyfile=/phishing/app/server.key", "app:app", "-b", "0.0.0.0:443", "--workers=1"]
