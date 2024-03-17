from rest_framework.views import APIView
from django.utils.decorators import method_decorator

from .models import QuestionPaperFormatIndex, QuestionPaperFormat, Assessment
from core.models import Question
from users.models import User

from .serializer import QuestionPaperFormatIndexSerializer, QuestionPaperFormatSerializer

from DawnQuest.utils import send_response, parse_tree

import json


{
            "format_id": 2,
            "chapters":[1504, 1505]
        }

class AssessmentTest(APIView):
    def get(self, request):
        data = QuestionPaperFormatIndex.objects.filter()
        data = QuestionPaperFormatIndexSerializer(data, many=True).data
        return send_response(result=True, message="Success Hello", data=data)
    
    def post(self, request):
        q ={}

        # questionaire = {
        #     "data_type":"question_paper",
        #     "_meta":{
        #         "marks":
        #     }
            
        # }
        
        payload = request.data

        result  = {}

        chapters = [1504, 1505]
        format_ = 2

        
        question_paper_format = QuestionPaperFormatIndex.objects.get(id=format_).format
        questions = Question.objects.filter(chapter__id__in=chapters, visibility=True)

        tree = question_paper_format.dump_bulk()[0]

        data_ = (parse_tree(tree, chapters=chapters))
        print(data_)
        # print(json.dumps(data_))
        assessment_instacne = Assessment.objects.create(created_by=User.objects.get(id=2), marks=20, raw_json=data_['result'], format_id_id=format_, subject_id=87)
        assessment_instacne.chapters.add(*chapters)
        assessment_instacne.questions.add(*data_['meta']['question_ids'])

        # parse_tree(tree)

        return send_response(result=True, message="post", data=data_['result'])


