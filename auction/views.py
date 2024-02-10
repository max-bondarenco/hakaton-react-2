import datetime

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from auction.models import Auction, User, Lot
from django.contrib.auth import authenticate, login, logout

from hakaton.views import account


def index(request: HttpRequest):
    return render(request, "index.html")


def auction_list_detail(request, pk: int):
    auction = Auction.objects.get(pk=pk)
    context = {
        "auction": auction
    }
    return render(request, "auction/auction-info.html", context=context)


def auction_my(request):
    if request.user.is_authenticated:
        auctions = Auction.objects.filter(creator_id=request.user.id)
        print("auction")
        print(auctions)
        context = {
            "auctions": auctions,
        }
        return render(request, "auction/auction-my.html", context=context)
    return account(request)


def auction_going(request, pk: int):
    auction = Auction.objects.get(pk=pk)
    context = {
        "auction": auction,
    }
    if auction.seconds_to_end == 0:
        auction.seconds_to_end -= 5
        auction.is_completed = True
        auction.save()
        return render(request, "auction/auction-completed.html", context=context)
    else:
        auction.seconds_to_end -= 5
        auction.save()
        print("Second to end:")
        print(auction.seconds_to_end)
        start_time = datetime.datetime.strptime(str(auction.time_of_start)[:-6], "%Y-%m-%d %H:%M:%S")

        if datetime.datetime.now() > start_time:

            return render(request, "auction/auction-going.html", context=context)
        return render(request, "auction/auction-not-going.html")


def auction_going_accept(request, pk: int):
    if request.method == "POST":
        print(request.headers.get("Custom-Header"))
        print("ssdsdefwewrwe")
        return HttpResponse("fsfesfs")
    else:
        auction = Auction.objects.get(pk=pk)
        auction.is_completed = True

        context = {
            "auction": auction,
            "IS-COM": auction.is_completed
        }
        print("------------------")
        print(context)
        print("------------------")
        return render(request, "success-auction.html", context=context)


def lots_my(request):
    if request.user.is_authenticated:
        auctions = Lot.objects.filter(sender_id=request.user.id)
        print("auction")
        print(auctions)
        context = {
            "auctions": auctions,
        }
        return render(request, "auction/lots-my.html", context=context)
    return account(request)


def create_auction(request):
    return render(request, "auction/create-auction.html")


def auction_bet(request, pk: int):
    if request.method == "POST":
        sender = request.user.id
        bet = request.POST.get('username', '')
        Lot.objects.create(sender=sender, sum_of_bet=bet, auction_id=pk)
        auction = Auction.objects.get(pk=pk)
        auction.current_better = sender
        auction.current_bet = bet
        auction.current_bet = bet
        auction.seconds_to_end = 60

        return HttpResponse("fsfesfs")
    else:
        print("------------------")
        print("------------------")
        return render(request, "success-auction.html")
