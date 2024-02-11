from django.urls import reverse_lazy
from django.views import generic
from django import forms
from django.views.generic import CreateView

from auction.models import Auction


class AuctionListView(generic.ListView):
    model = Auction
    template_name = "auction/auction-list.html"


class AuctionModelForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["name", "description", "image", "start_price",
                  "minimal_bet", "price_of_ransom", "time_of_start"]


class AuctionCreateView(generic.CreateView):
    form_class = AuctionListView
    success_url = reverse_lazy("auction:auction")


class AuctionModelCreateView(CreateView):
    model = Auction
    form_class = AuctionModelForm
    template_name = 'auction/auction-create.html'
    success_url = '/success-auction.html/'


class UserCreateView(generic.CreateView):
    form_class = AuctionListView
    success_url = reverse_lazy("auction:auction")
