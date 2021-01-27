FROM python:3.8-alpine3.11

RUN apk add --no-cache docker \
    && pip3 install --upgrade pip

ENV APP_DIR /phishing/app

# app dir
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# expose web server port
EXPOSE 4000

COPY . /phishing
COPY requirements.txt /phishing/requirements.txt

RUN pip3 install -r /phishing/requirements.txt

# exectute start up script
ENTRYPOINT ["gunicorn", "app:app", "-b", "0.0.0.0:4000", "--workers=1"]

