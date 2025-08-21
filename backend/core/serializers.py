# serializers.py

from rest_framework import serializers
from core.models import Grade, Board

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'grade']

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'board', 'board_display']

    board_display = serializers.CharField(source='get_board_display', read_only=True)
