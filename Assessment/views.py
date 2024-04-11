from rest_framework.views import APIView
from django.utils.decorators import method_decorator

from .models import QuestionPaperFormatIndex

from .serializer import QuestionPaperFormatIndexSerializer

from DawnQuest.utils import send_response
from .utils import AssessmentGenerator


class AssessmentTest(APIView):
    def get(self, request):
        data = QuestionPaperFormatIndex.objects.filter()
        data = QuestionPaperFormatIndexSerializer(data, many=True).data
        return send_response(result=True, message="Success Hello", data=data)
    
    def post(self, request):
        payload = request.data
        chapters = [1504, 1505]
        format_ = 2

        assessment_generator = AssessmentGenerator(format_id = format_, user=2, chapters=chapters,)
        data = assessment_generator.generate_json()


        return send_response(result=True, message="post", data=data)


