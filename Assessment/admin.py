from django.contrib import admin
from .models import QuestionPaperFormat, QuestionPaperFormatIndex, Assessment
from treebeard.admin import TreeAdmin

from treebeard.forms import movenodeform_factory


class QuestionPaperFormatAdminModel(TreeAdmin):
    form = movenodeform_factory(QuestionPaperFormat)

admin.site.register(QuestionPaperFormat, QuestionPaperFormatAdminModel)
admin.site.register(QuestionPaperFormatIndex)
admin.site.register(Assessment)

