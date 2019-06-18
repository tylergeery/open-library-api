FROM postgres:latest as base



FROM base as dev

COPY ./env/containers/db/seed.sql /docker-entrypoint-initdb.d/seed.sql



FROM base as prod
