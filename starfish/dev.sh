#!/usr/bin/env bash
set -e
set -x

python manage.py flush --no-input

python manage.py makemigrations

python manage.py migrate

python manage.py loaddata regions/fixtures/regions.json

python manage.py create_state_chapters

python manage.py dev_setup

python manage.py runserver 0.0.0.0:8000
