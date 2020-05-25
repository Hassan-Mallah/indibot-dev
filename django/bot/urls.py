from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('User', views.ListTelegramUserSerializerView)
router.register('Review', views.ListReviewSerializerView)

urlpatterns = [
    path('', include(router.urls))
]