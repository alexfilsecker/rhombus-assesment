FROM node:23-alpine

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . . 

RUN rm .env.local
RUN mv .env.production .env