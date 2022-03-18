from django.http import HttpResponse
from django.shortcuts import render


def register(request):
    return HttpResponse("register")


def login(request):
    return HttpResponse("login")
