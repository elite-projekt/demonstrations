# hadolint ignore=DL3007
from alpine:latest

# hadolint ignore=DL3018
RUN apk update --no-cache && apk upgrade --no-cache && apk add --no-cache nginx gettext

COPY nginx.conf /etc/nginx/nginx.conf
COPY a.py /var/lib/nginx/html/a.py

EXPOSE 80 443
CMD ["nginx"]
