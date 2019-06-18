FROM python:3.7-slim-stretch as base

# 
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
       g++ libpq-dev \
    && rm -f /var/cache/apk/* /tmp/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .
COPY library library

RUN pip install -r requirements.txt

RUN python /usr/src/app/library/manage.py collectstatic --noinput

RUN useradd -ms /bin/bash librarian
USER librarian

ENV PYTHONUNBUFFERED 1



FROM base as dev

COPY requirements-dev.txt .
COPY entrypoint.dev.sh .

USER root
RUN pip install -r requirements-dev.txt

CMD ["sh", "./entrypoint.dev.sh"]



FROM base as prod

COPY entrypoint.sh ./library/
COPY wsgi.py ./library/

WORKDIR /usr/src/app/library/

CMD ["sh", "./entrypoint.sh"]
