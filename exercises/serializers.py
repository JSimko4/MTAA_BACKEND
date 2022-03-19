from rest_framework import serializers
from .models import Exercise, BodyPart


class ExerciseBodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = ('id', 'name')


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'image_path', 'body_parts']
        depth = 1
