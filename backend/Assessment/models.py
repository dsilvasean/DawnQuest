from django.db import models

from treebeard.mp_tree import MP_Node

from core.models import Grade, Subject, QuestionType

class QuestionPaperFormat(MP_Node):
    NODE_TYPE = (
        (1, "FORMAT_ID"),
        (2, "QUESTION_SUBQUESTION"),
        (3, "TYPE")
    )
    node_type = models.IntegerField(choices=NODE_TYPE)
    marks = models.IntegerField()
    data = models.CharField(max_length=155)
    question_type = models.ManyToManyField(QuestionType, null=True, blank=True, limit_choices_to={'numchild': 0})

    def __str__(self):
        return f"{self.get_node_type_display(), self.marks, self.data}"



class QuestionPaperFormatIndex(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    format = models.ForeignKey(QuestionPaperFormat, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.grade.grade}, {self.subject.name} {self.format.data} {self.marks}"



