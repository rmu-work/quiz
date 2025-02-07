from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Category')
    description = models.TextField(blank=True, null=True, verbose_name='description')

    def __str__(self):
        return self.name



