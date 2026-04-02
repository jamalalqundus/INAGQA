# develop stage
FROM node:lts-slim AS develop-stage
WORKDIR /app

#install dockerize:
ENV DOCKERIZE_VERSION v0.6.1
RUN apt-get update && apt-get install -y wget && \
    wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# install highcharts 
COPY package*.json ./
RUN npm ci
RUN npm i --save angular-highcharts highcharts 
COPY . .
CMD dockerize -template ./src/assets/config.template.json:./src/assets/config.json npm run start


# production stage
FROM develop-stage AS builder
WORKDIR /app
COPY . .
RUN npm run build -- --prod

FROM nginx:alpine AS production-stage
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist/frontend /usr/share/nginx/html/

#install dockerize:
ENV DOCKERIZE_VERSION v0.6.1
RUN apk add --no-cache openssl && \
    wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz


#make openshifty:
RUN chgrp -R 0 /var/cache/nginx /run /var/log/nginx /usr/share/nginx/html && \
    chmod -R g=u /var/cache/nginx /run /var/log/nginx /usr/share/nginx/html
USER 1000
EXPOSE 8080

CMD ["dockerize", "-template","/usr/share/nginx/html/assets/config.template.json:/usr/share/nginx/html/assets/config.json","nginx","-g","daemon off;"]
