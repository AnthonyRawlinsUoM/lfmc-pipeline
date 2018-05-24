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
RUN npm install --no-optional

COPY . .
RUN mkdir /mnt/data_dir
RUN mkdir /mnt/awra_dir
RUN mkdir /mnt/queries

# Production
EXPOSE 1880/tcp
CMD ["npm", "start"]