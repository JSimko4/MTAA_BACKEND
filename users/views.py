from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        return Response("xx")


class LoginView(APIView):
    def post(self, request):
        return Response("xx")


class GetAllUsersView(APIView):
    def get(self, request):
        users = User.objects.filter()
        serializer = UserSerializer(users, many=True)

        # json bez hesiel
        for user in serializer.data:
            user.pop("password", None)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
