FROM node:alpine
MAINTAINER Anthony Rawlins <anthony.rawlins@unimelb.edu.au>

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
	mongodb \
	curl \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

# RUN curl 'https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh'
# RUN bash Anaconda3-5.0.1-Linux-x86_64.sh

# Make working dir
WORKDIR /usr/src/app

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

# Production
EXPOSE 1880
CMD ["npm", "start"]

EXPOSE 5000
CMD ["./fuel_moisture.py", "-p=5000"]

# Deployment
# EXPOSE 3000
# CMD ["node", "app.js"]
