from django.contrib import admin
from django.urls import path, include

admin.site.site_url = None

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),
    path('', include('bot.urls')),  # DRF

]
