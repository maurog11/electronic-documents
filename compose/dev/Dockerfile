FROM python:3.7.9-alpine3.13

LABEL maintainer="lmelo@softpymes.com.co"

RUN apk update && apk upgrade \ 
  && apk add supervisor nginx tzdata bash

ADD ./requirements.txt /app/requirements.txt

ADD ./compose/dev/default.conf /etc/nginx/conf.d

RUN adduser -S electronic -G nginx 

RUN mkdir -p /etc/supervisor/conf.d/ && \
  mkdir -p /var/log/supervisor/

ADD ./compose/dev/supervisord.conf /etc/

ADD ./compose/dev/electronic_dcto.conf /etc/supervisor/conf.d/

ADD ./compose/dev/start_nginx.conf /etc/supervisor/conf.d/

WORKDIR /app

COPY ./src .

RUN mkdir -p /run/nginx/ && \
  chown -R electronic:nginx /app &&\
  chown -R nginx:nginx /var/log/nginx/ &&\
  chown -R nginx:nginx /var/lib/nginx/ &&\
  chown -R nginx:nginx /var/run/nginx/

RUN apk add gcc build-base libffi-dev

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

ADD ./compose/dev/entrypoint /entrypoint
RUN chmod +x /entrypoint

#ADD ./compose/dev/start-app /start
#RUN chmod +x /start

ENTRYPOINT ["/entrypoint"]

#CMD ["/start"]

RUN sed -i 's/client_max_body_size 1m;/client_max_body_size 100m;/g' /etc/nginx/nginx.conf

EXPOSE 5000
CMD supervisord -c /etc/supervisord.conf

