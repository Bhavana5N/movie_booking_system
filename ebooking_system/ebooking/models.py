from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.IntegerField()

class UserRegisrationForm(models.Model):
    name = models.CharField()
    phoneNumber = models.IntegerField()
    email = models.EmailField()
    password1 = models.CharField()
    password2 = models.CharField()
    cardNum = models.IntegerField()
    cardExpDate = models.DateField()
    streetAddressBilling = models.CharField()
    aptNumberBilling = models.CharField()
    stateBilling = models.CharField()
    zipCodeBilling = models.IntegerField()
    streetAddressHome = models.CharField()
    aptNumberHome = models.CharField()
    stateHome = models.CharField()
    zipCodeHome = models.IntegerField()