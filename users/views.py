from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
from django.utils.crypto import get_random_string


class RegisterView(APIView):
    def post(self, request):
        try:
            name = request.data["name"]
            password = request.data["password"]

            if not (isinstance(name, str) and isinstance(password, str)):
                raise TypeError
        except (KeyError, TypeError):
            return Response({"status": "error - bad request"}, status=status.HTTP_400_BAD_REQUEST)

        # user name already in DB
        if User.objects.filter(name=name).exists():
            # https://stackoverflow.com/questions/9269040/which-http-response-code-for-this-email-is-already-registered
            return Response({"status": "fail - user name already registered"}, status=status.HTTP_409_CONFLICT)

        # create new user
        access_token = get_random_string(length=255)
        new_user = User.objects.create(name=name,
                                       password=password,
                                       access_token=access_token)
        new_user.save()

        return Response({"status": "success", "access_token": access_token}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        try:
            name = request.data["name"]
            password = request.data["password"]

            if not (isinstance(name, str) and isinstance(password, str)):
                raise TypeError
        except (KeyError, TypeError):
            return Response({"status": "error - bad request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_db = User.objects.get(name=name)
        except User.DoesNotExist:
            return Response({"status": "error - user not found"}, status=status.HTTP_404_NOT_FOUND)

        if password == user_db.password:
            return Response({"status": "success", "access_token": user_db.access_token}, status=status.HTTP_200_OK)

        return Response({"status": "fail - wrong password"}, status=status.HTTP_401_UNAUTHORIZED)



class GetAllUsersView(APIView):
    def get(self, request):
        users = User.objects.filter()
        serializer = UserSerializer(users, many=True)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
