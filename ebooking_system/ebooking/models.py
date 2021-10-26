from django.contrib.auth.models import User
from django.db import models
import sqlite3
from . import settings


from django.contrib.auth.models import AbstractUser

class customuser(AbstractUser):
    address = models.TextField()
    phone_number = models.IntegerField()

class UserRegisrationForm(models.Model):
    username = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    phone_number = models.IntegerField()
    email = models.EmailField()
    password1 = models.TextField()
    password2 = models.TextField()