FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN set -ex \
    && apt update \
    && apt upgrade -yqq --no-install-recommends \
    && pip install -U pip setuptools wheel \
    && pip install \
        ipython \
        numpy \
        pandas \
        psycopg2-binary \
        uwsgi \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base \
        ~/.cache/pip

ADD requirements.txt /
RUN set -ex \
    && apt update \
    && apt upgrade -yqq --no-install-recommends \
    && apt install git -yqq --no-install-recommends \
    && pip install -U pip setuptools wheel \
    && pip install -r requirements.txt \
    && apt-get purge --auto-remove -yqq git \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base \
        ~/.cache/pip

RUN mkdir /project
ADD carceropolis /project
ENV PYTHONPATH /project
WORKDIR /project
