#!/bin/bash

echo "RUN Entrypoint...  :D "

python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

exec "$@"