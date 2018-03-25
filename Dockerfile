FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /project
ADD . /project/
WORKDIR /project
RUN set -ex \
    && apt update \
    && apt upgrade -yqq --no-install-recommends \
    && apt install git git-core -yqq --no-install-recommends \
    && pip install -U pip setuptools wheel \
    && pip install uwsgi -r requirements.txt \
    && apt-get purge --auto-remove -yqq git git-core \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base \
    && export PYTHONPATH=/project
