from django.db import models

from core.models import TimeStampAbstractModel, MetaAbstarctModel
from core.models import Board, Grade, Subject, Question, QuestionType

class QuestionPaper(TimeStampAbstractModel, MetaAbstarctModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    max_marks = models.IntegerField()
    questions = models.ManyToManyField(Question, through='QuestionPaperQuestionRelation')


class QuestionPaperQuestionRelation(TimeStampAbstractModel, MetaAbstarctModel):
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()
    marks = models.IntegerField()


class QuestionPaperFormat(TimeStampAbstractModel,):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

class QuestionPaperFormatQuestion(TimeStampAbstractModel,):
    question_head = models.CharField(max_length=255)
    question_paper_format = models.ForeignKey(QuestionPaperFormat, on_delete=models.CASCADE)

class QuestionPaperFormatQuestionSubQuestion(TimeStampAbstractModel):
    question_paper_format_question = models.ForeignKey(QuestionPaperFormatQuestion, on_delete=models.CASCADE)
    question_type = models.ManyToManyField(QuestionType)
    max_marks = models.IntegerField()




