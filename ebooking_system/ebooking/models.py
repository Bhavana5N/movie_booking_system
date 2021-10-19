from django.db import models


class Movie(models.Model):
    movie_id = models.AutoField()
    title = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=255, blank=True, null=True)
    rating = models.TextField(blank=True, null=True)  # This field type is a guess.
    cast = models.CharField(max_length=255, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    producer = models.CharField(max_length=255, blank=True, null=True)
    trailer_link = models.CharField(max_length=255, blank=True, null=True)
    poster = models.CharField(max_length=255, blank=True, null=True)
    film_rating_code = models.IntegerField(blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie'


class RatingCode(models.Model):
    id = models.AutoField(blank=True, null=True)
    rating = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rating_code'


class User(models.Model):
    user_id = models.AutoField()
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    subscribe = models.IntegerField()
    password = models.CharField(max_length=255)
    is_admin = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'


class UserStatus(models.Model):
    id = models.AutoField()
    status_type = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_status'