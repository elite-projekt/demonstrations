# hadolint ignore=DL3007
from alpine:latest AS builder

# hadolint ignore=DL3018,DL3013,SC1091
RUN apk update --no-cache && apk upgrade --no-cache && apk add --no-cache python3-dev py-pip gcc musl-dev libffi-dev rustup openssl-dev g++ && rustup-init -y && source /root/.cargo/env && pip install --no-cache-dir mitmproxy && pip install --no-cache-dir --no-deps "cryptography>=39" && apk del python3-dev gcc musl-dev openssl-dev g++ rustup && rm -rf /root/.cargo && rm -rf /root/.rustup

EXPOSE 8080 8081

#CMD ["mitmweb", "--web-host", "0.0.0.0", "--modify-body", "/~s/let attacked = false;/let attacked = true;"]
CMD ["mitmweb", "-k", "-v", "--web-host", "0.0.0.0", "--modify-body", "/~s/let attacked = false;/let attacked = true;"]
