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



class Promotions(models.Model):
    promotion_code = models.TextField()
    expiray_date = models.TextField()  # This field type is a guess.
    discount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'promotions'

class EbookingMovie(models.Model):
    movie_title = models.TextField(blank=True, null=True, unique=True)
    actors = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    ratings = models.TextField(blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    trailer_link = models.TextField(blank=True, null=True)
    image_link = models.TextField(blank=True, null=True)
    producer = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    age_category = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.movie_title

    class Meta:
        managed = False
        db_table = 'ebooking_movie'


