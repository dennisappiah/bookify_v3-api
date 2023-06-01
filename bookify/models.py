from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from .validate import validate_file_size
from datetime import datetime
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="books")
    numberInStock = models.PositiveSmallIntegerField()
    dailyRentalRate = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return self.title

class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="bookify/images", validators=[validate_file_size])


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

class Customer(models.Model):
    phone = models.CharField(max_length=255)
    isGold = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    rentalFee = models.DecimalField(
        decimal_places=2,
         max_digits=6,  validators=[ MinValueValidator
        (1, message="rental Fee cannot less than 1")
        ])
    dateOut = models.DateTimeField(auto_now=True)
    dateReturned = models.DateField()
    


