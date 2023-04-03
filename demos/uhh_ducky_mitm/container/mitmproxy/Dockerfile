# hadolint ignore=DL3006
from debian

# hadolint ignore=DL3008,DL3013
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir mitmproxy && pip install --no-cache-dir --no-deps "cryptography>=39"

EXPOSE 8080 8081

#CMD ["mitmweb", "--web-host", "0.0.0.0", "--modify-body", "/~s/let attacked = false;/let attacked = true;"]
CMD ["mitmweb", "-k", "-v", "--web-host", "0.0.0.0", "--modify-body", "/~s/let attacked = false;/let attacked = true;"]
