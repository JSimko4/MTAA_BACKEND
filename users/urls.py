from django.urls import path
from .views import RegisterView, LoginView, GetAllUsersView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("all/", GetAllUsersView.as_view()),
]