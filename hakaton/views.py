from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from auction.models import Auction, User
from django.contrib.auth import authenticate, login, logout


def account(request: HttpRequest):
    return autorisation_my(request)


def sign_up(request: HttpRequest):
    return render(request, "sign-up.html")


def sign_in(request: HttpRequest):
    return validation_login(request)


def validation_login(request: HttpRequest):
    if request.method == 'POST':
        print("valaditob login")
        name = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=name, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("sign_up_verify"))
        else:
            return HttpResponse("<H1>Неправильно введені дані!!!</H1>")
    elif request.method == 'GET':
        return render(request, "sign-in.html")


def validation_reg(request: HttpRequest):
    if request.method == 'POST':
        name = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        print(name, email, password1, password2)
        return render(request, "success-reg.html")
    else:
        return HttpResponse('Ошибка: данные должны быть отправлены методasом POST.')


def autorisation_my(request: HttpRequest):
    if request.user.is_authenticated:
        context = {
            "user_I": request.user
        }
        return render(request, "profile.html", context=context)
    return sign_in(request)


def success(request):
    return render(request, "success-reg.html")
