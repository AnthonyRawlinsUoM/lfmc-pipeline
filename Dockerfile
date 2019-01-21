FROM node:alpine
MAINTAINER Anthony Rawlins <anthony.rawlins@unimelb.edu.au>
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
	mongodb \
    git \
	curl \
  && pip install virtualenv
RUN apk add --no-cache tzdata
RUN apk add --no-cache gcc musl-dev
ENV TZ Australia/Melbourne
RUN rm -rf /var/cache/apk/*

# Make working dir
WORKDIR /usr/src/app

COPY package.json .
COPY package-lock.json .
RUN npm i -g npm
RUN npm i node-red-contrib-redis
RUN npm install --no-optional

# Patch the ftp.js
COPY node_modules/node-red-contrib-ftp ./node_modules/node-red-contrib-ftp
# Patch the FTP-Download.js
COPY node_modules/node-red-contrib-ftp-download/ftp-download.js ./node_modules/node-red-contrib-ftp-download/ftp-download.js

COPY flows.json .
COPY settings.js .

RUN mkdir /mnt/data_dir
RUN mkdir /mnt/awra_dir
RUN mkdir /mnt/queries

RUN addgroup -g 1024 dockerdata
RUN adduser -D -g dockerdata dockeruser 

RUN chown :dockerdata /mnt/data_dir
RUN chown :dockerdata /mnt/awra_dir
RUN chown :dockerdata /mnt/queries
RUN chown -R dockeruser:dockerdata /usr/src/app
USER dockeruser

# Production
EXPOSE 1880/tcp
CMD ["npm", "start"]