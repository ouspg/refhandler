# Build and compile the frontend
FROM node:24 AS build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

RUN npm run build


# Setup nginx proxy
FROM nginx:1

COPY --from=build-stage /app/dist/ /usr/share/nginx/html

# Generate self-signed cert for HTTPS
RUN apt-get update && apt-get install -y openssl
RUN openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
RUN openssl rsa -passin pass:x -in server.pass.key -out server.key && rm server.pass.key
RUN openssl req -new -key server.key -out server.csr \
    -subj "/C=FI/L=Oulu/O=Refhandler/OU=INFRA/CN=refhandler.fi"
RUN openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

# Move and rename generated key and cert
RUN mkdir -p /etc/nginx/certs
RUN mv server.key /etc/nginx/certs/selfsigned.key
RUN mv server.crt /etc/nginx/certs/selfsigned.crt

# Nginx uses envsub to inject env variables into the template and copy it to /etc/nginx/conf.d
COPY ./nginx.conf /etc/nginx/templates/nginx.conf.template