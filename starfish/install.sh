#!/usr/bin/env bash
set -e
set -x

if [ ! -f ./.env ]; then
    cp .env.template .env 
    read -p "You will need to edit .env to add your secret keys. Press Enter to confirm you understand and continue."
fi


python3 -m venv .venv
source .venv/bin/activate

source ./.env
pip install -r requirements.txt
pip install -r requirements_dev.txt

python manage.py flush --no-input

python manage.py migrate

python manage.py loaddata regions/fixtures/regions.json

python manage.py create_state_chapters
