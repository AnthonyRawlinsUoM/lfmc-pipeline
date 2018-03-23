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
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

# Make working dir
WORKDIR /usr/src/app

COPY package.json .
COPY package-lock.json .
RUN npm i -g npm
RUN npm install --no-optional

COPY . .
RUN mkdir /mnt/data_dir
VOLUME /mnt/data_dir

# Production
EXPOSE 1880/tcp
CMD ["npm", "start"]