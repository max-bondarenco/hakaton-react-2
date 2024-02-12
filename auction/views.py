import datetime

from _decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from auction.models import Auction, User, Lot, Transation

from hakaton.views import account


def index(request: HttpRequest):
    return render(request, "index.html")


def auction_list_detail(request, pk: int):
    auction = Auction.objects.get(pk=pk)
    context = {
        "auction": auction,
        "lots": auction.lot_set.all(),
        "participants": auction.participants.all()
    }
    return render(request, "auction/auction-info.html", context=context)


@login_required
def auction_my(request):
    auctions = Auction.objects.filter(creator_id=request.user.id)
    context = {
        "auctions": auctions,
    }
    return render(request, "auction/auction-my.html", context=context)


@login_required
def auction_going(request, pk: int):
    auction = Auction.objects.get(pk=pk)
    if request.user not in auction.participants.all():
        auction.participants.add(request.user)
        auction.save()
    context = {
        "auction": auction,
        "lots": auction.lot_set.all(),
        "participants": auction.participants.all()
    }

    start_time = datetime.datetime.strptime(
        str(auction.time_of_start),
        "%Y-%m-%d %H:%M:%S"
    )
    if datetime.datetime.now() >= start_time:

        if request.method == "POST":
            return auction_bet(request, pk)

        if auction.seconds_to_end == 0 and not auction.is_completed:
            complete_auction(auction)
        if not auction.is_completed and auction.current_better_id:
            auction.seconds_to_end -= 5
            auction.save()
        if auction.is_completed:
            return render(
                request,
                "auction/auction-completed.html",
                context=context
            )
        return render(request, "auction/auction-going.html", context=context)
    return render(request, "auction/auction-not-going.html", context=context)


@login_required
def lots_my(request):
    if request.user.is_authenticated:
        lots = Lot.objects.filter(
            sender_id=request.user.id
        ).select_related("auction")
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

        except Exception as e:
            print("exception", e)
            return HttpResponse(e)
        return HttpResponseRedirect("/auction/my-auctions")
    return render(request, "auction/auction-create.html")


def auction_bet(request, pk: int):
    auction = Auction.objects.get(pk=pk)
    if request.method == "POST":
        if request.POST.get('bet', ''):
            bet = Decimal(request.POST.get('bet', ''))
            sender = request.user.id
        else:
            return render(request, "auction/auction-going.html")
        if User.objects.get(pk=request.user.id).balance < bet:
            return HttpResponse("<h1>Не вистачає грошей</h1>")
        if bet <= auction.current_bet:
            return HttpResponse("<h1>Ставка не може бути менша за поточну!!!</h1>")
        Lot.objects.create(
            sender_id=sender,
            sum_of_bet=bet,
            auction_id=pk,
            is_completed=False
        )

        auction = Auction.objects.get(pk=pk)
        auction.current_better_id = sender
        auction.current_bet = bet
        auction.seconds_to_end = 60
        auction.save()
        return HttpResponseRedirect(f"/auction/{pk}/going")
    return HttpResponse("<H1>Помилка</H1>")


@atomic
def complete_auction(auction: Auction):
    auction.is_completed = True
    buyer = auction.current_better
    buyer.balance -= auction.current_bet
    buyer.save()
    auction.creator.balance += auction.current_bet
    auction.creator.save()
    auction.save()
    Transation.objects.create(
        sender=buyer,
        recipient=auction.creator,
        sum_of_transaction=auction.current_bet
    )


def create_auction_success(request):
    return render(request, "auction/success-auction-create.html")


def auction_list(request):
    auctions = Auction.objects.filter(is_completed=0)
    if request.method == "POST":
        auctions = auctions.filter(name__contains=request.POST["query"])
    context = {
        "auction_list": auctions
    }
    return render(request, "auction/auction-list.html", context=context)


@atomic
def auction_refactor(request, pk: int):
    try:
        auction = Auction.objects.get(pk=pk)
    except Exception as e:
        return HttpResponse(e)
    context = {
        "auction": auction
    }

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        image = request.FILES["image"]
        start_price = request.POST["start_price"]
        minimal_bet = request.POST["minimal_bet"]
        price_of_ransom = request.POST["price_of_ransom"]
        date_start = request.POST["date_start"]

        if not image:
            image = auction.image
        auction.name = name
        auction.description = description
        auction.image = image
        auction.start_price = start_price
        auction.minimal_bet = minimal_bet
        auction.price_of_ransom = price_of_ransom
        auction.date_start = date_start
        auction.save()
        return auction_my(request)
    else:
        return render(
            request,
            "auction/auction-refactor.html",
            context=context
        )


def auction_ransom(request, pk: int):
    auction = Auction.objects.get(pk=pk)
    context = {
        "auction": auction,
        "lots": auction.lot_set.all(),
        "participants": auction.participants.all()
    }
    return render(request, "auction/auction-ransom.html", context=context)


@atomic
def auction_buy(request, pk: int):

    auction = Auction.objects.get(pk=pk)
    creator = auction.creator
    user = User.objects.get(pk=request.user.id)
    if user.balance < auction.price_of_ransom:
        return HttpResponse("<h1>Не вистачає грошей для викупу!!!</h1>")
    user.balance -= auction.price_of_ransom
    user.save()
    auction.current_better = user
    creator.balance += auction.price_of_ransom
    creator.save()
    auction.is_completed = True
    auction.seconds_to_end = 0
    auction.save()
    return auction_ransom(request, pk)
