#!/usr/bin/env sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata data.json
echo "from django.contrib.auth import get_user_model; User = get_user_model();
if User.objects.filter(username='admin').count() == 0:
    User.objects.create_superuser('admin', '', '2S~tR*-k>6Mz)h:K')" | python manage.py shell