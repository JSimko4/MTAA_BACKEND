from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('id', 'name')
