from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=150, null=True, verbose_name='Name')
    mobile_number = models.CharField(max_length=25, null=True, verbose_name='Mobile Number')

    def __str__(self):
        return self.name or self.username
