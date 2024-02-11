import datetime
import os

from _decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from auction.models import Auction, User, Lot, Transation
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


@login_required
def auction_my(request):
    auctions = Auction.objects.filter(creator_id=request.user.id)
    print("auction")
    print(auctions)
    context = {
        "auctions": auctions,
    }
    return render(request, "auction/auction-my.html", context=context)


@login_required
def auction_going(request, pk: int):
    if request.method == "POST":
        return auction_bet(request, pk)
    auction = Auction.objects.get(pk=pk)
    context = {
        "auction": auction,
    }
    if auction.seconds_to_end == 0 and not auction.is_completed:
        complete_auction(auction)
    if not auction.is_completed and auction.current_better_id:
        auction.seconds_to_end -= 5
        auction.save()
        print("Second to end:")
        print(auction.seconds_to_end)
    print("")
    start_time = datetime.datetime.strptime(str(auction.time_of_start), "%Y-%m-%d %H:%M:%S")
    print("Data")
    print(start_time)
    print("nigaaa")
    print(datetime.datetime.now() > start_time)
    print(datetime.datetime.now())
    if datetime.datetime.now() >= start_time:
        if auction.is_completed:
            return render(request, "auction/auction-completed.html", context=context)
        else:
            return render(request, "auction/auction-going.html", context=context)
    else:
        return render(request, "auction/auction-not-going.html", context=context)


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


@login_required
def lots_my(request):
    if request.user.is_authenticated:
        lots = Lot.objects.filter(sender_id=request.user.id).select_related("auction")
        context = {
            "lots": lots,
        }
        return render(request, "auction/lots-my.html", context=context)
    return account(request)


@login_required
def create_auction(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        image = request.FILES["image"]
        start_price = request.POST["start_price"]
        minimal_bet = request.POST["minimal_bet"]
        price_of_ransom = request.POST["price_of_ransom"]
        date_start = request.POST["date_start"]
        try:
            Auction.objects.create(
                creator=request.user,
                name=name,
                description=description,
                image=image,
                time_of_start=date_start,
                minimal_bet=minimal_bet,
                price_of_ransom=price_of_ransom,
                start_price=start_price,
            )
            print("Auction-----")
            print(Auction.objects.last())

        except Exception as e:
            print("exception", e)
            return HttpResponse(e)
        return HttpResponseRedirect("/auction/my-auctions")
    return render(request, "auction/create-auction.html")


def auction_bet(request, pk: int):
    if request.method == "POST":
        sender = request.user.id
        bet = Decimal(request.POST.get('bet', ''))
        Lot.objects.create(sender_id=sender, sum_of_bet=bet, auction_id=pk, is_completed=False)
        if User.objects.get(pk=request.user.id).balance < bet:
            return HttpResponse("<h1>Не вистачає грошей</h1>")
        auction = Auction.objects.get(pk=pk)
        auction.current_better_id = sender
        auction.current_bet = bet
        auction.seconds_to_end = 60
        auction.save()
        print(auction.current_bet)
        print(auction.current_bet)
        print(auction.current_bet)
        return HttpResponseRedirect(f"/auction/{pk}/going")
    return HttpResponse("<H1>Помилка</H1>")


@atomic
def complete_auction(auction: Auction):
    auction.is_completed = True
    buyer = auction.current_better
    print(buyer.balance)
    print(auction.creator.balance)
    Transation.objects.create(sender=buyer, recipient=auction.creator, sum_of_transaction=auction.current_bet)
    auction.creator.balance += auction.current_bet
    buyer.balance -= auction.current_bet
    buyer.save()
    auction.save()
    print(buyer.balance)
    print(auction.creator.balance)



def create_auction_success(request):
    return render(request, "auction/success-auction-create.html")


def auction_list(request):
    context = {
        "auction_list": Auction.objects.all()
    }
    return render(request, "auction/auction-list.html", context=context)

