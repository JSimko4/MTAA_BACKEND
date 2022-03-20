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
            try:
                url_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

            new_exercise = Exercise.objects.create(user=url_user, name=request.data["name"],
                                                   description=request.data["description"],
                                                   image_path=request.data["image_path"])
            new_exercise.save()

            if "body_parts" in request.data:
                body_parts = request.data["body_parts"]

                for body_part_id in body_parts:
                    try:
                        body_part = BodyPart.objects.get(id=body_part_id)
                        new_exercise.body_parts.add(body_part)
                    except BodyPart.DoesNotExist:
                        return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EditExerciseView(APIView):
    def put(self, request, exercise_id: int):
        exercise = Exercise.objects.get(id=exercise_id)
        
        serializer = ExerciseSerializer(exercise, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteExerciseView(APIView):
    def delete(self, request, exercise_id: int):
        print("x")