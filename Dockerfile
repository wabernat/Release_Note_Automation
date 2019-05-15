FROM python:3.7-alpine

ENV S6_VERSION 1.21.8.0

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-amd64.tar.gz /tmp/
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C / && rm /tmp/s6-overlay-amd64.tar.gz

ADD . /app

CMD /init
