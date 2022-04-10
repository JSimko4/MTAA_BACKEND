from django.urls import path
from .views import GetBodyPartsView, GetFilterExercisesView, GetExerciseView, GetAllExercisesView, \
    SaveExerciseView, EditExerciseView, DeleteExerciseView, CopyExerciseView

urlpatterns = [
    path("body_parts/", GetBodyPartsView.as_view()),
    path("copy_exercise/", CopyExerciseView.as_view()),

    path("<int:user_id>/filter_exercises/", GetFilterExercisesView.as_view()),
    path("<int:user_id>/all/", GetAllExercisesView.as_view()),
    path("<int:user_id>/save_exercise/", SaveExerciseView.as_view()),

    path("<int:exercise_id>/", GetExerciseView.as_view()),
    path("<int:exercise_id>/edit/", EditExerciseView.as_view()),
    path("<int:exercise_id>/delete/", DeleteExerciseView.as_view())
]
