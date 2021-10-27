from django.contrib.auth.models import User, AbstractUser
#from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import AbstractUser

class customuser(AbstractUser):
    address = models.TextField()
    phone_number = models.IntegerField()


class EbookingCard(models.Model):
    card_number = models.IntegerField()
    expiredate = models.IntegerField()
    expireyear = models.IntegerField()
    name = models.TextField()
    uid = models.IntegerField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    id=models.AutoField (primary_key=True)

    class Meta:
        managed = False
        db_table = 'ebooking_card'


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
