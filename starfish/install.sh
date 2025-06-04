#!/usr/bin/env bash
set -e
set -x

cp starfish/local_settings.template.py starfish/local_settings.py

read -p "Edit starfish/local_settings.py, then press Enter to continue..."

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements_dev.txt

python manage.py flush --no-input

python manage.py migrate

python manage.py loaddata regions/fixtures/regions.json

python manage.py create_state_chapters
