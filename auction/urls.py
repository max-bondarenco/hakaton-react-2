

from django.urls import path, include

from auction.views import auction_list_detail, auction_my, auction_going, auction_going_accept, lots_my, create_auction, \
    create_auction_success, auction_list, auction_bet, auction_refactor, auction_buy


urlpatterns = [
    path('', auction_list, name="auction"),
    path('<int:pk>/', auction_list_detail),
    path('<int:pk>/refactor', auction_refactor),
    path('<int:pk>/going/', auction_going),
    path('<int:pk>/going/', auction_buy),
    path('<int:pk>/going/accepted/', auction_going_accept),
    path('<int:pk>/going/bet/', auction_bet),
    path('my-auctions/', auction_my),
    path('create-auction/', create_auction, name='create_auction'),
    path('create-auction/success', create_auction_success, name='create_auction_success'),
    path('my-lots/', lots_my),
    ]


app_name = "auction"
