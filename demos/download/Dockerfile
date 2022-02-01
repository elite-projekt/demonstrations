FROM node:lts-stretch AS build

ENV APP_DIR /home/node/download/frontend
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

COPY ./src/frontend/src .

RUN npm install && npm run build

FROM python:3.10-alpine

ENV APP_DIR /download/src
RUN mkdir -p ${APP_DIR} && mkdir -p ${APP_DIR}/static/shop
WORKDIR ${APP_DIR}

# open port
EXPOSE 5001

COPY ./src/server.py /download/src/
COPY requirements.txt /download/requirements.txt
RUN pip3 install --no-cache-dir -r /download/requirements.txt

COPY --from=build /home/node/download/frontend/docs/ ${APP_DIR}/static/shop/

CMD [ "python", "./server.py" ]
