from django.contrib import admin
from .models import QuestionPaperFormat, QuestionPaperFormatIndex
from treebeard.admin import TreeAdmin

from treebeard.forms import movenodeform_factory


class QuestionPaperFormatAdminModel(TreeAdmin):
    form = movenodeform_factory(QuestionPaperFormat)

admin.site.register(QuestionPaperFormat, QuestionPaperFormatAdminModel)
admin.site.register(QuestionPaperFormatIndex)

