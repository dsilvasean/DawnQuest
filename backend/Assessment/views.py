from rest_framework.views import APIView
from django.utils.decorators import method_decorator

from .models import QuestionPaperFormatIndex, QuestionPaperFormat
from core.models import Question

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

        print(json.dumps((parse_tree(tree, chapters=chapters))))
        # parse_tree(tree)

        return send_response(result=True, message="post")


