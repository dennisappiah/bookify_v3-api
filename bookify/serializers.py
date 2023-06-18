from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Category, Book, Comment, BookImage, Customer, Rental


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
    book_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()

    class Meta:
        model = Rental
        fields = ['book_id', 'customer_id' ,'rentalFee', 'dateReturned']

    def validate_book_id(self, book_id):
        if not Book.objects.filter(pk=book_id).exists():
            raise serializers.ValidationError('No book with the given id was found')
        return book_id

    def validate_customer_id(self, customer_id):
        if not Customer.objects.filter(pk=customer_id).exists():
            raise serializers.ValidationError("No customer with the given id was found")
        return customer_id

    def save(self, **kwargs):
        with transaction.atomic():
            book_id = self.validated_data['book_id']
            customer_id = self.validated_data['customer_id']
            
            customer = get_object_or_404(Customer, pk=customer_id)
            book = get_object_or_404(Book, pk=book_id)

            if book.numberInStock <= 0:
                raise serializers.ValueError("Book is out of stock.")
        
            rental = Rental.objects.create(customer=customer, book=book, **self.validated_data)
            book.numberInStock -= 1
            book.save()

        return rental


   
                 

            
            
            

            

    