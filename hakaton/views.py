from string import ascii_lowercase

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from auction.models import User
from django.contrib.auth import authenticate, login


@login_required
def account(request: HttpRequest):
    context = {
        'user': request.user
    }
    return render(request, "profile.html", context=context)


def sign_up(request: HttpRequest):
    if request.method == "POST":
        name = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return HttpResponse("Паролі не збігаються")
        if check_password_valid(str(password2)):
            user = User(username=name, email=email, phone=phone)
            user.set_password(password1)
            try:
                user.save()
            except Exception:
                return render(request, "registration/unsuccess-sign-up.html")
        else:
            return HttpResponse(
                """accepts only letters of the Latin alphabet Aa-Zz, 
                   digits 0-9 or special character from $@#&!-_;
                   at least 8 characters; maximum 16 characters inclusive;
                   contains at least 1 digit,
                   1 special character, 1 uppercase letter."""
            )
        return HttpResponseRedirect("/account/")
    return render(request, "registration/sign-up.html")


def sign_in(request: HttpRequest):
    return validation_login(request)


def validation_login(request: HttpRequest):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST.get['password']
        user = authenticate(username=name, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("sign_up_verify"))
        else:
            return HttpResponse("<H1>Неправильно введені дані!!!</H1>")
    elif request.method == 'GET':
        return render(request, "registration/login.html")


def success(request):
    return render(request, "success-reg.html")


def check_password_valid(password: str) -> bool:
    print(password)
    if len(password) not in range(8, 17):
        return False
    has_upper = False
    has_digit = False
    has_special = False
    for letter in password:
        if letter.isalpha():
            if letter.upper() == letter:
                has_upper = True
            if letter.lower() not in ascii_lowercase:
                return False
        elif letter.isdigit():
            has_digit = True
        elif letter in "$@#&!-_":
            has_special = True
        else:
            return False
    return all([has_upper, has_digit, has_special])
