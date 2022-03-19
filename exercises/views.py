from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExerciseSerializer
from .models import Exercise


def user_exercises(request, user_id: int):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return JsonResponse({
            "mysql": {
                "test mysql version": version,
                "user_id": user_id
            }
        })

    except Exception as error:
        return HttpResponse(f"Error while connecting to PostgreSQL {error}")


class ExerciseView(APIView):
    def post(self, request, user_id: int):
        request.data["user_id"] = user_id

        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
