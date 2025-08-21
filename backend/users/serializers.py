from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Grade, Board
from .models import Student

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    grade_id = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), source='grade', required=False)
    board_id = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), source='board', required=False)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'type', 'first_name', 'last_name', 'grade_id', 'board_id']

    def validate_type(self, value):
        if value != 1:  # Only students can register via this endpoint
            raise serializers.ValidationError("Only students can register.")
        return value

    def create(self, validated_data):
        grade = validated_data.pop('grade', None)
        board = validated_data.pop('board', None)
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        # Create user
        user = User.objects.create_user(**validated_data)

        # Create linked student profile
        Student.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            grade=grade,
            board=board
        )
        return user
