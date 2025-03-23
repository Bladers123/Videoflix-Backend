# authentication_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    custom = models.CharField(max_length=500, default='')
    address = models.CharField(max_length=150, default='')
    phone = models.CharField(max_length=25, default='')