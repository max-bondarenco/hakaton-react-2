from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from auction.forms import AuctionListView, AuctionModelCreateView
from auction.views import auction_list_detail, auction_my, auction_going, auction_going_accept, lots_my, create_auction,create_auction_success

urlpatterns = [
    path('', AuctionListView.as_view(), name="auction"),
    path('<int:pk>/', auction_list_detail),
    path('<int:pk>/going/', auction_going),
    path('<int:pk>/going/accepted/', auction_going_accept),
    path('my-auctions/', auction_my),
    path('create-auction/', create_auction, name='create_auction'),
    path('create-auction/success', create_auction_success, name='create_auction_success'),
    path('my-lots/', lots_my),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "auction"
