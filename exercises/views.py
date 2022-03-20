from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .models import Exercise, BodyPart
from .serializers import ExerciseSerializer


class GetBodyPartsView(APIView):
    def get(self, request):
        print("x")


class GetFilterExercisesView(APIView):
    def get(self, request):
        print("x")


class GetExerciseView(APIView):
    def get(self, request, exercise_id: int):
        try:
            exercise = Exercise.objects.get(id=exercise_id)
            serializer = ExerciseSerializer(exercise)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exercise.DoesNotExist:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)


class GetAllExercisesView(APIView):
    def get(self, request, user_id: int):
        exercises = Exercise.objects.filter(user=user_id)
        serializer = ExerciseSerializer(exercises, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class SaveExerciseView(APIView):
    def post(self, request, user_id: int):

        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            # pridat osetrenie ked neexistuje dany user -> zla url id
            new_exercise = Exercise.objects.create(user=User.objects.get(id=user_id), name=request.data["name"],
                                                   description=request.data["description"],
                                                   image_path=request.data["image_path"])
            new_exercise.save()

            if "body_parts" in request.data:
                body_parts = request.data["body_parts"]

                # pridat osetrenie ak neexistuje dany body part
                for body_part_id in body_parts:
                    body_part = BodyPart.objects.get(id=body_part_id)
                    new_exercise.body_parts.add(body_part)

            return Response({"status": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EditExerciseView(APIView):
    def put(self, request):
        print("x")


class DeleteExerciseView(APIView):
    def delete(self, request):
        print("x")