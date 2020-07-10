#!/usr/bin/env sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata data.json
python manage.py shell < set_bot_api_token.py