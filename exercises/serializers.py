from rest_framework import serializers
from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    image_path = serializers.CharField(max_length=255)

    class Meta:
        model = Exercise
        fields = '__all__'
