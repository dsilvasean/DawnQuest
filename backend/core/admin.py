from django.contrib import admin

from .models import Grade, Spider, Book, Board, Subject


# Register your models here.

admin.site.register(Grade)
admin.site.register(Spider)
admin.site.register(Board)
admin.site.register(Book)
admin.site.register(Subject)

