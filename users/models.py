from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    tx_url = models.CharField(max_length=80, blank=True)

    class Meta(AbstractUser.Meta):
        pass
