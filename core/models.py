from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

"""Extending the User model to make email field unique"""


class User(AbstractUser):
    email = models.EmailField(unique=True)
