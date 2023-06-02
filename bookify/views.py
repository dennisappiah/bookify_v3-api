from django.db.models import Count
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Category, Book, Comment, BookImage
from .serializers import CategorySerializer,\
 BookSerializer, AddBookSerializer, CommentSerializer, BookImageSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(books_count=Count('books')).all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        if Book.objects.filter(category_id=kwargs['pk']).count() > 0:
            return Response({"error": "Category cannot be deleted because it associated with a book"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.prefetch_related('images').all()
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return AddBookSerializer
        return BookSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(book_id=self.kwargs['book_pk'])

    def get_serializer_context(self):
        return {'book_id': self.kwargs['book_pk']}


class BookImageViewSet(ModelViewSet):
    serializer_class = BookImageSerializer

    def get_queryset(self):
        return BookImage.objects.filter(book_id=self.kwargs['book_pk'])

    def get_serializer_context(self):
        return {'book_id': self.kwargs['book_pk']}
