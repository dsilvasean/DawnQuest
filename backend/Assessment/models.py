from django.db import models

from treebeard.mp_tree import MP_Node

from core.models import Grade, Subject, QuestionType, CoreQuestionType, Board, Grade, Question, Chapter
from users.models import User
class QuestionPaperFormat(MP_Node):
    NODE_TYPE = (
        (1, "FORMAT_ID"),
        (2, "QUESTION_SUBQUESTION"),
        (3, "TYPE")
    )
    node_type = models.IntegerField(choices=NODE_TYPE)
    marks = models.IntegerField()
    data = models.CharField(max_length=155)
    question_type = models.ManyToManyField(CoreQuestionType, null=True, blank=True, limit_choices_to={'numchild': 0})

    def __str__(self):
        return f"{self.get_node_type_display(), self.marks, self.data}"



class QuestionPaperFormatIndex(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    format = models.ForeignKey(QuestionPaperFormat, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.grade.grade}, {self.subject.name} {self.format.data} {self.marks}"
    
class Assessment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    format_id = models.ForeignKey(QuestionPaperFormatIndex, on_delete=models.CASCADE, blank=True, null=True)
    marks = models.IntegerField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, blank=True, null=True)
    chapters = models.ManyToManyField(Chapter, blank=True, )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    questions = models.ManyToManyField(Question, blank=True, related_name="assessment")

    raw_json = models.JSONField()

    def __str__(self):
        return f" {self.created_by.email} {self.format_id} {self.marks}"
    






