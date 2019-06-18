#!/bin/bash
exec gunicorn wsgi \
    --bind 127.0.0.1:8080 \
    --workers 2 \
    --log-level info \
    --timeout 600 \
    --preload \
"$@"