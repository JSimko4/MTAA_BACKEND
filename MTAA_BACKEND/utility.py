from rest_framework import status
from rest_framework.response import Response
from users.models import User


def validate_user(user_id: int, token: str,):
    token_db = User.objects.get(id=user_id).access_token

    if token == token_db:
        return True

    return False


# validate json for save/edit
def validate_json_data(request):
    try:
        access_token = request.data["access_token"]
        body_parts = request.data["body_parts"]

        if not (isinstance(access_token, str)):
            raise TypeError

        if not all(isinstance(j, int) for j in body_parts):
            raise TypeError
    except (KeyError, TypeError):
        return False
    return True
