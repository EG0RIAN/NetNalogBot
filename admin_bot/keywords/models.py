from django.db import models


class Users(models.Model):
    verbose_name = "Пользователи телеграм"
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.user_id)


class Keywords(models.Model):
    verbose_name = "Тригеры"
    keyword = models.CharField(max_length=50)
    message = models.TextField(max_length=4096)
    image_path = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"Keyword: {self.keyword}"
