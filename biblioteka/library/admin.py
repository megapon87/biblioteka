from django.contrib import admin
from .models import Book, SavedBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "shelf_label", "order", "rating")
    list_editable = ("order",)
    search_fields = ("title", "author")


@admin.register(SavedBook)
class SavedBookAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "saved_at")
