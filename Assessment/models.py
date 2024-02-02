# from django.db import models

# from core.models import Board, Grade, Subject
# from ShaalaaMiner.models import Question as ShaalaaQuestions

# # Create your models here.

# class QuestionPaper(models.Model):
#     max_marks = models.IntegerField()
#     board = models.ForeignKey(Board, on_delete=models.CASCADE)
#     grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
#     questions = models.ManyToManyField(ShaalaaQuestions, through='QuestionPaperQuestion')
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

# class QuestionPaperQuestion(models.Model):
#     question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
#     questions = models.ForeignKey(ShaalaaQuestions, on_delete=models.CASCADE)
#     index = models.IntegerField()
#     marks = models.IntegerField()
#     meta = models.CharField(max_length=255)



