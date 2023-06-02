from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Category, Book, Customer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'books_count']
    search_fields = ['name']

    @admin.display(ordering="books_count")
    def books_count(self, category: Category):
        url = (reverse('admin:bookify_book_changelist') + '?'
               + urlencode({'category__id': str(category.id)}))
        return format_html('<a href="{}">{}</a>', url, category.books_count)


    """overriding the queryset to include `books_count` attribute on Category object"""
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(books_count=Count('books'))


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    autocomplete_fields= ['category']
    list_display = ['title', 'category_name', 'numberInStock', 'dailyRentalRate']

    def category_name(self, book:Book):
        return book.category.name


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields=['user']
    list_display = ['first_name', 'last_name', 'isGold']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']