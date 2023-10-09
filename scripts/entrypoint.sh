#!/bin/bash
# Entrypoint for the app container in production
set -e 

python3 /app/adrianolczak/manage.py check --deploy
python3 /app/adrianolczak/manage.py collectstatic --noinput
python3 /app/adrianolczak/manage.py migrate

exec "$@"
