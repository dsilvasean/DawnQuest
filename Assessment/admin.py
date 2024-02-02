from django.contrib import admin

from .models import QuestionPaper, QuestionPaperQuestionRelation

from .models import QuestionPaperFormat, QuestionPaperFormatQuestion, QuestionPaperFormatQuestionSubQuestion

admin.site.register(QuestionPaper)
# admin.site.register(QuestionPaperQuestion)
admin.site.register(QuestionPaperQuestionRelation)

admin.site.register(QuestionPaperFormat)
admin.site.register(QuestionPaperFormatQuestion)
admin.site.register(QuestionPaperFormatQuestionSubQuestion)

