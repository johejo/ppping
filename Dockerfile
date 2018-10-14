FROM python:3.7-alpine3.8
LABEL maintainer="mitsuo_h@outlook.com"

RUN set -ex && \
    apk add --no-cache curl iputils
COPY standalone/ppping /
ENTRYPOINT ["/ppping"]
CMD ["--help"]
