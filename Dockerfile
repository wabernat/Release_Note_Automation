FROM aantonw/alpine-wkhtmltopdf-patched-qt as wkhtmltopdf
# FROM surnet/alpine-wkhtmltopdf:3.9-0.12.5-full as wkhtmltopdf
FROM python:3.7-alpine

ENV S6_VERSION 1.21.8.0

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-amd64.tar.gz /tmp/
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C / && rm /tmp/s6-overlay-amd64.tar.gz

ADD ./requirements.txt /tmp
RUN apk add --update \
        build-base \
        libffi-dev \
        openssl-dev \
        glib \
        libxrender \
        fontconfig \
        freetype \
        libxext \
        libx11 \
        libstdc++ \
        libgcc && \
    pip install -r /tmp/requirements.txt && \
    apk del build-base

# Copy over the wkhtmltopdf binaries and libs
COPY --from=wkhtmltopdf /bin/wkhtmltopdf /bin/wkhtmltopdf
COPY --from=wkhtmltopdf /bin/wkhtmltoimage /bin/wkhtmltoimage
COPY --from=wkhtmltopdf /lib/libwkhtmltox* /lib/

ADD . /usr/local/src/notomaton
WORKDIR /usr/local/src/notomaton
RUN python setup.py install

# CMD /init
CMD FLASK_APP=notomaton/app.py flask run --reload --host 0.0.0.0
