from django.contrib.auth.models import User, AbstractUser
#from django.contrib.auth.forms import UserCreationForm
from django.db import models

#class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    mobile = models.IntegerField()

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
    cardNum = models.IntegerField()
    cardExpDate = models.DateField()
    streetAddressBilling = models.TextField()
    aptNumberBilling = models.TextField()
    stateBilling = models.TextField()
    zipCodeBilling = models.IntegerField()
    streetAddressHome = models.TextField()
    aptNumberHome = models.TextField()
    stateHome = models.TextField()
    zipCodeHome = models.IntegerField()