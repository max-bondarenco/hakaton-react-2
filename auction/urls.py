

from django.urls import path

from auction.views import auction_list_detail, auction_my, auction_going, \
    lots_my, create_auction, create_auction_success, auction_list, \
    auction_bet, auction_refactor, auction_buy, api_list_auction

urlpatterns = [
    path('', auction_list, name="auction"),
    path('<int:pk>/', auction_list_detail),
    path('<int:pk>/refactor/', auction_refactor),
    path('<int:pk>/going/', auction_going),
    path('<int:pk>/going/buy/', auction_buy),
    path('<int:pk>/going/bet/', auction_bet),
    path('my-auctions/', auction_my),
    path(
        'create-auction/',
        create_auction,
        name='create_auction'
    ),
    path(
        'create-auction/success/',
        create_auction_success,
        name='create_auction_success'
    ),
    path('my-lots/', lots_my),
    path('react/', api_list_auction),
    ]


app_name = "auction"
