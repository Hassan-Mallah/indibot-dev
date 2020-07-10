from django.contrib import admin, messages
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
import os
import requests
from django.http import HttpResponseRedirect


# Dev: load .env locally
# from dotenv import load_dotenv
# load_dotenv()

# Register your models here.


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'name', 'city', 'email', 'phone')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewtype_id', 'reviewsubtype_id', 'date', 'text', 'get_email', 'get_phone')
    list_filter = ('reviewtype_id', 'reviewsubtype_id')
    readonly_fields = ['telegram_id', 'reviewtype_id', 'reviewsubtype_id', 'text', 'get_email', 'get_phone']

    change_form_template = 'admin/bot/Review_change_form.html'  # Change user page

    def get_email(self, obj):
        return obj.telegram_id.email

    get_email.short_description = 'email'

    def get_phone(self, obj):
        return obj.telegram_id.phone

    get_phone.short_description = 'Телефон'

    # send message to current user
    def response_change(self, request, obj):
        if "send_message" in request.POST:
            if request.POST['message']:
                text = request.POST['message']
                telegram_id = obj.telegram_id
                token = os.environ.get('BOT_TOKEN')

                data = {
                    'chat_id': telegram_id,
                    'text': text,
                    'parse_mode': 'Html'
                }
                url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
                requests.post(url, data=data)

                self.message_user(request, "Сообщение отправлено")
            else:
                messages.error(request, "Пожалуйста, введите сообщение")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Token)
