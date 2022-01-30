FROM node:lts-stretch AS build

ENV APP_DIR /home/node/download/frontend
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

COPY ./src/frontend/src .

RUN npm install && npm run build

FROM python:3.10-alpine

# No Version Pining necessary
# hadolint ignore=DL3013
RUN pip3 install --upgrade --no-cache-dir pip

ENV APP_DIR /download/src
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}
RUN mkdir -p ./static/shop

# open port
EXPOSE 5001

COPY . /download
COPY requirements.txt /download/requirements.txt
RUN pip3 install --no-cache-dir -r /download/requirements.txt

COPY --from=build /home/node/download/frontend/docs/* ./static/shop
RUN rm -r ./frontend

CMD [ "python", "./server.py" ]

