from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from auction.models import Auction


def render_range():
    return range(10)


def index(request: HttpRequest):
    return render(request, "index.html")


def auction_list(request: HttpRequest):
    auction_list = Auction.objects.all()
    context = {
        "auction_list": auction_list
    }
    return render(request, "auction-list.html", context=context)


@csrf_protect
def account(request: HttpRequest):
    return autorisation_my(request)


def sign_up(request: HttpRequest):
    return render(request, "sign-up.html")


def sign_in(request: HttpRequest):
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
        return HttpResponse('Ошибка: данные должны быть отправлены методом POST.')


@ensure_csrf_cookie
def autorisation_my(request: HttpRequest):
    if request.user.is_authenticated:
        csrf_token = request.COOKIES.get('csrftoken', '')  # Получение CSRF токена из куки

        return render(request, "profile.html")
    else:
        print("222222222222222222")
        # Если пользователь не аутентифицирован, выполните другие действия
        # Ваша логика для неаутентифицированного пользователя
        return sign_up(request)


def auction_list_detail(request, pk: int):
    print("Start")
    auction = Auction.objects.get(pk=pk)
    context = {
        "auction": auction
    }
    print("end")
    print(context)
    return render(request, "auction.html", context=context)
