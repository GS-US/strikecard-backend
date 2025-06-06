dev environment set up
(recommend venv + pip)

 - setup a virtualenv
 - install requirements.txt
 - install requirements_dev.txt
 - cp starfish/local_settings.template.py starfish/local_settings.py
 - edit starfish/local_settings.py
   - set a value for `SECRET_KEY`
   - set `ALLOWED_HOSTS` or set `DEBUG` to `True`
 - run dev.sh
 - visit `localhost:8000` in your favorite browser