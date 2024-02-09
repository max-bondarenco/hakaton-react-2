
from django.urls import path, include
from auction.views import auction_list, auction_list_detail

urlpatterns = [
    path('', auction_list, name="auction"),
    path('<int:pk>/', auction_list_detail),
    ]

app_name = "auction"
