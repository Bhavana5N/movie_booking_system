from django.contrib.auth.models import User
from django.db import models
import sqlite3
from . import settings


from django.contrib.auth.models import AbstractUser

class customuser(AbstractUser):
    address = models.TextField()

