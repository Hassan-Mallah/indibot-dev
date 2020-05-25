import os

from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

user = get_user_model().objects.get_or_create(username='bot_api', defaults={'is_superuser': True})[0]

token = Token.objects.filter(user_id=user.pk).all()

if token:
    token.delete()
Token.objects.create(user_id=user.pk, key=os.environ.get('BOT_API_TOKEN'))
