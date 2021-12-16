# build stage
FROM node:lts as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM node:lts as production-stage

# No Version Pining necessary
# hadolint ignore=DL3016
RUN npm install serve -g
COPY --from=build-stage /app/dist /var/www/html
EXPOSE 80
CMD ["serve", "-s", "/var/www/html", "-p", "80"]
