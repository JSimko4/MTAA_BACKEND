from django.urls import path
from . import views
from .views import ExerciseView

urlpatterns = [
    path("<int:user_id>/", views.user_exercises),
    path("<int:user_id>/save_exercise/", ExerciseView.as_view())
]
