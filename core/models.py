from django.db import models
from django.contrib.auth.models import AbstractUser



"""Extending the User model to include email"""
class User(AbstractUser):
    email = models.EmailField(unique=True)

