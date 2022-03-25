from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    access_token = serializers.CharField(max_length=64, required=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'access_token')
