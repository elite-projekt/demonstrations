# hadolint ignore=DL3007
from alpine:latest

# hadolint ignore=DL3018
RUN apk update --no-cache && apk add --no-cache nginx gettext && apk upgrade --no-cache

COPY nginx.conf.tmpl /etc/nginx/nginx.conf.tmpl
COPY html/ /var/lib/nginx/html/

COPY nimbus.crt /etc/nginx/nimbus.crt
COPY nimbus.key /etc/nginx/nimbus.key

EXPOSE 80 443
CMD ["sh","-c","ELITE_LANG=${ELITE_LANG:-de} envsubst < /etc/nginx/nginx.conf.tmpl > /etc/nginx/nginx.conf && nginx"]
