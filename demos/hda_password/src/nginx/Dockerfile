# hadolint ignore=DL3007
FROM alpine:latest

# hadolint ignore=DL3018
RUN apk update --no-cache && apk add --no-cache nginx

COPY nginx.conf /etc/nginx/http.d/nginx.conf

COPY server.crt /etc/nginx/server.crt
COPY server.key /etc/nginx/server.key

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]