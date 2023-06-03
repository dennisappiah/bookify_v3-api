from rest_framework import serializers
from .models import Category, Book, Comment, BookImage, Customer, Rental
from django.db import transaction


class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'books_count']

class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = ['id', 'image']

    def create(self, validated_data):
        book_id = self.context['book_id']
        return BookImage.objects.create(book_id=book_id, **validated_data)


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = BookImageSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'category', 'numberInStock', 'dailyRentalRate', 'images']


class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'category', 'numberInStock', 'dailyRentalRate']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        book_id = self.context['book_id']
        return Comment.objects.create(book_id=book_id, **validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'isGold']


class RentalSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Rental
        fields = ['book', 'customer', 'rentalFee', 'dateReturned']


class AddRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['book', 'customer', 'rentalFee', 'dateReturned']


    def save(self, **kwargs):
        with transaction.atomic():
            customer = Customer.objects.get()
        return super().save(**kwargs)

    