from rest_framework import status
from rest_framework.response import Response
from users.models import User


def validate_user(user_id: int, token: str,):
    token_db = User.objects.get(id=user_id).access_token

    if token == token_db:
        return True

    return False
