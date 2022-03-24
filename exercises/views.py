from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from MTAA_BACKEND.utility import validate_user, validate_json_data
from users.models import User
from .models import Exercise, BodyPart
from .serializers import ExerciseSerializer, BodyPartSerializer


# access vsetci pouzivatelia neni potrebne validovat token
class GetBodyPartsView(APIView):
    def get(self, request):
        body_parts = BodyPart.objects.filter()
        serializer = BodyPartSerializer(body_parts, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# access vsetci pouzivatelia neni potrebne validovat token
class GetFilterExercisesView(APIView):
    def post(self, request, user_id: int):
        # najdi cviky ktore splnaju aspon jeden z filtrov
        exercises = Exercise.objects.filter(user=user_id,
                                            body_parts__in=request.data["body_parts"])
        serializer = ExerciseSerializer(exercises, many=True)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# access vsetci pouzivatelia neni potrebne validovat token
class GetExerciseView(APIView):
    def get(self, request, exercise_id: int):
        try:
            exercise = Exercise.objects.get(id=exercise_id)
            serializer = ExerciseSerializer(exercise)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exercise.DoesNotExist:
            return Response({"status": "error - exercise not found"}, status=status.HTTP_404_NOT_FOUND)


# access vsetci pouzivatelia neni potrebne validovat token
class GetAllExercisesView(APIView):
    def get(self, request, user_id: int):
        exercises = Exercise.objects.filter(user=user_id)
        serializer = ExerciseSerializer(exercises, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# je potrebne validovat token
class CopyExerciseView(APIView):
    def post(self, request):
        try:
            user_id = request.data["user_id"]
            exercise_id = request.data["exercise_id"]
            access_token = request.data["access_token"]

            if not (isinstance(user_id, int) and isinstance(exercise_id, int) and isinstance(access_token, str)):
                raise TypeError
        except (KeyError, TypeError):
            return Response({"status": "error - bad request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"status": "error - user not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            exercise = Exercise.objects.get(id=exercise_id)
        except Exercise.DoesNotExist:
            return Response({"status": "error - exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        if not validate_user(user_id, access_token):
            return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

        exercise = Exercise.objects.create(user=user,
                                           creator=exercise.creator,
                                           name=exercise.name,
                                           description=exercise.description,
                                           image_path=exercise.image_path)
        exercise.save()

        return Response({"status": "success"}, status=status.HTTP_200_OK)


# je potrebne validovat token
class SaveExerciseView(APIView):
    def post(self, request, user_id: int):
        serializer = ExerciseSerializer(data=request.data)

        if serializer.is_valid():
            if not validate_json_data(request):
                return Response({"status": "error - bad request"}, status=status.HTTP_400_BAD_REQUEST)

            # check if all body parts exist
            body_parts_list = []
            for body_part_id in request.data["body_parts"]:
                try:
                    body_parts_list.append(BodyPart.objects.get(id=body_part_id))
                except BodyPart.DoesNotExist:
                    return Response({"status": "error - body part not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                user_n_creator = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"status": "error - user not found"}, status=status.HTTP_404_NOT_FOUND)

            if not validate_user(user_id, request.data["access_token"]):
                return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

            new_exercise = Exercise.objects.create(user=user_n_creator,
                                                   creator=user_n_creator,
                                                   name=request.data["name"],
                                                   description=request.data["description"],
                                                   image_path="TODOOOOOO")
            new_exercise.save()

            # add body parts
            for body_part in body_parts_list:
                new_exercise.body_parts.add(body_part)

            return Response({"status": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# je potrebne validovat token
class EditExerciseView(APIView):
    def put(self, request, exercise_id: int):
        try:
            exercise = Exercise.objects.get(id=exercise_id)
            serializer = ExerciseSerializer(exercise, data=request.data, partial=True)

            if serializer.is_valid():
                if not validate_json_data(request):
                    return Response({"status": "error - bad request"}, status=status.HTTP_400_BAD_REQUEST)

                # check if all body parts exist
                body_parts_list = []
                for body_part_id in request.data["body_parts"]:
                    try:
                        body_parts_list.append(BodyPart.objects.get(id=body_part_id))
                    except BodyPart.DoesNotExist:
                        return Response({"status": "error - body part not found"}, status=status.HTTP_404_NOT_FOUND)

                if not validate_user(exercise.user_id, request.data["access_token"]):
                    return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

                serializer.save()

                # remove all exercise  body parts
                for body_part in exercise.body_parts.all():
                    exercise.body_parts.remove(body_part)

                # add new/edited body parts
                for body_part in body_parts_list:
                    exercise.body_parts.add(body_part)

                return Response({"status": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error - bad request", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exercise.DoesNotExist:
            return Response({"status": "error - exercise not found"}, status=status.HTTP_404_NOT_FOUND)


# je potrebne validovat token
class DeleteExerciseView(APIView):
    def delete(self, request, exercise_id: int, access_token: str):
        exercise = get_object_or_404(Exercise, id=exercise_id)

        if not validate_user(exercise.user_id, access_token):
            return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

        exercise.delete()
        return Response({"status": "success"})
