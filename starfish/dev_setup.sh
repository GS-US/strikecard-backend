#!/usr/bin/env bash
set -e

source ./.env

set -x # must come after source to avoid leaking secrets

python manage.py flush --no-input

python manage.py makemigrations

python manage.py migrate

python manage.py loaddata regions/fixtures/regions.json

python manage.py create_state_chapters

python manage.py dev_setup "$@"
