from django.contrib import admin

from .models import Grade, Spider, Book, Board, Subject

class BookAdminModel(admin.ModelAdmin):
    list_display = ('grade', 'title_eng', 'to_scrape')  # Fields to display in the change list
    list_filter = ('grade', 'to_scrape')  # Fields for filtering

class GradeAdminModel(admin.ModelAdmin):
    list_display = ('grade',)   # Fields to display in the change list
    list_filter = ('grade',)



# Register your models here.

admin.site.register(Grade, GradeAdminModel)
admin.site.register(Spider)
admin.site.register(Board)
admin.site.register(Book, BookAdminModel)
admin.site.register(Subject)

