from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)

