# build stage
FROM node:lts as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install --no-package-lock
COPY . .
RUN npm run build

# production stage
FROM node:lts as production-stage
RUN npm install serve -g
COPY --from=build-stage /app/dist /var/www/html
EXPOSE 80
CMD ["serve", "-s", "/var/www/html", "-p", "80"]
