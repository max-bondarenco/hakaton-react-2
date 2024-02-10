
from django.urls import path, include

from auction.forms import AuctionListView, AuctionModelCreateView
from auction.views import auction_list_detail, auction_my, auction_going, auction_going_accept, lots_my, create_auction

urlpatterns = [
    path('', AuctionListView.as_view(), name="auction"),
    path('<int:pk>/', auction_list_detail),
    path('<int:pk>/going/', auction_going),
    path('<int:pk>/going/accepted/', auction_going_accept),
    path('my-auctions/', auction_my),
    path('create-auction/', AuctionModelCreateView.as_view(), name='your_model_create'),
    path('my-lots/', lots_my),
    ]

app_name = "auction"
