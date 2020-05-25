from rest_framework import serializers
from .models import TelegramUser, Review


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ("telegram_id", "username", "name", "phone", "email", "city")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("telegram_id", "text", "reviewtype_id", "reviewsubtype_id")