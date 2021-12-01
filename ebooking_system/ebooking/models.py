from django.contrib.auth.models import User, AbstractUser
#from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import AbstractUser
import base64

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
    promotion = models.TextField(default='off')
    rememberme = models.TextField(default='off')

class EncryptKey():

    is_instance = None

    def __init__(self):
        from cryptography.fernet import Fernet
        key = b'ETjEQiNW_TlaEqAVWGHkikn8g1LBd758knStznq3vpw='#Fernet.generate_key()  # this is your "password"
        self.cipher_suite = Fernet(key)

    @staticmethod
    def get_instance():
        if not EncryptKey.is_instance:
            EncryptKey.is_instance = EncryptKey()

        return EncryptKey.is_instance


class EbookingCard(models.Model):
    card_number = models.BinaryField()
    expiredate = models.IntegerField()
    expireyear = models.IntegerField()
    name = models.TextField()
    uid = models.IntegerField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    id=models.AutoField (primary_key=True)

    class Meta:
        managed = False
        db_table = 'ebooking_card'

    e_instance = EncryptKey.get_instance()

    def validate_card(self):
        if len(self.retreive_card) != 16:
            return False

        return True



    @property
    def retreive_card(cls):
        print(cls.card_number, type(cls.card_number))
        if cls.card_number:
            return cls.e_instance.cipher_suite.decrypt(cls.card_number).decode()
        else:
            return ''

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

class Order(models.Model):
    user_id = models.TextField(blank=True, null=True)
    showroom = models.TextField(blank=True, null=True)
    tickets = models.IntegerField(blank=True, null=True)
    seats = models.TextField(blank=True, null=True)
    show_time = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    movie = models.TextField(blank=True, null=True)
    schedule_id = models.IntegerField()
    payment_amount = models.IntegerField(default=0)
    card_id = models.TextField(default=0)
    class Meta:
        managed = False
        db_table = 'order'


class Promotions(models.Model):
    promotion_code = models.TextField()
    expiray_date = models.TextField()  # This field type is a guess.
    discount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'promotions'

class Ratings(models.Model):
    rating = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ratings'


class Showroom(models.Model):
    showroom = models.TextField(unique=True, blank=True, null=True)
    row_seats = models.IntegerField(blank=True, null=True)
    col_seats = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'showroom'

class EbookingMovie(models.Model):
    movie_title = models.TextField(blank=True, null=True, unique=True)
    actors = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True, default="coming_soon")
    ratings = models.TextField(blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    trailer_link = models.TextField(blank=True, null=True)
    image_link = models.TextField(blank=True, null=True)
    producer = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    age_category = models.TextField(blank=True, null=True)
    runtime = models.FloatField()
    price = models.TextField()

    def __str__(self):
        return self.movie_title

    class Meta:
        managed = False
        db_table = 'ebooking_movie'

class EbookingSchedule(models.Model):
    movie_title = models.TextField(blank=True, null=True, unique=True)
    date_time = models.DateTimeField(blank=True, null=True)
    showroom = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_schedule'


class Category(models.Model):
    c_type = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Tickets(models.Model):
    seats_booked = models.IntegerField(blank=True, null=True)
    showroom = models.TextField(blank=True, null=True)
    date = models.IntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    schedule_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tickets'


class TicketCategory(models.Model):
    ticket_type = models.IntegerField(unique=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_category'

