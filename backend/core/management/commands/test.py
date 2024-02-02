from django.core.management.base import BaseCommand

from Assessment.models import QuestionPaper
from core.models import Question, Subject

class Command(BaseCommand):
    help = 'Test command'

    def handle(self, *args, **options):
        format_ = {
            1:{
                '1':{"mark":5, "type_of_questions":['Fill in the blanks','MCQ ', 'One word answer']},
                '2':{"mark":5, "type_of_questions":['Match the columns', 'True or False', 'One line answer']}
            },
            2:{

            },
        }
        req = {
            "user":0,
            "grade":6,
            "subject":1,
            "board":1,
            "format":1 #unit test=1 or terminal=2
        }
        if req['format'] == 1:




