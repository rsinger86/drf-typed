import uuid

from django.utils import timezone
from django.core import mail
from django.db import models
from django.utils.functional import cached_property


class UserAccount(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    password_updated_at = models.DateTimeField(null=True)
    joined_at = models.DateTimeField(null=True)
    has_trial = models.BooleanField(default=False)

    status = models.CharField(
        default="active",
        max_length=30,
        choices=(("active", "Active"), ("banned", "Banned"), ("inactive", "Inactive")),
    )


class Movie(models.Model):
    title = models.CharField(max_length=100)
    rating = models.FloatField(default=0)

    genre = models.CharField(
        max_length=30, choices=(("comedy", "Comedy"), ("drama", "Drama"))
    )
