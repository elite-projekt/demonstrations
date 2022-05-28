# hadolint ignore=DL3007
from alpine:latest AS builder

# hadolint ignore=DL3018,DL3013
RUN apk update --no-cache && apk add --no-cache python3-dev py-pip gcc musl-dev libffi-dev rust cargo openssl-dev g++ && pip install --no-cache-dir mitmproxy && apk del python3-dev gcc musl-dev rust cargo openssl-dev g++ && rm -rf /root/.cargo

EXPOSE 8080 8081

#CMD ["mitmweb", "--web-host", "0.0.0.0", "--modify-body", "/~s/let attacked = false;/let attacked = true;"]
CMD ["mitmweb", "-k", "-v", "--web-host", "0.0.0.0", "--modify-body", "/~s/let attacked = false;/let attacked = true;"]
