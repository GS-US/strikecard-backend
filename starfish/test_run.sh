#!/usr/bin/env bash

echo "Be sure you ran dev_setup.sh first." >&2

source ./.env
python manage.py test
