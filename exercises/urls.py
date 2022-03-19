from django.urls import path
from .views import GetBodyPartsView, GetFilterExercisesView, GetExerciseView, GetAllExercisesView, \
    SaveExerciseView, EditExerciseView, DeleteExerciseView

urlpatterns = [
    path("<int:user_id>/body_parts", GetBodyPartsView.as_view()),
    path("<int:user_id>/body_parts", GetFilterExercisesView.as_view()),
    path("<int:user_id>/", GetExerciseView.as_view()),
    path("<int:user_id>/body_parts", GetAllExercisesView.as_view()),
    path("<int:user_id>/save_exercise/", SaveExerciseView.as_view()),
    path("<int:user_id>/edit/", EditExerciseView.as_view()),
    path("<int:user_id>/delete/", DeleteExerciseView.as_view())
]
