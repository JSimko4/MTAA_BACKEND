from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
from django.utils.crypto import get_random_string


class RegisterView(APIView):
    def post(self, request):
        request.data["access_token"] = access_token = get_random_string(length=64)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # check if user name already in DB
            if User.objects.filter(name=request.data["name"]).exists():
                # https://stackoverflow.com/questions/9269040/which-http-response-code-for-this-email-is-already-registered
                return Response({"status": "user name already registered"}, status=status.HTTP_409_CONFLICT)

            serializer.save()
            return Response({"status": "success", "access_token": access_token}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_db = User.objects.get(name=request.data["name"])
            except User.DoesNotExist:
                return Response({"status": "user not found"}, status=status.HTTP_404_NOT_FOUND)

            if request.data["password"] != user_db.password:
                return Response({"status": "wrong password"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"status": "success", "access_token": user_db.access_token}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


class GetAllUsersView(APIView):
    def get(self, request):
        users = User.objects.filter()
        serializer = UserSerializer(users, many=True)

        return_data = []
        for user in serializer.data:
            return_data.append({"id": user["id"], "name": user["name"]})

        return Response({"status": "success", "data": return_data}, status=status.HTTP_200_OK)
