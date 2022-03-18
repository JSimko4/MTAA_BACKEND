from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render


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