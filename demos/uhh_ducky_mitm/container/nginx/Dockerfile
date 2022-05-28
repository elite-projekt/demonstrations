# hadolint ignore=DL3007
from alpine:latest

# hadolint ignore=DL3018
RUN apk update --no-cache && apk add --no-cache nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY html/* /var/lib/nginx/html/
COPY a.py /var/lib/nginx/html/a.py

COPY elite.pem /etc/nginx/elite.pem
COPY elite.key /etc/nginx/elite.key

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
