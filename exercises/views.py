import os
import pathlib
import shutil
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .models import Exercise, BodyPart
from .serializers import ExerciseSerializer, BodyPartSerializer
from MTAA_BACKEND.utility import validate_user


# access vsetci pouzivatelia neni potrebne validovat token
class GetBodyPartsView(APIView):
    def get(self, request):
        body_parts = BodyPart.objects.filter()
        serializer = BodyPartSerializer(body_parts, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# access vsetci pouzivatelia neni potrebne validovat token
class GetFilterExercisesView(APIView):
    def post(self, request, user_id: int):
        try:
            body_parts = list(map(int, request.data["body_parts"].split(',')))
        except (KeyError, ValueError):
            return Response({"status": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

        # najdi cviky ktore splnaju aspon jeden z filtrov
        exercises = Exercise.objects.filter(user=user_id,
                                            body_parts__in=body_parts).distinct()
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
            return Response({"status": "exercise not found"}, status=status.HTTP_404_NOT_FOUND)


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
            return Response({"status": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"status": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            exercise = Exercise.objects.get(id=exercise_id)
        except Exercise.DoesNotExist:
            return Response({"status": "exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        if not validate_user(user_id, access_token):
            return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

        img_extension = exercise.image_path.split(".")[1]
        copy_name = str(uuid.uuid4()) + str(uuid.uuid4())
        copy_path = "%s/%s.%s" % ("images/", copy_name, img_extension)

        shutil.copy(exercise.image_path, copy_path)

        new_exercise = Exercise.objects.create(user=user,
                                               creator=exercise.creator,
                                               name=exercise.name,
                                               description=exercise.description,
                                               image_path=copy_path)
        new_exercise.save()

        # add body parts
        for body_part in exercise.body_parts.all():
            new_exercise.body_parts.add(body_part)

        return Response({"status": "success"}, status=status.HTTP_200_OK)


# je potrebne validovat token
class SaveExerciseView(APIView):
    def post(self, request, user_id: int):
        serializer = ExerciseSerializer(data=request.data)

        if serializer.is_valid():
            try:
                body_parts = list(map(int, request.data["body_parts"].split(',')))
                access_token = request.data["access_token"]
                if not isinstance(access_token, str):
                    raise TypeError
            except (KeyError, ValueError, TypeError):
                return Response({"status": "bad request missing access token or body parts"}, status=status.HTTP_400_BAD_REQUEST)

            # check if all body parts exist
            body_parts_list = []
            for body_part_id in body_parts:
                try:
                    body_parts_list.append(BodyPart.objects.get(id=body_part_id))
                except BodyPart.DoesNotExist:
                    return Response({"status": "body part not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                user_n_creator = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"status": "user not found"}, status=status.HTTP_404_NOT_FOUND)

            if not validate_user(user_id, request.data["access_token"]):
                return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

            if request.FILES.get("image", None) is not None:
                img = request.FILES["image"]
                img_extension = os.path.splitext(img.name)[1]

                save_path = "images"
                image_name = str(uuid.uuid4()) + str(uuid.uuid4())
                pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

                img_save_path = "%s/%s%s" % (save_path, image_name, img_extension)
                with open(img_save_path, "wb+") as f:
                    for chunk in img.chunks():
                        f.write(chunk)
            else:
                return Response({"status": "bad request - missing image"}, status=status.HTTP_400_BAD_REQUEST)

            new_exercise = Exercise.objects.create(user=user_n_creator,
                                                   creator=user_n_creator,
                                                   name=request.data["name"],
                                                   description=request.data["description"],
                                                   image_path=img_save_path)
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
                try:
                    body_parts = list(map(int, request.data["body_parts"].split(',')))
                    access_token = request.data["access_token"]
                    if not isinstance(access_token, str):
                        raise TypeError
                except (KeyError, ValueError, TypeError):
                    return Response({"status": "error - bad request access token / body parts"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # check if all body parts exist
                body_parts_list = []
                for body_part_id in body_parts:
                    try:
                        body_parts_list.append(BodyPart.objects.get(id=body_part_id))
                    except BodyPart.DoesNotExist:
                        return Response({"status": "error - body part not found"}, status=status.HTTP_404_NOT_FOUND)

                if not validate_user(exercise.user_id, request.data["access_token"]):
                    return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

                if request.FILES.get("image", None) is not None:
                    if os.path.exists(exercise.image_path):
                        os.remove(exercise.image_path)

                    img = request.FILES["image"]
                    img_extension = os.path.splitext(img.name)[1]

                    save_path = "images"
                    image_name = str(uuid.uuid4()) + str(uuid.uuid4())
                    pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

                    img_save_path = "%s/%s%s" % (save_path, image_name, img_extension)
                    with open(img_save_path, "wb+") as f:
                        for chunk in img.chunks():
                            f.write(chunk)

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
        try:
            exercise = Exercise.objects.get(id=exercise_id)
        except Exercise.DoesNotExist:
            return Response({"status": "exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        if not validate_user(exercise.user_id, access_token):
            return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

        if os.path.exists(exercise.image_path):
            os.remove(exercise.image_path)

        exercise.delete()
        return Response({"status": "success"})
