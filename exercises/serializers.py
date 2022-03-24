from rest_framework import serializers
from .models import Exercise, BodyPart
from users.serializers import UserSerializer

class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = ('id', 'name')


class ExerciseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    creator = UserSerializer(read_only=True)

    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    image_path = serializers.CharField(max_length=255)
    body_parts = serializers.ListField(child = serializers.IntegerField())

    class Meta:
        model = Exercise
        fields = ('__all__')
        depth = 1
