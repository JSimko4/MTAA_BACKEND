from rest_framework import serializers
from .models import Exercise, BodyPart


class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = ('id', 'name')


class ExerciseSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    image_path = serializers.CharField(max_length=255)
    body_parts = BodyPartSerializer(read_only=True, many=True)
    
    def get_creator(self, obj):
        return obj.creator.id

    class Meta:
        model = Exercise
        fields = ('__all__')
        depth = 1
