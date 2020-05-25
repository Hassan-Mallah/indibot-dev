from rest_framework import generics
from .models import TelegramUser, Review
from .serializers import TelegramUserSerializer, ReviewSerializer
from rest_framework import viewsets


class ListTelegramUserSerializerView(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer


class ListReviewSerializerView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer