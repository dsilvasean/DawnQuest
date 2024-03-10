from rest_framework import serializers
from .models import QuestionPaperFormatIndex, QuestionPaperFormat

class QuestionPaperFormatIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPaperFormatIndex
        fields = ['id','grade', 'subject', 'format', 'marks']

class QuestionPaperFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPaperFormat
        fields = "__all__"
