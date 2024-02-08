from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def render_range():
    return range(10)


def index(request: HttpRequest):
    return render(request, "index.html")