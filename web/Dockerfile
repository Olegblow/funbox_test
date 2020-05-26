FROM python:3.7-alpine

COPY ./pytest.ini pytest.ini
COPY ./requirements.txt requirements.txt
COPY ./app /app

RUN apk update \
    && apk add \
      bash \
      build-base \
      curl \
      g++ \
      gcc \
      libxslt-dev \
      gettext \
      git \
      libffi-dev \
      linux-headers \
      postgresql-dev \
      tini \
      jpeg-dev \
      zlib-dev \
      openjpeg-dev && rm -vrf /var/cache/apk/*

RUN pip install -r /requirements.txt

WORKDIR /app
RUN mkdir -p /volumes/web/media
RUN mkdir -p /volumes/web/static

RUN adduser -D user
RUN chown -R user:user /volumes/
RUN chmod -R 755 /volumes/

USER user
