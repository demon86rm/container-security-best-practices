# Dockerfile
# Purpose: build the Antora site and serve it from a Red Hat UBI9 httpd image.
# Both bases are pinned by digest (the same supply-chain habit the workshop teaches).
FROM docker.io/antora/antora@sha256:e2c2a3e2ae01f6dcb26ca4c6fe6bc335a06e05d23c976b5730567100d8475ed4 AS builder

ADD . /antora/

RUN antora generate --stacktrace site.yml

FROM registry.access.redhat.com/ubi9/httpd-24@sha256:358efd0640c4ebaa6c027dfb349e7f5fc51aa62698e01ef79f4a4dbbd5cfacdd

COPY --from=builder /antora/gh-pages/ /var/www/html/
