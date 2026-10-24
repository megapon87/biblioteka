from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField("Назва", max_length=200)
    author = models.CharField("Автор", max_length=200)

    catalog_index = models.CharField(
        "Каталожний індекс", max_length=50, blank=True,
        help_text="Наприклад: 821.161.2 Ш37"
    )
    genre = models.CharField("Жанр", max_length=100, blank=True)
    year = models.CharField("Рік написання", max_length=20, blank=True)
    pages_total = models.PositiveIntegerField("Обсяг (сторінок)", default=0)

    summary = models.TextField("Скорочено (короткий переказ)", blank=True)
    rating = models.PositiveSmallIntegerField("Оцінка (0-5)", default=5)
    shelf_label = models.CharField("Назва полиці", max_length=100, default="класика")

    order = models.PositiveIntegerField("Порядок на полиці", default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.title} — {self.author}"


class SavedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="saved_by")
    saved_at = models.DateTimeField("Додано", auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")
        ordering = ["-saved_at"]

    def __str__(self):
        return f"{self.user.username} → {self.book.title}"
