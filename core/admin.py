from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from core.models import User
from tag.models import TaggedItem
from bookify.admin import BookImageInline, BookAdmin
from bookify.models import Book


"""Extending the userAdmin model to include email, firstname, lastname"""
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 0


class CustomBookAdmin(BookAdmin):
    inlines = [TagInline , BookImageInline]


admin.site.unregister(Book)
admin.site.register(Book, CustomBookAdmin)