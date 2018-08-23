from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    tx_url = models.CharField(max_length=80, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class Tag(models.Model):
    name = models.CharField(max_length=100)  # 标签名

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)  # 标签名

    def __str__(self):
        return self.name


