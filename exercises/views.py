from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExerciseSerializer
from .models import Exercise


# def user_exercises(request, user_id: int):
#     try:
#         cursor = connection.cursor()
#         cursor.execute("SELECT VERSION();")
#         version = cursor.fetchone()[0]
#
#         cursor.close()
#         connection.close()
#
#         return JsonResponse({
#             "mysql": {
#                 "test mysql version": version,
#                 "user_id": user_id
#             }
#         })
#
#     except Exception as error:
#         return HttpResponse(f"Error while connecting to PostgreSQL {error}")


class GetBodyPartsView(APIView):
    def get(self, request):
        print("x")


class GetFilterExercisesView(APIView):
    def get(self, request):
        print("x")


class GetExerciseView(APIView):
    def get(self, request, id=None):
        if id:
            item = Exercise.objects.get(id=id)
            serializer = ExerciseSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Exercise.objects.all()
        serializer = ExerciseSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetAllExercisesView(APIView):
    def get(self, request):
        print("x")


class SaveExerciseView(APIView):
    def post(self, request, user_id: int):
        request.data["user_id"] = user_id

        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EditExerciseView(APIView):
    def put(self, request):
        print("x")


class DeleteExerciseView(APIView):
    def delete(self, request):
        print("x")