from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Category, Book, Customer, Rental, BookImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'books_count']
    search_fields = ['name']

    @admin.display(ordering="books_count")
    def books_count(self, category: Category):
        url = (reverse('admin:bookify_book_changelist') + '?'
               + urlencode({'category__id': str(category.id)}))
        return format_html(f'<a href="{url}">{category.books_count}</a>')


    """overriding the queryset to include `books_count` attribute on Category object"""
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(books_count=Count('books'))


class BookImageInline(admin.TabularInline):
    model = BookImage
    readonly_fields = ['thumbnail']
    extra = 0
    min_num = 0
    max_num = 10

    def thumbnail(self, instance):
        if instance.image.name != "":
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ""


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    autocomplete_fields= ['category']
    inlines = [BookImageInline]
    list_display = ['title', 'category_name', 'numberInStock', 'dailyRentalRate']
    search_fields = ['title']

    def category_name(self, book:Book) -> str:
        return book.category.name


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields=['user']
    list_display = ['first_name', 'last_name', 'isGold']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    autocomplete_fields = ['book', 'customer']
    list_display = ['book', 'customer', 'rentalFee', 'dateOut', 'dateReturned']