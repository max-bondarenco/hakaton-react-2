from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Auction, Transation, Lot, User


admin.site.register(Auction)
admin.site.register(User)
