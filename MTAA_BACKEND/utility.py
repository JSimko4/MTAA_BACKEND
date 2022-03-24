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
        if not (isinstance(request.data["access_token"], str)):
            raise TypeError

        if not all(isinstance(j, int) for j in request.data["body_parts"]):
            raise TypeError
    except (KeyError, TypeError):
        return True
    return False
