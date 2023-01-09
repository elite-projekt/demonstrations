# hadolint ignore=DL3007
from alpine:latest

# hadolint ignore=DL3018
RUN apk update --no-cache && apk upgrade --no-cache && apk add --no-cache nginx gettext

COPY nginx.conf.tmpl /etc/nginx/nginx.conf.tmpl
COPY html/* /var/lib/nginx/html/
COPY a.py /var/lib/nginx/html/a.py

COPY elite.pem /etc/nginx/elite.pem
COPY elite.key /etc/nginx/elite.key

EXPOSE 80 443
CMD ["sh","-c","ELITE_LANG=${ELITE_LANG:-de} envsubst < /etc/nginx/nginx.conf.tmpl > /etc/nginx/nginx.conf && nginx"]
