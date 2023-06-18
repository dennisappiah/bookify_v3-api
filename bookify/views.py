from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Category, Book, Comment, BookImage, Customer, Rental
from .serializers import CategorySerializer,\
 BookSerializer, AddBookSerializer, CommentSerializer,\
  BookImageSerializer, CustomerSerializer, RentalSerializer, AddRentalSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(books_count=Count('books')).all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        if Book.objects.filter(category_id=kwargs['pk']).count() > 0:
            return Response({"error": "Category cannot be deleted because it associated with a book"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('category').prefetch_related('images').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return AddBookSerializer
        return BookSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(book_id=self.kwargs['book_pk'])

    def get_serializer_context(self):
        return {'book_id': self.kwargs['book_pk']}


class BookImageViewSet(ModelViewSet):
    serializer_class = BookImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return BookImage.objects.filter(book_id=self.kwargs['book_pk'])

    def get_serializer_context(self):
        return {'book_id': self.kwargs['book_pk']}


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]

    # customer profile -> /api/v1/customers/me
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = customer.objects.get(user_id= request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class RentalViewSet(ModelViewSet):
    queryset = Rental.objects.select_related('book').select_related('customer').all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return AddRentalSerializer
        return RentalSerializer


