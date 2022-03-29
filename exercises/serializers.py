from rest_framework import serializers
from .models import Exercise, BodyPart


class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = ('id', 'name')


class ExerciseSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    creator_id = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    image_path = serializers.CharField(max_length=255, required=False)
    body_parts = BodyPartSerializer(read_only=True, many=True)

    def get_id(self, obj):
        return obj.id

    def get_creator_id(self, obj):
        return obj.creator.id

    def get_creator_name(self, obj):
        return obj.creator.name

    class Meta:
        model = Exercise
        fields = ('id', 'creator_id', 'creator_name', 'name', 'description', 'image_path', 'body_parts')
        depth = 1
