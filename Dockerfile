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
RUN apk add --no-cache gcc musl-dev nano parallel
ENV TZ Australia/Melbourne
RUN apk update
RUN apk add --no-cache ca-certificates
RUN apk add wget curl openssl
RUN rm -rf /var/cache/apk/*

# Make working dir
WORKDIR /usr/src/app
RUN chown -R 1000:1000 /usr/src/app

COPY package.json .
COPY package-lock.json .
RUN npm i -g npm
RUN npm i node-red-contrib-redis
RUN npm install --no-optional

# Patch the ftp.js
#COPY node_modules/node-red-contrib-ftp ./node_modules/node-red-contrib-ftp
# Patch the FTP-Download.js
#COPY node_modules/node-red-contrib-ftp-download/ftp-download.js ./node_modules/node-red-contrib-ftp-download/ftp-download.js

COPY flows.json .
COPY settings.js .
COPY netrc /home/node/.netrc

RUN mkdir /mnt/data_dir
RUN mkdir /mnt/awra_dir
RUN mkdir /mnt/fuel
RUN mkdir /mnt/queries

RUN chown 1000:1000 /mnt/data_dir
RUN chown 1000:1000 /mnt/awra_dir
RUN chown 1000:1000 /mnt/fuel
RUN chown 1000:1000 /mnt/queries
#RUN apk --update add tor torsocks
#RUN sed "1s/^/SocksPort 0.0.0.0:9050\n/" /etc/tor/torrc.sample > /etc/tor/torrc
#RUN tor -f /etc/tor/torrc &

USER 1000

# Production
EXPOSE 9050
EXPOSE 1880/tcp
CMD ["npm", "start"]
