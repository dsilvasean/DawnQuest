from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from django.utils.safestring import mark_safe

from .models import Spider,Book, Meta, MetaAttributeExtra
from .models import Board, Publication, Grade, Subject, Chapter, Question, QuestionType, Solution, QuestionResource, SolutionResource
class BookAdminModel(admin.ModelAdmin):
    list_display = ('grade', 'title_eng', 'to_scrape')  # Fields to display in the change list
    list_filter = ('grade', 'to_scrape')  # Fields for filtering

class GradeAdminModel(admin.ModelAdmin):
    list_display = ('grade',)   # Fields to display in the change list
    list_filter = ('grade',)


@admin.action(description="Mark select chapters to scrape")
def mark_to_scrape(modeladmin, request, queryset,):
    queryset.update(to_scrape=True)

@admin.action(description="Mark select chapters to not scrape")
def mark_to_not_scrape(modeladmin, request, queryset,):
    queryset.update(to_scrape=False)

class ChapterAdminModel(admin.ModelAdmin):
    list_display = ('name', 'get_subject', 'get_grade', 'to_scrape')   # Fields to display in the change list
    list_filter = ('subject__name','subject__grade__grade')
    actions  = [mark_to_scrape, mark_to_not_scrape]

    @admin.display(ordering= "chapter__subject", description='Subject')
    def get_subject(self, obj):
        return obj.subject.name

    @admin.display(ordering= "__grade", description='Grade')
    def get_grade(self, obj):
        return obj.subject.grade.grade

class QuestionAdminModel(admin.ModelAdmin):
    list_display = ('get_question', 'get_question_type', 'get_subject', 'get_grade', 'get_chapter', 'get_question_board')
    list_filter = ( 'chapter__subject__name', 'chapter__name', 'type__name')

    @admin.display(ordering= "chapter__subject", description='Subject')
    def get_subject(self, obj):
        return obj.chapter.subject.name

    @admin.display(ordering= "chapter__subject__grade", description='Grade')
    def get_grade(self, obj):
        return obj.chapter.subject.grade.grade

    @admin.display(ordering= "chapter__name", description='Chapter')
    def get_chapter(self, obj):
        return obj.chapter.name
     
    @admin.display(ordering= "question__type", description='Type')
    def get_question_type(self, obj):
        type_ = obj.type
        # descendants = type_.get_decendents()
        # descendants_names = [descendant.name for descendant in descendants]
        return f"{type_.name}"

    @admin.display(ordering= "question__type", description='Board')
    def get_question_board(self, obj):
        return obj.chapter.subject.board
    
    @admin.display(ordering= "question_render", description='Question')
    def get_question(self, obj):
        max_length = 150
        html_field = obj.question[:max_length] if obj.question else '' 
        truncated_html = mark_safe(html_field) if html_field else ''
        return f"{truncated_html}..." if len(html_field) == max_length else truncated_html  
    

class QuestionTypeAdminModel(TreeAdmin):
    form = movenodeform_factory(QuestionType)

admin.site.register(Spider)
# admin.site.register(Book, BookAdminModel)
admin.site.register(Meta)
admin.site.register(MetaAttributeExtra)

admin.site.register(Board)
admin.site.register(Publication)
admin.site.register(Grade, GradeAdminModel)
admin.site.register(Subject)
admin.site.register(Chapter, ChapterAdminModel)
admin.site.register(QuestionType, QuestionTypeAdminModel)
# admin.site.register(QuestionSubType)
admin.site.register(Question, QuestionAdminModel)
admin.site.register(Solution)
admin.site.register(QuestionResource)
admin.site.register(SolutionResource)




