from django.core.management.base import BaseCommand

from Assessment.models import QuestionPaperFormat
from core.models import Question, Subject, QuestionType

class Command(BaseCommand):
    help = 'Test command'
    def handle(self, *args, **kwars):
        qt = QuestionType.objects.filter(name="Fill in the Blanks")
        for node in qt:
            if 0== 0:
                questions = node.questions.filter(chapter__subject__id=87, chapter__id=1512)
                print(questions.count())
                for question in questions:
                    print(question.question, node)
                    print("*"*10)




