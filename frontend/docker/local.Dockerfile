FROM node:23-alpine

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . . 

RUN rm .env.production
RUN mv .env.local .env