FROM node:18-alpine3.20

WORKDIR /app
COPY package*.json ./
COPY . .

RUN npm install
CMD ["npm", "run", "dev"]
