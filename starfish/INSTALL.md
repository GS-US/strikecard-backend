# Dev Environment Setup
(recommend venv + pip)

 - setup a virtualenv
 - install requirements.txt
 - install requirements_dev.txt
 - `cp .env.template .env`
 - edit .env
   - set a value for `DJANGO_SECRET_KEY`
   - set a value for `DJANGO_CONTACT_HASH_SALT`
 - run dev.sh
 - visit `localhost:8000` in your favorite browser

## Generating secret keys for development
You can run the following in a terminal with the venv activated to output a
value appropriate for both `DJANGO_SECRET_KEY` and `DJANGO_CONTACT_HASH_SALT`:

```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```


## Notes for other setups

If you are running on a host other than localhost (or you have changed that name
on your system) and/or have multiple hostnames you need to allow, add the following to `.env`

```
export DJANGO_ALLOWED_HOSTS='yourhostname,yourotherhostname,localhost,ifyouuseit'
```