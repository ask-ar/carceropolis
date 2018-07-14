FROM diraol/alpine-py36-pandas-numpy-psql:1.0.1

ENV PYTHONUNBUFFERED 1

RUN set -ex \
    && apk add libstdc++ pcre-dev libuuid \
    && apk --no-cache add --virtual _build_deps \
        build-base \
        libc-dev \
        linux-headers \
        git \
        gcc \
        # Pillow deps
        jpeg-dev \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev \
        harfbuzz-dev \
        fribidi-dev \
    && pip install \
        uwsgi \
        git+https://github.com/stephenmcd/mezzanine.git#egg=Mezzanine \
    && apk del _build_deps \
    && rm -rf \
        ~/.cache/pip \
        /var/cache/apk/*

COPY requirements.txt /tmp/requirements.txt
RUN set -ex \
    && pip install -U pip setuptools wheel \
    && pip install -r /tmp/requirements.txt \
    && rm -rf \
        ~/.cache/pip \
        /var/cache/apk/*

ENV CARCEROPOLIS_HOME=/project/carceropolis
RUN mkdir -p ${CARCEROPOLIS_HOME} /var/log/uwsgi

WORKDIR ${CARCEROPOLIS_HOME}

COPY deploy/entrypoint.sh /usr/bin/entrypoint
ENTRYPOINT ["/usr/bin/entrypoint"]
