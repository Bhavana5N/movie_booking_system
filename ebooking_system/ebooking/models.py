from django.contrib.auth.models import User, AbstractUser
#from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import AbstractUser

class customuser(AbstractUser):
    phone_number = models.IntegerField()
    streetAddressBilling = models.TextField()
    aptNumberBilling = models.TextField()
    stateBilling = models.TextField()
    zipCodeBilling = models.IntegerField()
    streetAddressHome = models.TextField()
    aptNumberHome = models.TextField()
    stateHome = models.TextField()
    zipCodeHome = models.IntegerField()
    promotion = models.BooleanField(default='False')
    rememberme = models.BooleanField(default='False')


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
    password1 = models.TextField()
    password2 = models.TextField()
    email = models.EmailField()
    promotion = models.BooleanField()
    phone_number = models.IntegerField()
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

class EbookingMovie(models.Model):
    movie_title = models.TextField(blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    ratings = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    trailer_link = models.BinaryField(blank=True, null=True)
    image_link = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ebooking_movie'


