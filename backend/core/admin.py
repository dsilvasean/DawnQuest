from django.contrib import admin

from .models import Spider,Book, Meta, MetaAttributeExtra
from .models import Board, Publication, Grade, Subject, Chapter, QuestionType, Question, Solution, QuestionResource, SolutionResource
class BookAdminModel(admin.ModelAdmin):
    list_display = ('grade', 'title_eng', 'to_scrape')  # Fields to display in the change list
    list_filter = ('grade', 'to_scrape')  # Fields for filtering

class GradeAdminModel(admin.ModelAdmin):
    list_display = ('grade',)   # Fields to display in the change list
    list_filter = ('grade',)


admin.site.register(Spider)
# admin.site.register(Book, BookAdminModel)
admin.site.register(Meta)
admin.site.register(MetaAttributeExtra)

admin.site.register(Board)
admin.site.register(Publication)
admin.site.register(Grade, GradeAdminModel)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Solution)
admin.site.register(QuestionResource)
admin.site.register(SolutionResource)




