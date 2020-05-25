from django.db import models

# Create your models here.


class TelegramUser(models.Model):
    telegram_id = models.IntegerField(primary_key=True, verbose_name='id')
    username = models.CharField(max_length=80, default='')  # Telegram username
    name = models.CharField(max_length=120, default='', verbose_name='имя')
    city = models.CharField(max_length=80, default='', verbose_name='город')
    email = models.CharField(max_length=80, default='')
    phone = models.CharField(max_length=20,default='', verbose_name='Телефон')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.telegram_id)


class ReviewType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=80, null=False, blank=False)

    def __str__(self):
        return self.description


class ReviewSubType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=80, null=False, blank=False)

    def __str__(self):
        return self.description


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    reviewtype_id = models.ForeignKey(ReviewType, on_delete=models.CASCADE, verbose_name='Тип')
    reviewsubtype_id = models.ForeignKey(ReviewSubType, on_delete=models.CASCADE, verbose_name='Подтип')
    text = models.CharField(max_length=2000, null=False, blank=False, verbose_name='текст')
    date = models.DateTimeField(auto_now=True, verbose_name='дата')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return str(self.id)


