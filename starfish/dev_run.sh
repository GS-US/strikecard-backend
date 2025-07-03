#!/usr/bin/env bash

echo "Be sure you ran dev_setup.sh first." >&2

PORT="${1:-8000}"
if [[ $# -gt 0 ]]; then shift; fi

source ./.env
python manage.py runserver 0.0.0.0:$PORT
