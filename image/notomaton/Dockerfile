FROM tmacro/lego as lego
FROM tmacro/wkhtmltopdf:0.12.6 as wkhtmltopdf
FROM python:3.8-alpine3.10

ENV S6_VERSION 1.21.8.0
# Let's encrypt config
ENV LEGO_PROVIDER cloudflare
ENV LEGO_DNS_RESOLVERS 8.8.8.8
ENV LEGO_PATH /lego
ENV LEGO_HOOKS_DIR $LEGO_PATH/hooks
ENV LEGO_KEY_TYPE ec384
ENV LEGO_RENEW_DAYS 30
ENV LEGO_ACME_HOST "https://acme-v02.api.letsencrypt.org/directory"
ENV	LEGO_ACME_STAGING_HOST "https://acme-staging-v02.api.letsencrypt.org/directory"
ENV LEGO_STAGING TRUE
# Notomaton config
ENV NOTOMATON_RUNTIME_ASSET_PATH /usr/local/share/assets/

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-amd64.tar.gz /tmp/
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C / && rm /tmp/s6-overlay-amd64.tar.gz

RUN apk add --update \
      libffi-dev \
      openssl-dev \
      glib \
      libxrender \
      fontconfig \
      freetype \
      libxext \
      libx11 \
      libstdc++ \
      libgcc \
      git \
      libssl1.1 \
      ca-certificates \
      ttf-dejavu \
      ttf-droid \
      ttf-freefont \
      ttf-liberation \
      ttf-ubuntu-font-family \
  && apk add --no-cache --virtual .build-deps \
      msttcorefonts-installer \
  && update-ms-fonts \
  && fc-cache -f \
  && rm -rf /tmp/* \
  && apk del .build-deps

ADD ./requirements.txt /tmp
RUN apk add --update \
        build-base && \
    pip install -r /tmp/requirements.txt && \
    apk del build-base

# Copy over lego binary and scripts
COPY --from=lego /usr/bin/lego /usr/bin/lego
COPY --from=lego /usr/bin/issue-certs /usr/bin/
COPY --from=lego /usr/bin/lego-config /usr/bin/
COPY --from=lego /usr/bin/wait-grep /usr/bin/

RUN mkdir -p $LEGO_HOOKS_DIR

# Copy over the wkhtmltopdf binary
COPY --from=wkhtmltopdf /bin/wkhtmltopdf /bin/wkhtmltopdf

ADD ./s6 /etc

ADD . /usr/local/src/notomaton
ADD docs/ /usr/local/share/docs/

WORKDIR /usr/local/src/notomaton

CMD /init